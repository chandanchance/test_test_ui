from flask import Flask, render_template, request, redirect, url_for, flash, session
import csv
import os
import random
import string
from werkzeug.utils import secure_filename
from io import StringIO

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_random_suffix():
    """Generate a random 3-digit number suffix"""
    return str(random.randint(100, 999))

def extract_headers_from_csv(file_path):
    """Extract headers from CSV file using built-in csv module"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)  # Get the first row (headers)
            return headers
    except Exception as e:
        print(f"Error reading CSV file {file_path}: {str(e)}")
        return []

def read_reference_usecases():
    """Read business usecase names and database names from reference.csv"""
    try:
        usecases = []
        with open('reference.csv', 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                usecases.append({
                    'business_usecase_name': row['business_usecase_name'],
                    'database_name': row['database_name']
                })
        return usecases
    except Exception as e:
        print(f"Error reading reference.csv: {str(e)}")
        return []

@app.route('/')
def index():
    return redirect(url_for('upload_files'))

@app.route('/upload_files', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        if 'files' not in request.files:
            flash('No files selected')
            return redirect(request.url)
        
        files = request.files.getlist('files')
        if not files or files[0].filename == '':
            flash('No files selected')
            return redirect(request.url)
        
        # Process uploaded files and extract headers
        all_headers = []
        file_headers_mapping = {}  # Track which headers come from which file
        
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                try:
                    headers = extract_headers_from_csv(filepath)
                    for header in headers:
                        if header not in file_headers_mapping:
                            file_headers_mapping[header] = filename
                    all_headers.extend(headers)
                except Exception as e:
                    flash(f'Error reading {filename}: {str(e)}')
        
        if all_headers:
            # Remove duplicates while preserving order
            unique_headers = list(dict.fromkeys(all_headers))
            session['headers'] = unique_headers
            session['file_headers_mapping'] = file_headers_mapping
            session['concatenated_headers'] = "Business usecase that is detected"#', '.join(unique_headers)
            return redirect(url_for('confirm_usecase'))
        else:
            flash('No valid headers found in uploaded files')
            return redirect(request.url)
    
    return render_template('upload_files.html')

@app.route('/confirm_usecase', methods=['GET', 'POST'])
def confirm_usecase():
    if 'headers' not in session:
        return redirect(url_for('upload_files'))
    
    if request.method == 'POST':
        user_input = request.form.get('usecase_text', '')
        session['user_usecase'] = user_input
        return redirect(url_for('confirm_columns'))
    
    # Read reference usecases
    reference_usecases = read_reference_usecases()
    
    return render_template('confirm_usecase.html', 
                         headers=session.get('concatenated_headers', ''),
                         reference_usecases=reference_usecases)

@app.route('/confirm_columns', methods=['GET', 'POST'])
def confirm_columns():
    if 'headers' not in session:
        return redirect(url_for('upload_files'))
    
    if request.method == 'POST':
        # Process the edited columns
        headers = session.get('headers', [])
        edited_columns = {}
        table_names = {}
        
        for header in headers:
            edited_value = request.form.get(f'column_{header}', '')
            table_name = request.form.get(f'table_{header}', '')
            if edited_value:
                edited_columns[header] = edited_value
            if table_name:
                table_names[header] = table_name
        
        session['edited_columns'] = edited_columns
        session['table_names'] = table_names
        return redirect(url_for('process_confirmation'))
    
    # Generate headers with random numbers for display
    headers = session.get('headers', [])
    file_headers_mapping = session.get('file_headers_mapping', {})
    headers_with_random = {}
    for header in headers:
        random_suffix = generate_random_suffix()
        headers_with_random[header] = f"{header}_{random_suffix}"
    
    session['headers_with_random'] = headers_with_random
    
    return render_template('confirm_columns.html', 
                         headers_with_random=headers_with_random,
                         file_headers_mapping=file_headers_mapping)

@app.route('/process_confirmation')
def process_confirmation():
    if 'edited_columns' not in session:
        return redirect(url_for('upload_files'))
    
    edited_columns = session.get('edited_columns', {})
    table_names = session.get('table_names', {})
    original_headers = session.get('headers', [])
    headers_with_random = session.get('headers_with_random', {})
    file_headers_mapping = session.get('file_headers_mapping', {})
    
    # Print changes to console (backend processing)
    print("=== USER CHANGES ===")
    for header in original_headers:
        original_value = headers_with_random.get(header, header)
        edited_value = edited_columns.get(header, original_value)
        table_name = table_names.get(header, file_headers_mapping.get(header, 'Unknown'))
        
        print(f"Column '{header}' from file '{file_headers_mapping.get(header, 'Unknown')}':")
        print(f"  - Table Name: '{table_name}'")
        if edited_value != original_value:
            print(f"  - Modified Header: '{original_value}' -> '{edited_value}'")
        else:
            print(f"  - Modified Header: No changes (kept as '{original_value}')")
        print()
    print("===================")
    
    # Clear session data
    session.clear()
    
    return render_template('process_confirmation.html', success=True)

if __name__ == '__main__':
    app.run(debug=True) 