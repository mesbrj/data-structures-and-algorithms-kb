from typing import List, Dict, Union
from dataclasses import dataclass
from pytest import fixture


@dataclass
class Vertex:
    id: Union[str, int]
    edges: List[tuple[Union[str, int], float]]
    coordinate: tuple[float, float] = (0.0, 0.0)

class Graph:
    def __init__(self):
        self.vertices: Dict[Union[str, int], int] = {}
        self.adjacency_list: List[List[tuple[Union[str, int], float]]] = []
        self.coordinates: Dict[Union[str, int], tuple[float, float]] = {}

    def add_vertex(self, vertex: Vertex) -> None:
        if vertex.id not in self.vertices.keys():
            self.vertices[vertex.id] = len(self.adjacency_list)
            self.adjacency_list.append(vertex.edges)
            self.coordinates[vertex.id] = vertex.coordinate

    def remove_vertex(self, vertex_id: Union[str, int]) -> None:
        if vertex_id in self.vertices.keys():
            adjacency_list_index = self.vertices[vertex_id]
            del self.adjacency_list[adjacency_list_index]
            del self.coordinates[vertex_id]
            del self.vertices[vertex_id]
            for v_id, v_index in self.vertices.items():
                if v_index > adjacency_list_index:
                    self.vertices[v_id] = v_index - 1
            for edges in self.adjacency_list:
                edges[:] = [edge for edge in edges if edge[0] != vertex_id]

    def update_edges(self, vertex_id: Union[str, int], updated_edges: List[tuple[Union[str, int], float]]) -> None:
        if vertex_id in self.vertices.keys():
            index = self.vertices[vertex_id]
            current_edges_id = [e[0] for e in self.adjacency_list[index]]
            for i, edge in enumerate(updated_edges):
                if edge[0] not in current_edges_id:
                    self.adjacency_list[index].append(edge)
                else:
                    for j, existing_edge in enumerate(self.adjacency_list[index]):
                        if updated_edges[i][0] == existing_edge[0] and updated_edges[i][1] != existing_edge[1]:
                            self.adjacency_list[index][j] = updated_edges[i]

    def remove_edges(self, vertex_id: Union[str, int], edge_vertex_id: List[Union[str, int]]) -> None:
        if vertex_id in self.vertices.keys():
            index = self.vertices[vertex_id]
            self.adjacency_list[index] = [
                edge for edge in self.adjacency_list[index] if edge[0] not in edge_vertex_id
            ]

    def adjacent_vertices(self, vertex: Union[str, int]) -> List[tuple[Union[str, int], float]]:
        if vertex in self.vertices.keys():
            return self.adjacency_list[
                self.vertices[vertex]
            ]


@fixture
def sample_weighted_dag() -> Graph:
    graph = Graph()
    graph.add_vertex(Vertex('A', [('B', 1), ('C', 1.5)], (1, 3)))
    graph.add_vertex(Vertex('B', [('A', 1), ('D', 3)], (12, 17)))
    graph.add_vertex(Vertex('C', [('A', 1.5)], (35, 25)))
    graph.add_vertex(Vertex('D', [('B', 3)], (49, 36)))
    return graph

def test_coordinates(sample_weighted_dag: Graph) -> None:
    sample_weighted_dag.add_vertex(Vertex('Z', []))
    assert sample_weighted_dag.coordinates == {
        'A': (1, 3),
        'B': (12, 17),
        'C': (35, 25),
        'D': (49, 36),
        'Z': (0.0, 0.0)
    }

def test_add_vertex() -> None:
    graph = Graph()
    graph.add_vertex(Vertex('X', [('Y', 2)]))
    assert graph.vertices == {'X': 0}
    assert graph.adjacency_list == [[('Y', 2)]]
    graph.add_vertex(Vertex('Y', [('X', 2), ('Z', 4)]))
    assert graph.vertices == {'X': 0, 'Y': 1}
    assert graph.adjacency_list == [[('Y', 2)], [('X', 2), ('Z', 4)]]
    graph.add_vertex(Vertex('BB', []))
    graph.add_vertex(Vertex('AA', [], (100, 250)))
    assert graph.vertices == {'X': 0, 'Y': 1, 'BB': 2, 'AA': 3}
    assert graph.adjacency_list == [[('Y', 2)], [('X', 2), ('Z', 4)], [], []]

def test_remove_vertex(sample_weighted_dag: Graph) -> None:
    assert sample_weighted_dag.vertices == {'A': 0, 'B': 1, 'C': 2, 'D': 3}
    assert sample_weighted_dag.adjacency_list == [[('B', 1), ('C', 1.5)], [('A', 1), ('D', 3)], [('A', 1.5)], [('B', 3)]]    
    sample_weighted_dag.add_vertex(Vertex('X', [('Y', 2)]))
    sample_weighted_dag.remove_vertex('C')
    assert sample_weighted_dag.vertices == {'A': 0, 'B': 1, 'D': 2, 'X': 3}
    assert sample_weighted_dag.adjacency_list == [[('B', 1)], [('A', 1), ('D', 3)], [('B', 3)], [('Y', 2)]]
    sample_weighted_dag.remove_vertex('A')
    assert sample_weighted_dag.vertices == {'B': 0, 'D': 1, 'X': 2}
    assert sample_weighted_dag.adjacency_list == [[('D', 3)], [('B', 3)], [('Y', 2)]]
    sample_weighted_dag.remove_vertex('D')
    assert sample_weighted_dag.vertices == {'B': 0, 'X': 1}
    assert sample_weighted_dag.adjacency_list == [[], [('Y', 2)]]
    sample_weighted_dag.add_vertex(Vertex('Y', [('X', 2.8)]))
    sample_weighted_dag.remove_vertex('B')
    assert sample_weighted_dag.vertices == {'X': 0, 'Y': 1} 
    assert sample_weighted_dag.adjacency_list == [[('Y', 2)], [('X', 2.8)]]

def test_adjacent_vertices(sample_weighted_dag: Graph) -> None:
    assert sample_weighted_dag.adjacent_vertices('A') == [('B', 1), ('C', 1.5)]
    assert sample_weighted_dag.adjacent_vertices('B') == [('A', 1), ('D', 3)]
    assert sample_weighted_dag.adjacent_vertices('C') == [('A', 1.5)]
    assert sample_weighted_dag.adjacent_vertices('D') == [('B', 3)]
    assert sample_weighted_dag.adjacent_vertices('E') == None

def test_update_edges(sample_weighted_dag: Graph) -> None:
    sample_weighted_dag.update_edges('A', [('B', 2), ('C', 1.5)])
    assert sample_weighted_dag.adjacent_vertices('A') == [('B', 2), ('C', 1.5)]
    sample_weighted_dag.update_edges('B', [('A', 1), ('D', 4), ('C', 5)])
    assert sample_weighted_dag.adjacent_vertices('B') == [('A', 1), ('D', 4), ('C', 5)]
    sample_weighted_dag.update_edges('C', [('A', 1.5), ('B', 3.5)])
    assert sample_weighted_dag.adjacent_vertices('C') == [('A', 1.5), ('B', 3.5)]

def test_remove_edges(sample_weighted_dag: Graph) -> None:
    sample_weighted_dag.remove_edges('A', ['B'])
    assert sample_weighted_dag.adjacent_vertices('A') == [('C', 1.5)]
    sample_weighted_dag.remove_edges('B', ['A'])
    assert sample_weighted_dag.adjacent_vertices('B') == [('D', 3)]
    sample_weighted_dag.remove_edges('C', ['A'])
    assert sample_weighted_dag.adjacent_vertices('C') == []
    sample_weighted_dag.add_vertex(Vertex('Z', [('X', 7), ('Y', 2), ('C', 5)]))
    sample_weighted_dag.add_vertex(Vertex('X', [('Y', 3)]))
    sample_weighted_dag.add_vertex(Vertex('Y', [('X', 4)]))
    assert sample_weighted_dag.adjacent_vertices('Z') == [('X', 7), ('Y', 2), ('C', 5)]
    sample_weighted_dag.remove_edges('Z', ['X', 'C'])
    assert sample_weighted_dag.adjacent_vertices('Z') == [('Y', 2)]
