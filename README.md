# CSV Processor Web Application

This is a production-ready web application built with Flask and Gunicorn that allows users to upload CSV files, process them from a specified start date, and download the processed results.

## Features

- Upload CSV files through web interface or API
- Specify a start date for processing
- Download processed CSV files
- RESTful API endpoint for programmatic access
- Production-grade WSGI server (Gunicorn)
- Comprehensive logging system
- Docker containerization
- Resource management and monitoring

## Prerequisites

- Docker
- Docker Compose (optional, but recommended)

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/csv-processor.git
   cd csv-processor
   ```

2. Build and run the Docker container:
   ```bash
   docker-compose up --build
   ```
   Or without Docker Compose:
   ```bash
   docker build -t csv-processor .
   docker run -p 9000:5000 csv-processor
   ```

3. Open a web browser and navigate to `http://localhost:9000`

## Usage

### Web Interface

1. Upload a CSV file using the web interface
2. Specify the start date for processing
3. Click "Process and Download" to receive the processed file

### API Endpoint

The application provides a RESTful API endpoint for programmatic access:

**POST /api/process-csv**
- Content-Type: `multipart/form-data`
- Parameters:
  - `file`: CSV file to process (required)
  - `start_date`: Start date in YYYY-MM-DD format (required)

Example using curl:
```bash
curl -X POST -F "file=@your_file.csv" -F "start_date=2024-01-01" http://localhost:9000/api/process-csv
```

Example using Python:
```python
import requests

url = 'http://localhost:9000/api/process-csv'
files = {'file': open('your_file.csv', 'rb')}
data = {'start_date': '2024-01-01'}

response = requests.post(url, files=files, data=data)

if response.headers['Content-Type'] == 'text/csv':
    with open('processed_file.csv', 'wb') as f:
        f.write(response.content)
else:
    print(response.json())  # Handle error response
```

## Project Structure

```
csv-processor/
├── LICENSE
├── README.md
├── app.py              # Main application file
├── docker-compose.yml  # Docker Compose configuration
├── Dockerfile         # Docker build instructions
├── requirements.txt   # Python dependencies
├── logs/             # Application logs directory
│   ├── access.log    # Gunicorn access logs
│   └── error.log     # Gunicorn error logs
└── templates/
    └── upload.html   # Web interface template
```

## Configuration

### Environment Variables

- `WORKERS`: Number of Gunicorn workers (default: 4)
- `LOG_LEVEL`: Logging level (default: INFO)
- `PYTHONUNBUFFERED`: Python output buffering (default: 1)

### Resource Limits

Docker container is configured with the following resource limits:
- CPU: 2 cores
- Memory: 2GB

### Logging

The application implements a comprehensive logging system:

1. **Application Logs**:
   - Location: `./logs/` directory
   - Access logs: `access.log`
   - Error logs: `error.log`
   - Log format: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`
   - Timestamp format: `YYYY-MM-DD HH:MM:SS`

2. **Log Levels**:
   - DEBUG: Detailed processing information
   - INFO: Successful operations
   - WARNING: Potential issues
   - ERROR: Operation failures
   - CRITICAL: System-level issues

3. **Docker Container Logs**:
   - View logs: `docker-compose logs web`
   - Follow logs: `docker-compose logs -f web`
   - Log rotation: 10MB max size, keep 3 files

## Development

To run the application locally without Docker:

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```

3. Run with Gunicorn:
   ```bash
   gunicorn --bind 0.0.0.0:9000 --workers 4 app:app
   ```

   Or for development with Flask:
   ```bash
   python app.py
   ```

## Security Features

- Non-root user in Docker container
- File size limits (16MB max)
- Secure filename handling
- WSGI production server
- Resource limitations
- Temporary file cleanup

## Error Handling

The application includes comprehensive error handling:
- File format validation
- Encoding detection
- Date format validation
- Exception tracking with stack traces
- Detailed error logging
- User-friendly error messages

## License

[MIT License](https://opensource.org/licenses/MIT)

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request
