import threading
import time
import webbrowser
from flask import Flask, render_template_string, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import pyperclip
from extractor import extract_text_from_image
from gpt_query import query_gpt
from database import save_to_database, init_db

UPLOAD_FOLDER = 'uploaded_images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            absolute_filepath = os.path.abspath(filepath)
            file.save(absolute_filepath)
            threading.Thread(target=process_and_restart_server, args=(absolute_filepath,)).start()
            shutdown_server()
            return 'Image uploaded successfully. Processing...'

    return '''
    <!doctype html>
    <title>Upload an Image</title>
    <h1>Upload an Image</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

def run_flask_app():
    app.run(debug=False, use_reloader=False)

def process_and_restart_server(image_path):
    # 이미지 처리
    process_image(image_path)

    # 결과를 보여주는 새로운 서버 실행
    run_result_server()

def process_image(image_path):
    # 데이터베이스 초기화
    init_db()

    global extracted_text

    # Mathpix에서 텍스트를 추출
    extracted_text = extract_text_from_image(image_path)

    print("Extracted Text from Mathpix:")
    print(extracted_text)

    # 클립보드에 텍스트 저장
    pyperclip.copy(extracted_text)
    print("Extracted text has been copied to clipboard.")

    # GPT로 텍스트 전달 및 응답 받기
    global gpt_result
    gpt_result = query_gpt()

    print("GPT Result:")
    print(gpt_result)

    # 추출된 텍스트, 이미지 경로 및 GPT 응답을 데이터베이스에 저장
    save_to_database(image_path, extracted_text, gpt_result)

def run_result_server():
    result_app = Flask(__name__)

    @result_app.route('/result')
    def index():
        # HTML 결과 페이지 생성
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Result Page</title>
            <script id="MathJax-script" async
                    src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
            </script>
        </head>
        <body>
            <h1>Extracted Text</h1>
            <p>{extracted_text}</p>
            <h2>GPT Result</h2>
            <p id="gpt-result">{gpt_result}</p>
            <script type="text/javascript">
                document.addEventListener("DOMContentLoaded", function() {{
                    MathJax.typeset();
                }});
            </script>
        </body>
        </html>
        """
        return render_template_string(html_content)

    # 결과 서버를 별도의 스레드에서 실행
    threading.Thread(target=result_app.run, kwargs={'debug': False, 'use_reloader': False, 'port': 5001}).start()

    time.sleep(2)

    # 결과 페이지를 새로운 경로로 엽니다.
    webbrowser.open("http://127.0.0.1:5001/result")

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.start()

    time.sleep(2)

    webbrowser.open("http://127.0.0.1:5000")

    flask_thread.join()
