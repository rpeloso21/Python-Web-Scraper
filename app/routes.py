import os
from flask import Blueprint, request, render_template, send_file
from werkzeug.utils import secure_filename
from .scraper import scrape_links

main = Blueprint('main', __name__)
 

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')
        keywords = request.form.get('keywords')

        if file and keywords:
            filename = secure_filename(file.filename)
            filepath = os.path.join('uploads', filename)
            file.save(filepath)

            result_file = scrape_links(filepath, keywords.split(','))

            return send_file(result_file, as_attachment=True)
        
    return render_template('index.html')

