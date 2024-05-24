from parameters import ROAD_WIDTH
import networkx as nx


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
        conflictCars = {}
        for car in self.carList:
            for i in range(len(car["trajectory"])):
                self.nodes[(car["index"], car["trajectory"][i])] = len(self.nodes)
                if car["trajectory"][i] not in conflictCars:
                    conflictCars[car["trajectory"][i]] = [car["index"]]
                else:
                    conflictCars[car["trajectory"][i]].append(car["index"])
                if i > 0:
                    self.edges.append(
                        (
                            self.nodes[(car["index"], car["trajectory"][i - 1])],
                            self.nodes[(car["index"], car["trajectory"][i])],
                            1,  # Type 1 edge
                        )
                    )
        for key, value in conflictCars.items():
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
        # print("Nodes: ", self.nodes)
        # print("Edges: ", self.edges)
        # print("Conflict Cars: ", conflictCars)

    def _isAcyclic(
        self,
        nodeNum: int,
        adjList: dict[int, list[int]],
        visited=None,
        recursionStack=None,
    ) -> bool:
        if visited is None:
            visited = [False] * (len(self.nodes) + 1)
        if recursionStack is None:
            recursionStack = [False] * (len(self.nodes) + 1)

        visited[nodeNum] = True
        recursionStack[nodeNum] = True

        if nodeNum in adjList:
            for neighbor in adjList[nodeNum]:
                if not visited[neighbor]:
                    if not self._isAcyclic(neighbor, adjList, visited, recursionStack):
                        return False
                elif recursionStack[neighbor]:
                    return False

        recursionStack[nodeNum] = False
        return True

    def removeCycle(self):
        type1Edges = [
            (self.edges[i][0], self.edges[i][1])
            for i in range(len(self.edges))
            if self.edges[i][2] == 1
        ]
        type3Edges = [
            (self.edges[i][0], self.edges[i][1])
            for i in range(len(self.edges))
            if self.edges[i][2] == 3 and self.edges[i][0] < self.edges[i][1]
        ]
        # We only choose one type3 edges for each pair as we will enumerate all possible combinations

        def enumerateCombinations(ind: int) -> list[list[int]]:
            if ind == len(type3Edges):
                return [[]]

            laterComb = enumerateCombinations(ind + 1)
            result = []
            for comb in laterComb:
                result.append([(type3Edges[ind][0], type3Edges[ind][1])] + comb)
                result.append([(type3Edges[ind][1], type3Edges[ind][0])] + comb)
            return result

        adjList = {}
        for edge in type1Edges:
            if edge[0] not in adjList:
                adjList[edge[0]] = [edge[1]]
            else:
                adjList[edge[0]].append(edge[1])

        enumerateResult = enumerateCombinations(0)
        # print("enumerateResult: ", enumerateResult)
        for enum in enumerateResult:
            tmpAdjList = adjList.copy()
            for edge in enum:
                if edge[0] not in tmpAdjList:
                    tmpAdjList[edge[0]] = [edge[1]]
                else:
                    tmpAdjList[edge[0]].append(edge[1])
            if self._isAcyclic(0, tmpAdjList):
                self.adjList = tmpAdjList
                print("AdjList: ", self.adjList)
                if self.isValid():
                    return True  # self.adjList
        return None

    def isValid(self):
        # Construct source conflict graph and check whether it is acyclic
        return True  # TODO: Implement this

    def schedule(self):
        for _ in range(10):
            self.constructTimingConflictGraph()
            result = self.removeCycle()
            if not result:
                continue

            # topological sort
            G = nx.DiGraph(self.adjList)
            try:
                topologicalOrder = list(nx.topological_sort(G))
                print("Topological Order: ", topologicalOrder)
            except nx.NetworkXUnfeasible:
                continue
            for i in range(len(topologicalOrder)):
                topologicalOrder[i] = list(self.nodes.keys())[topologicalOrder[i]]
            return topologicalOrder
