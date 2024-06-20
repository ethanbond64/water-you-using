import base64
import re
import threading
import json
import uuid

from dotenv import load_dotenv
from flask import Flask, render_template, request, url_for

from ai import analyze_image

load_dotenv()

data = {
    "ffe87144-eaf4-40f8-be72-3354fb81fb48": json.loads("""{\n    "Sugar": "Sugar has a moderate water footprint, requiring about 1,500 to 2,000 liters of water per kilogram produced.",\n    "Palm Oil": "Palm oil requires a relatively low amount of water compared to many other crops, but its cultivation often leads to deforestation.",\n    "Hazelnuts": "Hazelnuts have a moderate water footprint, typically consuming around 1,000 liters of water per kilogram.",\n    "Skim Milk": "Skim milk has a high water footprint, requiring about 1,000 liters of water per liter of milk produced.",\n    "Cocoa": "Cocoa is a water-intensive crop, with an estimated 20,000 liters of water needed to produce one kilogram of cocoa beans.",\n    "Lecithin": "Lecithin, often derived from soy, has a moderate water footprint, depending on the source, but is generally lower than many other ingredients.",\n    "Vanillin (an artificial flavor)": "Artificial vanillin has a relatively low water footprint compared to natural vanilla, as it is synthesized in a lab.",\n    "Ingredients less than 2%": "Ingredients used in smaller quantities generally have a minimal impact on the overall water footprint of the product.",\n    "Contains tree nuts (Hazelnuts)": "As previously mentioned, hazelnuts have a moderate water footprint, needing around 1,000 liters of water per kilogram.",\n    "Milk (as skim milk)": "Again, skim milk requires about 1,000 liters of water per liter of milk produced.",\n    "score": 90\n}""")
}

app = Flask(__name__)

def load(uuid_str):
    info = analyze_image('static/imgs/' + uuid_str + '.png')
    data[uuid_str] = info

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

    data[uuid_str] = None

    threading.Thread(target=load, args=(uuid_str,)).start()

    return render_template("loading.html", 
                           status_url=url_for('status', uuid_str=uuid_str), 
                           view_url=url_for('view', uuid_str=uuid_str))

@app.route('/status/<uuid_str>')
def status(uuid_str):
    return {'status': data.get(uuid_str, None) != None }

@app.route('/view/<uuid_str>')
def view(uuid_str):
    
    info = data.get(uuid_str, None)

    info = {k.capitalize(): v for k, v in info.items() if "%" not in k}
    score = info.pop('Score', 57)
    
    return render_template("result.html", 
                           info=info,
                           score=score,
                           image_url=url_for('static', filename='imgs/' + uuid_str + '.png'))

if __name__ == '__main__':
    app.run(debug=True)
