from fastapi import FastAPI, File, UploadFile, Response
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi import Request
import io
from utils.csv_processor import (
    is_freestyle_libre_format,
    parse_creation_date,
    find_latest_dates_by_register_type,
    calculate_shifts,
    process_csv_line
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

def shift_csv_dates(file):
    """Main function to shift dates in Freestyle Libre CSV format."""
    file.seek(0)
    content = file.read().decode("utf-8")
    lines = content.split('\n')
    
    if len(lines) < 4:
        return None  # Need at least header rows + 1 data row
    
    # Check if this looks like a Freestyle Libre CSV
    if not is_freestyle_libre_format(lines):
        return None  # Not a Freestyle Libre format
    
    # Parse the creation date from header
    creation_date = parse_creation_date(lines[0])
    if not creation_date:
        return None
    
    # Group data by register type and find latest date for each type
    register_types = find_latest_dates_by_register_type(lines)
    
    if not register_types:
        return None
    
    # Calculate shifts for each register type
    shifts = calculate_shifts(register_types)
    
    # Apply the appropriate shift to each row based on its register type
    shifted_lines = []
    
    # Keep header rows unchanged
    shifted_lines.append(lines[0])  # Patientrapport line
    shifted_lines.append(lines[1])  # F001 line
    shifted_lines.append(lines[2])  # Enhet line
    
    # Shift dates in data rows based on register type
    for line in lines[3:]:
        processed_line = process_csv_line(line, shifts)
        shifted_lines.append(processed_line)
    
    return '\n'.join(shifted_lines)

@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    content = await file.read()
    shifted_csv = shift_csv_dates(io.BytesIO(content))
    if shifted_csv is None:
        return Response(content="Invalid Freestyle Libre CSV format or no date columns found.", status_code=400)
    return StreamingResponse(io.StringIO(shifted_csv), media_type="text/csv", headers={"Content-Disposition": f"attachment; filename=shifted_{file.filename}"})

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request}) 