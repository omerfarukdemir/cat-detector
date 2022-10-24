import base64
from io import BytesIO
from typing import List

from PIL import Image
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from detection import Detection
from detector import Detector

load_dotenv()

app = FastAPI()

detector = Detector({'cat'})


class Request(BaseModel):
    image: str


@app.post("/detect")
def detect(request: Request):
    image_bytes: BytesIO = BytesIO(base64.b64decode(request.image))

    image: Image = Image.open(image_bytes)

    detections: List[Detection] = detector.detect(image)

    return detections
