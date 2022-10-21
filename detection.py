class Detection:
    def __init__(self, label: str, score: float, x_min: int, y_min: int, x_max: int, y_max: int) -> None:
        self.label: str = label
        self.score: float = round(float(score), 2)
        self.x_min: int = x_min
        self.y_min: int = y_min
        self.x_max: int = x_max
        self.y_max: int = y_max

    def width(self) -> int:
        return self.x_max - self.x_min

    def height(self) -> int:
        return self.y_max - self.y_min

    def area(self) -> int:
        return self.width() * self.height()

    def x_range(self) -> range:
        return range(self.x_min, self.x_max)

    def y_range(self) -> range:
        return range(self.y_min, self.y_max)

    def intersection_area(self, other) -> int:
        x_intersection = Detection.overlapping_length(self.x_range(), other.x_range())
        y_intersection = Detection.overlapping_length(self.y_range(), other.y_range())

        return x_intersection * y_intersection

    def intersection_percentage(self, other) -> float:
        intersection_area = self.intersection_area(other)
        total_area = self.area() + other.area() - intersection_area

        return intersection_area / float(total_area)

    @staticmethod
    def overlapping_length(range1: range, range2: range) -> int:
        if range2.stop < range1.start or range1.stop < range2.start:
            return 0

        return min(range1.stop, range2.stop) - max(range2.start, range1.start)
