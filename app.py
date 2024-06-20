import base64
import os
import re
import threading
import time
import uuid

from dotenv import load_dotenv
from flask import Flask, render_template, request, url_for
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),)

data = {}

app = Flask(__name__)

def load(uuid_str):
    time.sleep(5)
    data[uuid_str] = True

@app.route('/')
def camera():
    return render_template("camera.html", submit_url=url_for('submit'))

@app.route('/submit', methods=['POST'])
def submit():
    image_data = request.form['image']
    image_data = re.sub('^data:image/.+;base64,', '', image_data)
    image_data = base64.b64decode(image_data)

    uuid_str = str(uuid.uuid4())
    with open('static/imgs/' + uuid_str + '.png', 'wb') as f:
        f.write(image_data)

    data[uuid_str] = False

    threading.Thread(target=load, args=(uuid_str,)).start()

    return render_template("loading.html", 
                           status_url=url_for('status', uuid_str=uuid_str), 
                           view_url=url_for('view', uuid_str=uuid_str))

@app.route('/status/<uuid_str>')
def status(uuid_str):
    return {'status': data.get(uuid_str, False)}

@app.route('/view/<uuid_str>')
def view(uuid_str):
    return render_template("view.html", 
                           image_url=url_for('static', filename='imgs/' + uuid_str + '.png'))

if __name__ == '__main__':
    app.run(debug=True)
