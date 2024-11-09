from flask import Flask, request, jsonify
import easyocr

app = Flask(__name__)
reader = easyocr.Reader(['en'])  # You can add more languages as needed

@app.route('/ocr', methods=['POST'])
def ocr():
    file = request.files['image']
    image_path = "temp_image.jpg"
    file.save(image_path)

    result = reader.readtext(image_path)
    text = " ".join([res[1] for res in result])

    return jsonify({"text": text})

if __name__ == '__main__':
    app.run(port=5000)
