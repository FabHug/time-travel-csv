import csv
import io
from datetime import datetime
from .date_parser import try_parse_date, format_date_for_output

def is_freestyle_libre_format(lines):
    """Check if the CSV looks like a Freestyle Libre format."""
    if len(lines) < 4:
        return False
    
    return (lines[0].startswith('Patientrapport') and 
            lines[2].startswith('Enhet,Serienummer,Enhetens tidsstämpel'))

def parse_creation_date(header_line):
    """Parse the creation date from the header line."""
    try:
        header_parts = header_line.split(',')
        if len(header_parts) >= 3:
            creation_date_str = header_parts[2].strip()
            # Remove UTC suffix if present
            creation_date_str = creation_date_str.split(' UTC')[0]
            return try_parse_date(creation_date_str)
    except Exception:
        pass
    return None

def find_latest_dates_by_register_type(lines):
    """Find the latest date for each register type."""
    register_types = {}  # {register_type: latest_date}
    
    for line in lines[3:]:  # Skip header rows
        if not line.strip():
            continue
        
        try:
            # Parse the timestamp and register type using proper CSV parsing
            # Strip outer quotes if present
            clean_line = line.strip().strip('"')
            reader = csv.reader([clean_line])
            parts = next(reader)
            
            if len(parts) < 4:
                continue
                
            timestamp_str = parts[2].strip()
            register_type = parts[3].strip()
            
            if timestamp_str and register_type:
                date_obj = try_parse_date(timestamp_str)
                if date_obj:
                    if register_type not in register_types:
                        register_types[register_type] = date_obj
                    elif date_obj > register_types[register_type]:
                        register_types[register_type] = date_obj
                        
        except Exception:
            continue
    
    return register_types

def calculate_shifts(register_types):
    """Calculate the shift needed for each register type."""
    today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    shifts = {}
    for reg_type, latest_date in register_types.items():
        shifts[reg_type] = today - latest_date
    return shifts

def process_csv_line(line, shifts):
    """Process a single CSV line and shift its timestamp."""
    if not line.strip():
        return line
    
    try:
        # Parse the timestamp and register type using proper CSV parsing
        # Strip outer quotes if present
        clean_line = line.strip().strip('"')
        reader = csv.reader([clean_line])
        parts = next(reader)
        
        if len(parts) < 4:
            return line
            
        timestamp_str = parts[2].strip()
        register_type = parts[3].strip()
        
        if timestamp_str and register_type and register_type in shifts:
            date_obj = try_parse_date(timestamp_str)
            if date_obj:
                shifted_date = date_obj + shifts[register_type]
                shifted_timestamp = format_date_for_output(shifted_date)
                
                # Use f-string for easy format modification with clear part names
                device = parts[0]
                serial = parts[1]
                timestamp = shifted_timestamp
                register_type = parts[3]
                
                # Handle glucose value carefully - it might be split due to comma
                glucose_value = ''
                if len(parts) > 4:
                    if parts[4] and parts[4].strip():
                        glucose_value = parts[4].strip()
                        # If there's a comma in the glucose value, it might be split
                        if len(parts) > 5 and parts[5] and parts[5].strip():
                            glucose_value += ',' + parts[5].strip()
                            # Remove the extra part from remaining_fields
                            parts = parts[:5] + parts[6:]
                
                remaining_fields = ','.join(parts[5:]) if len(parts) > 5 else ''
                
                # Ensure glucose value is properly quoted (remove any existing quotes first)
                if glucose_value:
                    glucose_value = glucose_value.strip().strip('"')
                    glucose_value = f'"{glucose_value}"'
                
                reconstructed_line = f'{device},{serial},{timestamp},{register_type},{glucose_value},{remaining_fields}'
                
                return reconstructed_line
        return line
    except Exception:
        return line 