import base64
import time
from io import BytesIO
from typing import List

from PIL import Image
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from pydantic import BaseModel

from detection import Detection
from detector import Detector

load_dotenv()

app = FastAPI()

detector = Detector({'cat'})


class DetectRequest(BaseModel):
    image: str


@app.middleware('http')
async def request_time(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    response.headers["x-request-time"] = str(round(time.time() - start_time, 3))

    return response


@app.post('/detect')
def detect(request: DetectRequest):
    image_bytes: BytesIO = BytesIO(base64.b64decode(request.image))

    image: Image = Image.open(image_bytes)

    detections: List[Detection] = detector.detect(image)

    return detections
