from parameters import ROAD_WIDTH


class ControlCenter:
    def __init__(self, center: tuple[int, int]):
        self.carList = []
        self.center = center
        self.width = ROAD_WIDTH

    def addCar(self, car):
        """
        car: {
            "index": int,
            "sourceDir": int,
                # 0 for up, 1 for right, 2 for down, 3 for left
            "trajectory": list[tuple[int, int]],
        }
        """
        self.carList.append(car)

    def constructTimingConflictGraph(self):
        self.nodes = {}
        self.edges = []
        for car in self.carList:
            for i in range(car["trajectory"]):
                self.nodes[(car["index"], car["trajectory"][i])] = len(self.nodes)
                if i < len(car["trajectory"]) - 1:
                    self.edges.append(
                        (
                            self.nodes[(car["index"], car["trajectory"][i])],
                            self.nodes[(car["index"], car["trajectory"][i + 1])],
                        )
                    )

    def constructSourceConflictGraph(self):
        pass

    def removeCycle(self):
        pass

    def schedule(self):
        pass
