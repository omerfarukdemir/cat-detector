import itertools
import os
from typing import List, Dict, Set, Optional
import numpy
from PIL import Image
from keras.utils import img_to_array
from keras.models import load_model
from tensorflow import sigmoid

from constant import WIDTH, HEIGHT, ANCHORS, THRESHOLD, INDEX_LABEL_DICT, INTERSECTION_THRESHOLD
from detection import Detection


class Detector:
    def __init__(self, labels: Set[str]) -> None:
        super().__init__()

        self.index_label_dict: Dict[int, str] = {}

        for index, label in INDEX_LABEL_DICT.items():
            if label in labels:
                self.index_label_dict[index] = label

        model_path: Optional[str] = os.getenv('MODEL_PATH')

        if not model_path:
            exit('Could not find MODEL_PATH')

        self.model = load_model(model_path)

    def detect(self, image: Image) -> List[Detection]:
        width, height = image.size

        image: numpy.ndarray = self.adjust_image(image)

        model_outputs: List[numpy.ndarray] = self.model.predict(image)

        detections: List[Detection] = self.decode(model_outputs, width, height)
        detections: List[Detection] = self.filter_overlapping_detections(detections)

        return detections

    def decode(self, model_outputs: List[numpy.ndarray], width: int, height: int) -> List[Detection]:
        detections: List[Detection] = []

        nb_box = 3

        for model_putput, anchors in zip(model_outputs, ANCHORS):
            result = model_putput[0]

            grid_height, grid_width = result.shape[:2]

            result: numpy.ndarray = result.reshape((grid_height, grid_width, nb_box, -1))
            result[..., :2] = sigmoid(result[..., :2])
            result[..., 4:] = sigmoid(result[..., 4:])
            result[..., 5:] = result[..., 4][..., numpy.newaxis] * result[..., 5:]

            for row, column in itertools.product(range(grid_height), range(grid_width)):
                for b in range(nb_box):
                    scores: List[float] = result[int(row)][column][b][5:]
                    for index, score in enumerate(scores):
                        label: Optional[str] = self.index_label_dict.get(index)
                        if label is not None and score > THRESHOLD:
                            x, y, w, h = result[int(row)][int(column)][b][:4]

                            x = (column + x) / grid_width
                            y = (row + y) / grid_height

                            w = anchors[2 * b + 0] * numpy.exp(w) / WIDTH
                            h = anchors[2 * b + 1] * numpy.exp(h) / HEIGHT

                            x_min = int((x - w / 2) * width)
                            y_min = int((y - h / 2) * height)
                            x_max = int((x + w / 2) * width)
                            y_max = int((y + h / 2) * height)

                            detections.append(Detection(label, score, x_min, y_min, x_max, y_max))

        return detections

    @staticmethod
    def filter_overlapping_detections(detections: List[Detection]) -> List[Detection]:
        detections.sort(key=lambda d: d.score, reverse=True)

        for index, detection in enumerate(detections):
            for x in range(index + 1, len(detections)):
                other: Detection = detections[x]
                if detection.label == other.label:
                    if detection.intersection_percentage(other) >= INTERSECTION_THRESHOLD:
                        other.score = 0

        return [detection for detection in detections if detection.score > 0]

    @staticmethod
    def adjust_image(image: Image) -> numpy.ndarray:
        image: Image = image.resize((WIDTH, HEIGHT))
        image: numpy.ndarray = img_to_array(image)
        image = image.astype('float32')
        image /= 255.0
        image = numpy.expand_dims(image, 0)

        return image
