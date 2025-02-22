import io
from flask import Flask, request, render_template, send_file, jsonify, make_response
import pandas as pd
from datetime import datetime
from werkzeug.utils import secure_filename

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
                break
            except UnicodeDecodeError:
                continue
        
        if df is None:
            raise ValueError("Unable to decode the CSV file with the attempted encodings.")
        
        # Convert 'Date' column to datetime format
        df['Date'] = pd.to_datetime(df['Date'], format='%d %b %Y')
        
        # Filter the DataFrame to only include rows on or after the start date
        df = df[df['Date'] >= pd.to_datetime(start_date)]
        
        # Remove the pound sign and convert columns to numeric
        for col in ['Paid out', 'Paid in', 'Balance']:
            df[col] = pd.to_numeric(df[col].str.replace('£', '', regex=True))
        
        return df
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        start_date = request.form['start_date']
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_content = file.read()
            
            df = parse_csv(file_content, start_date)
            if df is not None:
                # Convert DataFrame back to CSV
                output = io.StringIO()
                df.to_csv(output, index=False)
                output.seek(0)
                
                return send_file(
                    io.BytesIO(output.getvalue().encode('utf-8')),
                    as_attachment=True,
                    download_name=f"processed_{filename}",
                    mimetype='text/csv'
                )
            else:
                return 'Error processing file. Please check the file format and encoding.'
    return render_template('upload.html')

@app.route('/api/process-csv', methods=['POST'])
def process_csv_api():
    try:
        # Check if file is present in request
        if 'file' not in request.files:
            return make_response(jsonify({'error': 'No file provided'}), 400)
        
        file = request.files['file']
        if file.filename == '':
            return make_response(jsonify({'error': 'No file selected'}), 400)
            
        # Check if start_date is provided
        start_date = request.form.get('start_date')
        if not start_date:
            return make_response(jsonify({'error': 'Start date is required'}), 400)
            
        # Validate file type
        if not allowed_file(file.filename):
            return make_response(jsonify({'error': 'Invalid file type. Only CSV files are allowed'}), 400)
            
        # Process the file
        file_content = file.read()
        df = parse_csv(file_content, start_date)
        
        if df is not None:
            # Convert DataFrame to CSV
            output = io.StringIO()
            df.to_csv(output, index=False)
            output.seek(0)
            
            # Create response with CSV file
            response = make_response(output.getvalue())
            response.headers['Content-Type'] = 'text/csv'
            response.headers['Content-Disposition'] = f'attachment; filename=processed_{secure_filename(file.filename)}'
            return response
        else:
            return make_response(jsonify({'error': 'Error processing file. Please check the file format and encoding'}), 400)
            
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)

# Remove the direct run statement and replace with proper app factory pattern
def create_app():
    return app

# This allows direct running for development, but won't be used by Gunicorn
if __name__ == '__main__':
    print("Warning: Running in development mode. Use Gunicorn for production!")
    app.run(host='0.0.0.0', port=9000, debug=False)