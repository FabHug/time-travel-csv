# Time Travel CSV - Freestyle Libre Date Shifter

A FastAPI application that shifts dates in Freestyle Libre CSV files to make the latest date become today's date, while preserving the exact CSV format.

## Features

- **Register Type-Specific Processing**: Handles different measurement types (0, 1, 5, 6) separately
- **Exact Format Preservation**: Maintains the original CSV structure and headers
- **Proper Date Shifting**: Shifts all dates so the latest date of each register type becomes today
- **Web Interface**: Simple upload interface for CSV files

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
uvicorn main:app --reload
```

3. Visit http://localhost:8000 to use the web interface

## Deployment on Captain Rover

This application is configured for deployment on Captain Rover with the following files:

- `Dockerfile`: Container configuration
- `captain-definition`: Captain Rover deployment settings
- `.dockerignore`: Files to exclude from Docker build

### Deployment Steps

1. Push your code to a Git repository
2. Connect your repository to Captain Rover
3. Deploy using the Captain Rover dashboard

The application will be available at your Captain Rover domain.

## CSV Format

The application expects Freestyle Libre CSV files with the following structure:

```
Patientrapport,Skapat den,12-04-2023 06:25 UTC,Skapat av,Berit Gustafsson
F001,01-01-1900
Enhet,Serienummer,Enhetens tidsstämpel,Registertyp,Historiskt glukosvärde mmol/L,...
FreeStyle LibreLink,647B89DE-EDC9-43DF-97C8-5364B44315C7,12-01-2022 15:45,0,"6,4",,,,,,,,,,,,,,
```

## API Endpoints

- `GET /`: Web interface for file upload
- `POST /upload`: Upload CSV file and get shifted version

## Environment Variables

No environment variables are required for basic functionality. 