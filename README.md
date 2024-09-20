# CSV Processor Web Application

This is a simple web application built with Flask that allows users to upload CSV files, process them from a specified start date, and download the processed results.

## Features

- Upload CSV files
- Specify a start date for processing
- Download processed CSV files

## Prerequisites

- Docker
- Docker Compose (optional, but recommended)

## Quick Start

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/csv-processor.git
   cd csv-processor
   ```

2. Build and run the Docker container:
   ```
   docker-compose up --build
   ```
   Or without Docker Compose:
   ```
   docker build -t csv-processor .
   docker run -p 5000:5000 csv-processor
   ```

3. Open a web browser and navigate to `http://localhost:5000`

## Usage

1. Upload a CSV file using the web interface
2. Specify the start date for processing
3. Click "Process and Download" to receive the processed file

## Project Structure

```
csv-processor/
│
├── app.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
├── templates/
│   └── upload.html
├── uploads/
└── outputs/
```

## Development

To run the application locally without Docker:

1. Create a virtual environment and activate it
2. Install the requirements: `pip install -r requirements.txt`
3. Run the Flask app: `python app.py`

## License

[MIT License](https://opensource.org/licenses/MIT)
