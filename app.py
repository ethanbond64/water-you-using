import base64
import re
from flask import Flask, render_template, request, url_for

app = Flask(__name__)

@app.route('/')
def camera():
    return render_template("camera.html", link=url_for('submitted'))

@app.route('/results')
def submitted():
    return "Photo submitted"

@app.route('/submitted', methods=['POST'])
def submitted():
    image_data = request.form['image']
    image_data = re.sub('^data:image/.+;base64,', '', image_data)
    image_data = base64.b64decode(image_data)

    # Save the image
    with open('captured_image.png', 'wb') as f:
        f.write(image_data)

    return "Photo submitted"

if __name__ == '__main__':
    app.run(debug=True)
