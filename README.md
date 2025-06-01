# CSV Processor Web Application

This is a production-ready web application built with Flask and Gunicorn that allows users to upload CSV files, process them from a specified start date, and download the processed results.

## Features

- Upload CSV files through web interface or API
- Specify a start date for processing
- Download processed CSV files
- Merge multiple CSV files into a single dataset
- Export data in CSV or Markdown format
- Modern, intuitive user interface
- RESTful API endpoint for programmatic access
- Production-grade WSGI server (Gunicorn)
- Comprehensive logging system
- Docker containerization
- Resource management and monitoring
- Automated CI/CD with GitHub Actions
- Semantic versioning

## Prerequisites

- Docker
- Docker Compose (optional, but recommended)
- GitHub Account (for CI/CD and container registry)

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/csv-processor.git
   cd csv-processor
   ```

2. Build and run the Docker container:
   ```bash
   # Using the latest version
   docker pull ghcr.io/yourusername/csv-processor:latest
   docker run -p 9000:5000 ghcr.io/yourusername/csv-processor:latest
   ```
   
   Or build locally:
   ```bash
   docker-compose up --build
   ```

3. Open a web browser and navigate to `http://localhost:9000`

## Versioning

This project uses semantic versioning. The current version is stored in the `VERSION` file.

### Available Tags

The following Docker image tags are available:
- `latest`: Most recent version from the main branch
- `x.y.z` (e.g., `1.0.0`): Specific version
- `x.y` (e.g., `1.0`): Latest patch version of a minor release
- `x` (e.g., `1`): Latest minor version of a major release
- `sha-xxxxx`: Specific commit

### Using Specific Versions

```bash
# Pull specific version
docker pull ghcr.io/yourusername/csv-processor:1.0.0

# Pull latest patch of 1.0
docker pull ghcr.io/yourusername/csv-processor:1.0

# Pull latest minor of version 1
docker pull ghcr.io/yourusername/csv-processor:1
```

## Usage

### Web Interface

1. Upload one or more CSV files using the web interface
2. Select processing option:
   - **Parse and Filter**: Process a single file and filter by start date (requires start date)
   - **Merge Files**: Combine multiple files into a single dataset (start date optional)
3. Choose output format:
   - **CSV**: Standard format for spreadsheet software
   - **Markdown**: Format for easy display in documentation
4. Specify start date (required for Parse and Filter, optional for Merge)
5. Click "Process and Download" to receive the processed file

The interface includes smart features:
- Automatically suggests merge option when multiple files are selected
- Dynamic validation based on selected options
- Clear visual feedback on file selection
- Responsive design that works on desktop and mobile devices

### API Endpoint

The application provides a RESTful API endpoint for programmatic access:

**POST /api/process-csv**
- Content-Type: `multipart/form-data`
- Parameters:
  - `file`: CSV file(s) to process (required, can be multiple for merging)
  - `start_date`: Start date in YYYY-MM-DD format (required for parse, optional for merge)
  - `process_option`: Processing option (optional, default: 'parse')
    - `parse`: Process a single file and filter by start date
    - `merge`: Merge multiple files into a single dataset
  - `output_format`: Output format (optional, default: 'csv')
    - `csv`: Standard CSV format
    - `markdown`: Markdown table format

Example using curl for single file processing (CSV output):
```bash
curl -X POST -F "file=@your_file.csv" -F "start_date=2024-01-01" http://localhost:9000/api/process-csv
```

Example using curl for merging multiple files with markdown output:
```bash
curl -X POST -F "file=@file1.csv" -F "file=@file2.csv" -F "file=@file3.csv" -F "process_option=merge" -F "output_format=markdown" http://localhost:9000/api/process-csv
```

Example using Python for single file processing:
```python
import requests

url = 'http://localhost:9000/api/process-csv'
files = {'file': open('your_file.csv', 'rb')}
data = {'start_date': '2024-01-01'}

response = requests.post(url, files=files, data=data)

# Check content type to determine file extension
file_extension = 'csv'
if response.headers['Content-Type'] == 'text/markdown':
    file_extension = 'md'

if response.headers['Content-Type'] in ['text/csv', 'text/markdown']:
    with open(f'processed_file.{file_extension}', 'wb') as f:
        f.write(response.content)
else:
    print(response.json())  # Handle error response
```

Example using Python for merging multiple files with markdown output:
```python
import requests

url = 'http://localhost:9000/api/process-csv'
files = [
    ('file', open('file1.csv', 'rb')),
    ('file', open('file2.csv', 'rb')),
    ('file', open('file3.csv', 'rb'))
]
data = {
    'process_option': 'merge',
    'output_format': 'markdown'
}

response = requests.post(url, files=files, data=data)

if response.headers['Content-Type'] == 'text/markdown':
    with open('merged_health_data.md', 'wb') as f:
        f.write(response.content)
else:
    print(response.json())  # Handle error response
```

## Project Structure

```
csv-processor/
├── LICENSE
├── README.md
├── VERSION              # Current version number
├── app.py              # Main application file
├── docker-compose.yml  # Docker Compose configuration
├── Dockerfile         # Docker build instructions
├── requirements.txt   # Python dependencies
├── logs/             # Application logs directory
│   ├── access.log    # Gunicorn access logs
│   └── error.log     # Gunicorn error logs
├── .github/          # GitHub Actions configuration
│   └── workflows/
│       └── docker-build.yml
└── templates/
    └── upload.html   # Web interface template
```

## Configuration

### Environment Variables

- `WORKERS`: Number of Gunicorn workers (default: 4)
- `LOG_LEVEL`: Logging level (default: INFO)
- `PYTHONUNBUFFERED`: Python output buffering (default: 1)
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 5000)
- `ALLOWED_EXTENSIONS`: Allowed file types (default: csv)
- `MAX_CONTENT_LENGTH`: Maximum file size (default: 16MB)
- `UPLOAD_FOLDER`: Temporary upload directory (default: /tmp)
- `DATE_FORMAT`: Date format for parsing (default: %d %b %Y)
- `NUMERIC_COLUMNS`: Columns to convert to numeric (default: Paid out,Paid in,Balance)
- `SKIP_ROWS`: Number of rows to skip in CSV (default: 3)
- `DEBUG`: Debug mode (default: False)

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

## CI/CD Pipeline

The project includes a GitHub Actions workflow for automated building and publishing of Docker images:

1. **Triggers**:
   - Push to main branch
   - Push of version tags (v*.*.*)
   - Pull requests to main

2. **Features**:
   - Automated builds
   - Multi-tag support
   - Version extraction
   - Build caching
   - Security scanning
   - Container registry publishing

3. **Publishing a New Version**:
   ```bash
   # Update VERSION file
   echo "1.1.0" > VERSION
   
   # Commit and tag
   git add VERSION
   git commit -m "Bump version to 1.1.0"
   git tag v1.1.0
   git push && git push --tags
   ```

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

### Version Updates

When contributing, please follow these steps for version updates:

1. Update the VERSION file
2. Update relevant documentation
3. Create a pull request
4. After merge, create a new version tag
