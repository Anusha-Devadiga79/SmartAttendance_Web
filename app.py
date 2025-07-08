from flask import Flask, render_template, request, redirect, session, url_for
import subprocess
import gspread
import os, json, base64
from google.oauth2.service_account import Credentials
from datetime import datetime
from werkzeug.middleware.proxy_fix import ProxyFix
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

app = Flask(__name__)
app.secret_key = 'secret_key'

# 🔥 Increase request size limit to 16MB (you can adjust this)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Google Sheets setup
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
creds_b64 = os.environ['GOOGLE_CREDS_B64']
creds_json = base64.b64decode(creds_b64).decode('utf-8')
credentials = Credentials.from_service_account_info(json.loads(creds_json), scopes=SCOPES)
gc = gspread.authorize(credentials)
spreadsheet = gc.open_by_key('1j5cxov8g0jl4Ou6M2ehzcwA-MPBXO8pn85nHTCHFqAg')
sheet = spreadsheet.worksheet("Attendance")

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'bcca' and request.form['password'] == 'bcca':
            session['user'] = 'admin'
            return redirect('/dashboard')
        else:
            return render_template('index.html', error='Invalid Credentials')
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    return render_template('dashboard.html')

@app.route('/view_data')
def view_data():
    if 'user' not in session:
        return redirect('/')
    records = sheet.get_all_values()
    return render_template('view_data.html', records=records)

@app.route('/shortage')
def shortage():
    if 'user' not in session:
        return redirect('/')
    records = sheet.get_all_values()
    headers = records[0][1:]  # Exclude 'Name'
    result = []
    for row in records[1:]:
        present_count = row[1:].count('Present')
        if present_count < len(headers) * 0.75:
            result.append([row[0], present_count, len(headers)])
    return render_template('shortage.html', result=result)

@app.route('/absentees_today')
def absentees_today():
    if 'user' not in session:
        return redirect('/')
    today = datetime.now().strftime('%Y-%m-%d')
    records = sheet.get_all_records()
    absentees = [r['Name'] for r in records if r.get(today) == 'Absent']
    return render_template('absentees.html', absentees=absentees, date=today)

@app.route('/run_attendance')
def run_attendance():
    if 'user' not in session:
        return redirect('/')
    subprocess.Popen(["python", "chat.py", "--manual"])
    return render_template('dashboard.html', msg="Manual attendance started.")
    
def upload_to_drive(file_path, file_name, folder_id):
    creds = Credentials.from_service_account_info(json.loads(creds_json), scopes=SCOPES)
    drive_service = build('drive', 'v3', credentials=creds)
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path, mimetype='image/png')

    uploaded = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    return uploaded.get('id')

@app.route('/add-student', methods=['GET', 'POST'])
def add_student():
    if 'user' not in session:
        return redirect('/')

    if request.method == 'POST':
        name = request.form['name']
        photo_data = request.form['photo']

        if photo_data:
            try:
                header, encoded = photo_data.split(",", 1)
                image_bytes = base64.b64decode(encoded)

                filename = f"{name}.png"
                os.makedirs("data", exist_ok=True)
                local_path = os.path.join("data", filename)
                with open(local_path, "wb") as f:
                    f.write(image_bytes)

                if os.path.exists("SmartAttendanceWeb"):
                    os.makedirs(os.path.join("SmartAttendanceWeb", "data"), exist_ok=True)
                    git_path = os.path.join("SmartAttendanceWeb", "data", filename)
                    with open(git_path, "wb") as f:
                        f.write(image_bytes)

                try:
                    upload_to_drive(local_path, filename, '146S39x63_ycnNpv9vgtLOE18cx-54ghG')
                except Exception as e:
                    print("Drive upload failed:", e)

            except Exception as e:
                print("Image processing error:", e)
                return "Invalid image data", 400

        try:
            existing_data = sheet.get_all_values()
            new_row = [name] + ['' for _ in range(len(existing_data[0]) - 1)]
            sheet.append_row(new_row)
        except Exception as e:
            print("Google Sheet append error:", e)
            return "Sheet update failed", 500

        return render_template('dashboard.html', msg="Student added and photo uploaded successfully.")

    return render_template('add_student.html')
    
@app.route('/remove-student', methods=['GET', 'POST'])
def remove_student():
    if 'user' not in session:
        return redirect('/')
    student_names = [row[0] for row in sheet.get_all_values()[1:]]
    if request.method == 'POST':
        name_to_remove = request.form['name']
        records = sheet.get_all_values()
        for idx, row in enumerate(records):
            if row[0] == name_to_remove:
                sheet.delete_rows(idx + 1)
                break
        return redirect('/dashboard')
    return render_template('remove_student.html', students=student_names)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
