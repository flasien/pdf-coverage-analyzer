from flask import Flask, request, jsonify, render_template
from pdf2image import convert_from_bytes
from PIL import Image
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_pdf():
    file = request.files['file']
    images = convert_from_bytes(file.read(), dpi=72)

    coverage_results = []

    for idx, img in enumerate(images):
        img = img.convert("RGB")
        pixels = img.getdata()
        total_pixels = len(pixels)

        total_ink_intensity = 0

        for r, g, b in pixels:
            # Calculamos la "intensidad de tinta" estimada: 1 - brillo promedio
            intensity = 1 - ((r + g + b) / (255 * 3))
            total_ink_intensity += intensity

        avg_ink_usage = round((total_ink_intensity / total_pixels) * 100, 2)

        # Clasificación
        if avg_ink_usage < 10:
            nivel = "Muy bajo"
        elif avg_ink_usage < 30:
            nivel = "Bajo"
        elif avg_ink_usage < 60:
            nivel = "Medio"
        elif avg_ink_usage < 90:
            nivel = "Alto"
        else:
            nivel = "Muy alto"

        coverage_results.append({
            'page': idx + 1,
            'ink_coverage_percent': avg_ink_usage,
            'nivel': nivel
        })

    return render_template('result.html', results=coverage_results)
