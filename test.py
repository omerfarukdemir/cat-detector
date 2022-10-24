import os
from typing import List, Optional

from PIL import Image
from dotenv import load_dotenv
from matplotlib import pyplot
from matplotlib.patches import Rectangle

from detector import Detector
from detection import Detection


def draw(file_path: str, detections: List[Detection]):
    data = pyplot.imread(file_path)

    dpi = 80.0

    height, width, _ = data.shape

    figure_size = width / dpi, height / dpi

    figure = pyplot.figure(figsize=figure_size)

    axes = figure.add_axes([0, 0, 1, 1])
    axes.axis('off')
    axes.imshow(data)
    axes = pyplot.gca()

    for detection in detections:
        rectangle = Rectangle(
            (detection.x_min, detection.y_min),
            detection.width(),
            detection.height(),
            fill=False,
            color='red',
            linewidth=20
        )

        axes.add_patch(rectangle)

        info = f'{detection.label.upper()} [{detection.score}]'

        pyplot.text(detection.x_min, detection.y_min - 20, info, color='red', fontdict={'size': 100})

    file_name = file_path.split('/')[-1]

    pyplot.savefig(f'image/result.{file_name}', bbox_inches='tight', pad_inches=0)


load_dotenv()

test_image_path: Optional[str] = os.getenv('TEST_IMAGE_PATH')

if not test_image_path:
    exit('Could not find TEST_IMAGE_PATH')

image = Image.open(test_image_path)

detector: Detector = Detector({'cat'})

detections: List[Detection] = detector.detect(image)

draw(test_image_path, detections)
