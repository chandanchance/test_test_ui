# CSV Header Processor

A Flask-based web application that allows users to upload multiple CSV files, extract their headers, and modify them with a user-friendly interface.

## Features

- **Multi-file Upload**: Drag and drop or select multiple CSV files
- **Header Extraction**: Automatically extracts headers from uploaded CSV files
- **Header Modification**: Add random numbers to headers and edit them
- **Modern UI**: Beautiful, responsive interface with progress indicators
- **Backend Processing**: Console output for tracking changes

## Project Structure

```
usecase_detection/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/            # HTML templates
│   ├── base.html         # Base template with styling
│   ├── upload_files.html # Page 1: File upload
│   ├── confirm_usecase.html # Page 2: Header confirmation
│   ├── confirm_columns.html # Page 3: Column editing
│   └── process_confirmation.html # Page 4: Success page
└── uploads/              # Directory for uploaded files (auto-created)
```

## Installation

1. **Clone or download the project files**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

### Step 1: Upload Files
- Drag and drop CSV files or click "Choose Files"
- Select multiple CSV files
- Click "Process Files" to continue

### Step 2: Confirm Headers
- Review the extracted headers from your CSV files
- Edit the headers if needed
- Click "Continue to Columns" to proceed

### Step 3: Edit Columns
- View the original headers (Column A) and modified headers with random numbers (Column B)
- Edit any values in Column B as needed
- Use "Reset Changes" to revert all edits
- Click "Submit Changes" to process

### Step 4: Success
- View the success confirmation
- Check the backend console for detailed change logs
- Option to process new files

## API Endpoints

The application includes the following endpoints:

- `GET/POST /upload_files` - Handle file uploads and header extraction
- `GET/POST /confirm_usecase` - Display and confirm extracted headers
- `GET/POST /confirm_columns` - Edit headers with random numbers
- `GET /process_confirmation` - Show success page and process changes

## Backend Functions

The application includes three main backend functions as specified:

1. **`on_upload_files(files)`** - Called after files are uploaded to extract headers
2. **`on_usecase_confirmation(user_input, headers)`** - Called when user confirms headers in page 2
3. **`on_columns_confirmation(edited_columns, original_headers)`** - Called after user submits column changes

## Technical Details

- **Framework**: Flask 2.3.3
- **Data Processing**: Pandas 2.1.1
- **File Handling**: Werkzeug 2.3.7
- **Frontend**: Bootstrap 5.1.3, Font Awesome 6.0.0
- **Styling**: Custom CSS with gradient backgrounds and modern design

## Console Output

When users make changes to columns, the application prints detailed logs to the console:

```
=== USER CHANGES ===
Column 'name': 'name_123' -> 'name_modified'
Column 'email': 'email_456' -> 'email_updated'
===================
```

## Browser Compatibility

- Chrome (recommended)
- Firefox
- Safari
- Edge

## File Requirements

- Only CSV files are accepted
- Files are temporarily stored in the `uploads/` directory
- Session data is used to maintain state between pages

## Security Notes

- Files are validated for CSV format
- Filenames are sanitized using `secure_filename`
- Session data is cleared after processing

## Troubleshooting

1. **Port already in use**: Change the port in `app.py` or kill the existing process
2. **File upload issues**: Ensure files are valid CSV format
3. **Styling issues**: Check internet connection for CDN resources

## License

This project is created for educational and demonstration purposes. 