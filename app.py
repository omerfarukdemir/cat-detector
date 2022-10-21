import json
from typing import List

from PIL import Image
from dotenv import load_dotenv
from flask import Flask, request, abort, Response
from werkzeug.datastructures import FileStorage

from detector import Detector
from detection import Detection


load_dotenv()

app = Flask(__name__)

detector = Detector({'cat'})


@app.route('/detect', methods=['POST'])
def detect():
    if request.method == 'POST':
        file: FileStorage = request.files.get('image')

        image: Image = Image.open(file)

        detections: List[Detection] = detector.detect(image)

        response = json.dumps([detection.__dict__ for detection in detections])

        return Response(response=response, mimetype='application/json')

    abort(404)
