import os
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from library import markdown_table_generator, allowed_file

UPLOAD_FOLDER = '/tmp'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'secret'
bootstrap = Bootstrap(app)

def print_error(message):
    flash(message)
    return redirect(request.url)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
             return print_error('No file part')

        file = request.files['file']

        if file.filename == '':
            return print_error('No selected file.')

        if not allowed_file(file.filename):
            return print_error('Not allowd filetype.')

        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        return redirect(url_for('uploaded_file', excel=filename))

    return render_template('index.html')

@app.route('/uploaded_file/<excel>')
def uploaded_file(excel):
    messages = markdown_table_generator(excel)
    os.remove('/tmp/%s' % (excel))

    return render_template('markdown.html', messages=messages)

if __name__ == '__main__':
    app.run()

