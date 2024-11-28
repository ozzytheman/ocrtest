from flask import Flask, request, jsonify
import easyocr
import logging
from flask_cors import CORS


app = Flask(__name__)

CORS(app)  # Enable CORS for all routes

# Initialize EasyOCR reader with English language
reader = easyocr.Reader(['en'])

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/ocr', methods=['POST'])
def ocr():
    logging.info("Received a request")

    # Check if an image is included in the request
    if 'image' not in request.files:
        logging.error("No image file found in the request")
        return jsonify({"error": "No image file provided"}), 400

    # Save the image locally
    file = request.files['image']
    image_path = "temp_image.jpg"
    file.save(image_path)
    logging.info(f"Image saved to {image_path}")

    # Perform OCR on the image
    try:
        result = reader.readtext(image_path)
        text = " ".join([res[1] for res in result])
        logging.info(f"OCR Result: {text}")
        return jsonify({"text": text})
    except Exception as e:
        logging.error(f"Error during OCR processing: {e}")
        return jsonify({"error": "OCR processing failed"}), 500

if __name__ == '__main__':
    logging.info("Starting Flask server on http://localhost:5000")
    app.run(port=5000)
