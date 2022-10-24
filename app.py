import json
from typing import List, Optional

from PIL import Image
from dotenv import load_dotenv
from flask import Flask, request, Response
from werkzeug.datastructures import FileStorage

from detector import Detector
from detection import Detection

load_dotenv()

app = Flask(__name__)

detector = Detector({'cat'})


@app.route('/detect', methods=['POST'])
def detect():
    # TODO: get file as numpy.ndarray or base64
    file: Optional[FileStorage] = request.files.get('image')

    if file is None:
        return Response(status=400)

    image: Image = Image.open(file)

    detections: List[Detection] = detector.detect(image)

    response = json.dumps([detection.__dict__ for detection in detections])

    return Response(status=200, response=response, mimetype='application/json')
