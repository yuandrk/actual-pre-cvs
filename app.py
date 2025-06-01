import io
from flask import Flask, request, render_template, send_file, jsonify, make_response
import pandas as pd
from datetime import datetime
import logging
import os
import glob
from werkzeug.utils import secure_filename

# Configure logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Create Flask application
app = Flask(__name__)

# Configure application from environment variables
app.config.update(
    MAX_CONTENT_LENGTH=int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024)),
    UPLOAD_FOLDER=os.getenv('UPLOAD_FOLDER', '/tmp'),
    DATE_FORMAT=os.getenv('DATE_FORMAT', '%d %b %Y'),
    NUMERIC_COLUMNS=os.getenv('NUMERIC_COLUMNS', 'Paid out,Paid in,Balance').split(','),
    SKIP_ROWS=int(os.getenv('SKIP_ROWS', 3))
)

# Get allowed extensions from environment
ALLOWED_EXTENSIONS = set(os.getenv('ALLOWED_EXTENSIONS', 'csv').split(','))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def parse_csv(file_content, start_date=None):
    try:
        # Try different encodings
        encodings = ['utf-8', 'Windows-1252', 'iso-8859-1']
        df = None
        
        for encoding in encodings:
            try:
                df = pd.read_csv(io.BytesIO(file_content), 
                               encoding=encoding, 
                               skiprows=app.config['SKIP_ROWS'])
                logger.info(f"Successfully read CSV with encoding: {encoding}")
                break
            except UnicodeDecodeError:
                logger.warning(f"Failed to decode CSV with encoding: {encoding}")
                continue
            except Exception as e:
                logger.warning(f"Error reading CSV with encoding {encoding}: {str(e)}")
                continue
        
        if df is None:
            logger.error("Failed to decode CSV with any of the attempted encodings")
            raise ValueError("Unable to decode the CSV file with the attempted encodings.")
        
        # Check if 'Date' column exists
        if 'Date' in df.columns:
            try:
                # Convert 'Date' column to datetime format
                df['Date'] = pd.to_datetime(df['Date'], format=app.config['DATE_FORMAT'])
                logger.debug("Successfully converted Date column to datetime format")
                
                # Filter by start date if provided
                if start_date:
                    original_rows = len(df)
                    df = df[df['Date'] >= pd.to_datetime(start_date)]
                    filtered_rows = len(df)
                    logger.info(f"Filtered DataFrame from {original_rows} to {filtered_rows} rows based on start date: {start_date}")
            except Exception as e:
                logger.warning(f"Error processing Date column: {str(e)}")
        
        # Check for numeric columns that need conversion
        for col in app.config['NUMERIC_COLUMNS']:
            if col in df.columns:
                try:
                    # Check if column has string values
                    if df[col].dtype == 'object':
                        df[col] = pd.to_numeric(df[col].str.replace('£', '', regex=True))
                except Exception as e:
                    logger.warning(f"Error converting column {col} to numeric: {str(e)}")
                    continue
        
        logger.debug("Successfully processed CSV data")
        return df
    except Exception as e:
        logger.error(f"Error processing CSV file: {str(e)}", exc_info=True)
        return None

def dataframe_to_markdown(df):
    """Convert DataFrame to markdown format"""
    try:
        return df.to_markdown(index=False)
    except Exception as e:
        logger.error(f"Error converting DataFrame to markdown: {str(e)}")
        # Fallback to a simple HTML table if markdown conversion fails
        return df.to_html(index=False)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        logger.info("Received POST request for file upload")
        if 'file' not in request.files:
            logger.warning("No file part in the request")
            return 'No file part'
        
        files = request.files.getlist('file')
        process_option = request.form.get('process_option', 'parse')
        output_format = request.form.get('output_format', 'csv')
        
        if not files or files[0].filename == '':
            logger.warning("No selected files in the request")
            return 'No selected files'
        
        # For parse option, start date is required
        if process_option == 'parse':
            if not request.form.get('start_date'):
                logger.warning("No start date provided for parse operation")
                return 'Start date is required for parsing'
            start_date = request.form['start_date']
        else:
            # For merge, start date is optional
            start_date = request.form.get('start_date')
        
        # Check for merge option
        if process_option == 'merge':
            logger.info(f"Processing merge request for {len(files)} files")
            
            df_list = []
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    logger.info(f"Processing file for merge: {filename}")
                    file_content = file.read()
                    
                    # For merge, we pass the start_date only if it's provided
                    df = parse_csv(file_content, start_date)
                    if df is not None:
                        df_list.append(df)
                    else:
                        logger.warning(f"Failed to process file for merge: {filename}")
            
            if not df_list:
                logger.error("No valid CSV files found for merging")
                return 'No valid CSV files for merging. Please check file formats.'
                
            # Merge all dataframes
            merged_df = pd.concat(df_list, ignore_index=True)
            
            # Process output based on format selection
            if output_format == 'markdown':
                # Convert to markdown
                output_content = dataframe_to_markdown(merged_df)
                mimetype = 'text/markdown'
                download_name = "merged_health_data.md"
            else:
                # Convert to CSV
                output = io.StringIO()
                merged_df.to_csv(output, index=False)
                output.seek(0)
                output_content = output.getvalue()
                mimetype = 'text/csv'
                download_name = "merged_health_data.csv"
            
            logger.info(f"Successfully merged files into {output_format} format")
            return send_file(
                io.BytesIO(output_content.encode('utf-8')),
                as_attachment=True,
                download_name=download_name,
                mimetype=mimetype
            )
        
        # Process single file (or first file if multiple selected with parse option)
        file = files[0]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            logger.info(f"Processing single file: {filename} with start date: {start_date}")
            file_content = file.read()
            
            df = parse_csv(file_content, start_date)
            if df is not None:
                # Process output based on format selection
                if output_format == 'markdown':
                    # Convert to markdown
                    output_content = dataframe_to_markdown(df)
                    mimetype = 'text/markdown'
                    download_name = f"processed_{filename.rsplit('.', 1)[0]}.md"
                else:
                    # Convert to CSV
                    output = io.StringIO()
                    df.to_csv(output, index=False)
                    output.seek(0)
                    output_content = output.getvalue()
                    mimetype = 'text/csv'
                    download_name = f"processed_{filename}"
                
                logger.info(f"Successfully processed file {filename} to {output_format}. Sending response.")
                return send_file(
                    io.BytesIO(output_content.encode('utf-8')),
                    as_attachment=True,
                    download_name=download_name,
                    mimetype=mimetype
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
        
        files = request.files.getlist('file')
        if not files or files[0].filename == '':
            logger.warning("Empty filename in API request")
            return make_response(jsonify({'error': 'No file selected'}), 400)
            
        # Get processing options
        process_option = request.form.get('process_option', 'parse')
        output_format = request.form.get('output_format', 'csv')
        
        # For parse option, start date is required
        if process_option == 'parse':
            start_date = request.form.get('start_date')
            if not start_date:
                logger.warning("No start date provided for parse API request")
                return make_response(jsonify({'error': 'Start date is required for parsing'}), 400)
        else:
            # For merge, start date is optional
            start_date = request.form.get('start_date')
        
        # Check for merge option
        if process_option == 'merge':
            logger.info(f"Processing API merge request for {len(files)} files")
            
            df_list = []
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    logger.info(f"Processing file for API merge: {filename}")
                    file_content = file.read()
                    
                    # For merge, we pass the start_date only if it's provided
                    df = parse_csv(file_content, start_date)
                    if df is not None:
                        df_list.append(df)
                    else:
                        logger.warning(f"Failed to process file for API merge: {filename}")
            
            if not df_list:
                logger.error("No valid CSV files found for API merging")
                return make_response(jsonify({'error': 'No valid CSV files for merging. Please check file formats'}), 400)
                
            # Merge all dataframes
            merged_df = pd.concat(df_list, ignore_index=True)
            
            # Process output based on format selection
            if output_format == 'markdown':
                # Convert to markdown
                output_content = dataframe_to_markdown(merged_df)
                content_type = 'text/markdown'
                filename = 'merged_health_data.md'
            else:
                # Convert to CSV
                output = io.StringIO()
                merged_df.to_csv(output, index=False)
                output.seek(0)
                output_content = output.getvalue()
                content_type = 'text/csv'
                filename = 'merged_health_data.csv'
            
            logger.info(f"Successfully merged CSV files in API request to {output_format}")
            # Create response with appropriate format
            response = make_response(output_content)
            response.headers['Content-Type'] = content_type
            response.headers['Content-Disposition'] = f'attachment; filename={filename}'
            return response
        
        # Process single file
        file = files[0]
        # Validate file type
        if not allowed_file(file.filename):
            logger.warning(f"Invalid file type in API request: {file.filename}")
            return make_response(jsonify({'error': 'Invalid file type. Only CSV files are allowed'}), 400)
            
        # Process the file
        logger.info(f"Processing API request for file: {file.filename} with start date: {start_date}")
        file_content = file.read()
        df = parse_csv(file_content, start_date)
        
        if df is not None:
            # Process output based on format selection
            if output_format == 'markdown':
                # Convert to markdown
                output_content = dataframe_to_markdown(df)
                content_type = 'text/markdown'
                filename = f"processed_{secure_filename(file.filename).rsplit('.', 1)[0]}.md"
            else:
                # Convert to CSV
                output = io.StringIO()
                df.to_csv(output, index=False)
                output.seek(0)
                output_content = output.getvalue()
                content_type = 'text/csv'
                filename = f"processed_{secure_filename(file.filename)}"
            
            logger.info(f"Successfully processed API request for file: {file.filename} to {output_format}")
            # Create response with appropriate format
            response = make_response(output_content)
            response.headers['Content-Type'] = content_type
            response.headers['Content-Disposition'] = f'attachment; filename={filename}'
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
    app.run(
        host=os.getenv('HOST', '0.0.0.0'),
        port=int(os.getenv('PORT', 9000)),
        debug=os.getenv('DEBUG', 'False').lower() == 'true'
    )