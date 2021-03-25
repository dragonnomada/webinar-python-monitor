from flask import Flask, render_template

app = Flask(__name__, static_url_path='/view/sensor', static_folder='templates/admin-lte')

@app.route("/")
def home():
    return "<h1>Hola mundo</h1>"

import matplotlib.pyplot as plt
from io import BytesIO
import base64
import numpy as np

@app.route("/graphics/sensor/<id>")
def sensor_plot(id):
    fig = plt.Figure()
    ax = fig.subplots()
    x = np.linspace(0, 10, 20)
    y = np.sin(x) + np.random.uniform(-1, 1, 20) * 5
    ax.plot(x, y, "r+-")
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"

from flask import make_response
import pdfkit 
 
@app.route("/pdf/sensor/<id>")
def sensor_pdf(id):
    html = render_template(
        "sensor_pdf.html",
        celcius=60.5)
    pdf = pdfkit.from_string(html, False)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=output.pdf"
    return response

# /api/sensor/temperatura
# /api/sensor/humedad
# /api/sensor/123
# /api/sensor/...
@app.route("/api/sensor/<id>")
def sensor(id):
    from random import uniform

    celcius = uniform(0, 90)

    # TODO: Recupera los datos del sensor <id>
    return {
        "celcius": celcius,
        "faren": 9 / 5. * celcius + 32,
        "label": "Normal" if celcius < 30 else "Alta",
        "color": "success" if celcius < 30 else "danger"
    }

@app.route("/view/sensor/<id>")
def sensor_view(id):
    return render_template("sensor.html")

app.run()