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
        img = img.convert("L")  # grayscale
        pixels = img.getdata()
        total_pixels = len(pixels)
        dark_pixels = sum(1 for p in pixels if p < 250)  # not white
        coverage = round((dark_pixels / total_pixels) * 100, 2)
        coverage_results.append({
            'page': idx + 1,
            'coverage_percent': coverage
        })

    return render_template('result.html', results=coverage_results)