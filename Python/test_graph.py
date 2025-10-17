from typing import List, Dict, Union
from dataclasses import dataclass
from pytest import fixture


@dataclass
class Vertex:
    id: Union[str, int]
    edges: List[tuple[Union[str, int], float]]

class Graph:
    def __init__(self):
        self.vertices: Dict[Union[str, int], int] = {}
        self.adjacency_list: List[List[tuple[Union[str, int], float]]] = []

    def add_vertex(self, vertex: Vertex) -> None:
        if vertex.id not in self.vertices.keys():
            self.vertices[vertex.id] = len(self.adjacency_list)
            self.adjacency_list.append(vertex.edges)

    def adjacent_vertices(self, vertex: Union[str, int]) -> List[tuple[Union[str, int], float]]:
        if vertex in self.vertices.keys():
            return self.adjacency_list[
                self.vertices[vertex]
            ]


@fixture
def sample_weighted_dag() -> Graph:
    graph = Graph()
    graph.add_vertex(Vertex('A', [('B', 1), ('C', 1.5)]))
    graph.add_vertex(Vertex('B', [('A', 1), ('D', 3)]))
    graph.add_vertex(Vertex('C', [('A', 1.5)]))
    graph.add_vertex(Vertex('D', [('B', 3)]))
    return graph

def test_add_vertex() -> None:
    graph = Graph()

    graph.add_vertex(Vertex('X', [('Y', 2)]))
    assert graph.vertices == {'X': 0}
    assert graph.adjacency_list == [[('Y', 2)]]
    graph.add_vertex(Vertex('Y', [('X', 2), ('Z', 4)]))
    assert graph.vertices == {'X': 0, 'Y': 1}
    assert graph.adjacency_list == [[('Y', 2)], [('X', 2), ('Z', 4)]]

def test_adjacent_vertices(sample_weighted_dag: Graph) -> None:

    assert sample_weighted_dag.adjacent_vertices('A') == [('B', 1), ('C', 1.5)]
    assert sample_weighted_dag.adjacent_vertices('B') == [('A', 1), ('D', 3)]
    assert sample_weighted_dag.adjacent_vertices('C') == [('A', 1.5)]
    assert sample_weighted_dag.adjacent_vertices('D') == [('B', 3)]
    assert sample_weighted_dag.adjacent_vertices('E') == None