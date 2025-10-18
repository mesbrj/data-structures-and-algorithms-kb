from typing import Union, Any
from dataclasses import dataclass
from pytest import fixture

@dataclass
class LinkedListNode:
    value: Any
    next: Union['LinkedListNode', None] = None

class LIFOQueue:
    def __init__(self):
        self.top: Union[LinkedListNode, None] = None
        self.size: int = 0

    def push(self, value: Any) -> None:
        new_node = LinkedListNode(value, self.top)
        self.top = new_node
        self.size += 1

    def pop(self) -> Any:
        if self.top is not None:
            value = self.top.value
            self.top = self.top.next
            self.size -= 1
            return value

    def seek(self) -> Union[Any, None]:
        if self.top is not None:
            return self.top.value
        return None

    def stack_size(self) -> int:
        return self.size


@fixture
def sample_stack() -> LIFOQueue:
    stack = LIFOQueue()
    stack.push(1)
    stack.push(2)
    stack.push(3)
    return stack

def test_lifo_push_and_seek(sample_stack: LIFOQueue) -> None:
    sample_stack.push(4)
    assert sample_stack.seek() == 4

def test_lifo_pop_and_size(sample_stack: LIFOQueue) -> None:
    assert sample_stack.pop() == 3
    assert sample_stack.stack_size() == 2
    assert sample_stack.pop() == 2
    assert sample_stack.stack_size() == 1
    assert sample_stack.pop() == 1
    assert sample_stack.stack_size() == 0
    assert sample_stack.pop() is None