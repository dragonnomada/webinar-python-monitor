# Seminario Web - Estación de Monitoreo de Datos con Python

Alan Badillo Salas (dragonnomada123@gmail.com)

## Bienvenida

En este seminario web gratuito aprenderemos a construir una estación de monitoreo de datos, que nos permitirá consumir nuestros datos generados en Python desde cualquier lugar. Además aprenderemos a crear un Dashboard con gráficas y reportes para impactar a nuestra audiencia. No necesitas saber a programar ya que Python es un lenguaje muy sencillo de aprender.

## Resumen

En este seminario aprendimos:

1. Montar un Servidor de Datos
2. Construir un API de Datos
3. Crear una Interfaz
4. Consumir el API en la Interfaz
5. Crear un Dashboard
6. Generar una Gráfica
7. Generar un Reporte

## Presentación

Puedes consultar la presentación en:

https://slides.com/dragonnomada123/python-monitor

## Así quedó nuestro dashboard

![resources/sensor.png](resources/sensor.png)

## Así montamos el servidor

> app.py

``` py
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Estación de Monitoreo de Datos</h1>"

app.run()
```

## Así definimos el API de datos

``` py
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
```

## Así creamos nuestra interfaz

> templates/sensor-dep.html

``` html
<span id="temp-celcius" class="badge bg-primary">60°C</span>
<span id="temp-faren" class="badge bg-secondary">128°F</span>
<span id="temp-label" class="badge bg-success">Normal</span>
```

## Así consumimos el servidor cada sengundo

> templates/sensor-dep.html

``` js
setInterval(async () => {
    const response = await fetch("/api/sensor/temperatura");

    const data = await response.json();

    console.log(data);

    const tempCelcius = document.getElementById("temp-celcius");
    tempCelcius.textContent = `${data.celcius.toFixed(2)}°C`;

    const tempFaren = document.getElementById("temp-faren");
    tempFaren.textContent = `${data.faren.toFixed(2)}°F`;

    const tempLabel = document.getElementById("temp-label");
    tempLabel.textContent = `Estado: ${data.label}`;

    tempLabel.classList.remove("bg-success");
    tempLabel.classList.remove("bg-danger");
    tempLabel.classList.add(`bg-${data.color}`);
}, 1000);
```

## Así montamos la vista

> app.py

``` py
@app.route("/view/sensor/<id>")
def sensor_view(id):
    return render_template("sensor.html")
```

### Así cargamos el dashboard

> templates/sensor.html

``` html
{% extends "admin-lte/base.html" %}

{% block box1 %}
<div class="small-box bg-warning">
    <div class="inner">
        <h3 id="temp-celcius">0 °C</h3>

        <p>TEMPERATURA</p>
    </div>
    <div class="icon">
        <i class="fas fa-temperature-low"></i>
    </div>
    <a href="javascript:void(0)" class="small-box-footer" onclick="showTemp()">More info <i class="fas fa-arrow-circle-right"></i></a>
</div>

<script>
    let lastData = {};

    function showTemp() {
        alert(`La temperatura es ${lastData.celcius}`);
    }

    setInterval(async () => {
        const rensponse = await fetch("/api/sensor/temperatura");

        const data = await rensponse.json();

        lastData = data;

        const tempCelcius = document.getElementById("temp-celcius");

        tempCelcius.textContent = `${data.celcius.toFixed(2)}°C`;
    }, 5000);
</script>
{% endblock %}
```

## Así generamos una gráfica dinámica con Matplotlib

> app.py

``` py
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
```

## Así generamos un documento PDF con PDFKit

> app.py

``` py
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
```

# ...

## Documentación

> Documentación oficial de flask

https://flask.palletsprojects.com/en/1.1.x/

> Uso de templates

https://flask.palletsprojects.com/en/1.1.x/tutorial/templates/

> Documentación oficial de los templates de Jinja

https://jinja.palletsprojects.com/en/2.11.x/templates/

> Bootstrap - Diseño rápido y de buena calidad

https://getbootstrap.com

> Plantilla de Dashboard gratuita

https://adminlte.io

> Descargar la plantilla

https://github.com/ColorlibHQ/AdminLTE/releases/tag/v3.1.0

> Devolver una Gráfica de Matplolib con Flask

https://matplotlib.org/devdocs/gallery/user_interfaces/web_application_server_sgskip.html

> Crear un PDF desde una plantilla HTML con Flask

https://pythonprogramming.altervista.org/make-a-pdf-from-html-with-python-and-flask/

> Íconos de temperatura para el Dashboard con Fontawesome

https://fontawesome.com/icons?d=gallery&p=2&q=temp
