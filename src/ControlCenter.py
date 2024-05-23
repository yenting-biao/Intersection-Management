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
            "trajectory": list[tuple[int, int]],
        }
        """
        self.carList.append(car)

    def constructTimingConflictGraph(self):
        self.nodes = {}
        self.edges: list[tuple[int, int, int]] = []  # directed edges (src, dst, type)
        self.conflictCars = {}
        for car in self.carList:
            for i in range(len(car["trajectory"])):
                self.nodes[(car["index"], car["trajectory"][i])] = len(self.nodes)
                if car["trajectory"][i] not in self.conflictCars:
                    self.conflictCars[car["trajectory"][i]] = [car["index"]]
                else:
                    self.conflictCars[car["trajectory"][i]].append(car["index"])
                if i > 0:
                    self.edges.append(
                        (
                            self.nodes[(car["index"], car["trajectory"][i - 1])],
                            self.nodes[(car["index"], car["trajectory"][i])],
                            1,  # Type 1 edge
                        )
                    )
        for key, value in self.conflictCars.items():
            if len(value) > 1:
                for i in range(len(value)):
                    for j in range(i + 1, len(value)):
                        self.edges.append(
                            (
                                self.nodes[(value[i], key)],
                                self.nodes[(value[j], key)],
                                3,  # Type 3 edge
                            )
                        )
                        self.edges.append(
                            (
                                self.nodes[(value[j], key)],
                                self.nodes[(value[i], key)],
                                3,  # Type 3 edge
                            )
                        )
        print("Nodes: ", self.nodes)
        print("Edges: ", self.edges)
        print("Conflict Cars: ", self.conflictCars)

    def removeCycle(self):
        pass

    def constructSourceConflictGraph(self):
        pass

    def schedule(self):
        while True:
            self.constructTimingConflictGraph()
            self.removeCycle()
            result = self.constructSourceConflictGraph()
            if result:
                return result
