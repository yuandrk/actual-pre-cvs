import io
from flask import Flask, request, render_template, send_file, jsonify, make_response
import pandas as pd
from datetime import datetime
import logging
from werkzeug.utils import secure_filename

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Create Flask application
app = Flask(__name__)

# Configure application
app.config.update(
    MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # Limit file size to 16MB
    UPLOAD_FOLDER='/tmp'  # Temporary folder for file uploads
)

ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def parse_csv(file_content, start_date):
    try:
        # Try different encodings
        encodings = ['utf-8', 'Windows-1252', 'iso-8859-1']
        df = None
        
        for encoding in encodings:
            try:
                df = pd.read_csv(io.BytesIO(file_content), encoding=encoding, skiprows=3)
                logger.info(f"Successfully read CSV with encoding: {encoding}")
                break
            except UnicodeDecodeError:
                logger.warning(f"Failed to decode CSV with encoding: {encoding}")
                continue
        
        if df is None:
            logger.error("Failed to decode CSV with any of the attempted encodings")
            raise ValueError("Unable to decode the CSV file with the attempted encodings.")
        
        # Convert 'Date' column to datetime format
        df['Date'] = pd.to_datetime(df['Date'], format='%d %b %Y')
        logger.debug("Successfully converted Date column to datetime format")
        
        # Filter the DataFrame to only include rows on or after the start date
        original_rows = len(df)
        df = df[df['Date'] >= pd.to_datetime(start_date)]
        filtered_rows = len(df)
        logger.info(f"Filtered DataFrame from {original_rows} to {filtered_rows} rows based on start date: {start_date}")
        
        # Remove the pound sign and convert columns to numeric
        for col in ['Paid out', 'Paid in', 'Balance']:
            df[col] = pd.to_numeric(df[col].str.replace('£', '', regex=True))
        logger.debug("Successfully converted monetary columns to numeric format")
        
        return df
    except Exception as e:
        logger.error(f"Error processing CSV file: {str(e)}", exc_info=True)
        return None

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        logger.info("Received POST request for file upload")
        if 'file' not in request.files:
            logger.warning("No file part in the request")
            return 'No file part'
        file = request.files['file']
        start_date = request.form['start_date']
        
        if file.filename == '':
            logger.warning("No selected file in the request")
            return 'No selected file'
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            logger.info(f"Processing file: {filename} with start date: {start_date}")
            file_content = file.read()
            
            df = parse_csv(file_content, start_date)
            if df is not None:
                # Convert DataFrame back to CSV
                output = io.StringIO()
                df.to_csv(output, index=False)
                output.seek(0)
                
                logger.info(f"Successfully processed file {filename}. Sending response.")
                return send_file(
                    io.BytesIO(output.getvalue().encode('utf-8')),
                    as_attachment=True,
                    download_name=f"processed_{filename}",
                    mimetype='text/csv'
                )
            else:
                logger.error(f"Failed to process file: {filename}")
                return 'Error processing file. Please check the file format and encoding.'
        else:
            logger.warning(f"Invalid file type: {file.filename}")
            return 'Invalid file type'
    return render_template('upload.html')

@app.route('/api/process-csv', methods=['POST'])
def process_csv_api():
    try:
        logger.info("Received API request for CSV processing")
        # Check if file is present in request
        if 'file' not in request.files:
            logger.warning("No file provided in API request")
            return make_response(jsonify({'error': 'No file provided'}), 400)
        
        file = request.files['file']
        if file.filename == '':
            logger.warning("Empty filename in API request")
            return make_response(jsonify({'error': 'No file selected'}), 400)
            
        # Check if start_date is provided
        start_date = request.form.get('start_date')
        if not start_date:
            logger.warning("No start date provided in API request")
            return make_response(jsonify({'error': 'Start date is required'}), 400)
            
        # Validate file type
        if not allowed_file(file.filename):
            logger.warning(f"Invalid file type in API request: {file.filename}")
            return make_response(jsonify({'error': 'Invalid file type. Only CSV files are allowed'}), 400)
            
        # Process the file
        logger.info(f"Processing API request for file: {file.filename} with start date: {start_date}")
        file_content = file.read()
        df = parse_csv(file_content, start_date)
        
        if df is not None:
            # Convert DataFrame to CSV
            output = io.StringIO()
            df.to_csv(output, index=False)
            output.seek(0)
            
            logger.info(f"Successfully processed API request for file: {file.filename}")
            # Create response with CSV file
            response = make_response(output.getvalue())
            response.headers['Content-Type'] = 'text/csv'
            response.headers['Content-Disposition'] = f'attachment; filename=processed_{secure_filename(file.filename)}'
            return response
        else:
            logger.error(f"Failed to process file in API request: {file.filename}")
            return make_response(jsonify({'error': 'Error processing file. Please check the file format and encoding'}), 400)
            
    except Exception as e:
        logger.error(f"Unexpected error in API request: {str(e)}", exc_info=True)
        return make_response(jsonify({'error': str(e)}), 500)

# Remove the direct run statement and replace with proper app factory pattern
def create_app():
    return app

# This allows direct running for development, but won't be used by Gunicorn
if __name__ == '__main__':
    logger.warning("Running in development mode. Use Gunicorn for production!")
    app.run(host='0.0.0.0', port=9000, debug=False)