from random import randrange
from typing import List, Tuple, Union
from pytest import fixture

def bubble_sort(arr: List[int]) -> List[int]:
	swapped = False
	for i in range(len(arr) - 1):
		if arr[i] > arr[i+1]:
			arr[i], arr[i+1] = arr[i+1], arr[i]
			swapped = True
	return arr if not swapped else bubble_sort(arr)

def quick_sort(arr: List[int]) -> List[int]:
	if len(arr) < 2:
		return arr
	pivot = arr.pop(randrange(len(arr) - 1))
	return [
		*quick_sort([x for x in arr if x <= pivot]),
		pivot,
		*quick_sort([x for x in arr if x > pivot]),
	]

def merge_sort(arr: List[int]):
	if len(arr) > 1:
		mid = len(arr) // 2
		left = arr[:mid]
		right = arr[mid:]
		merge_sort(left)
		merge_sort(right)
		i = j = k = 0
		while(
			i < len(left)
			and j < len(right)
		):
			if left[i] < right[j]:
				arr[k] = left[i]
				i += 1
			else:
				arr[k] = right[j]
				j += 1
			k += 1
		while i < len(left):
			arr[k] = left[i]
			i += 1
			k += 1
		while j < len(right):
			arr[k] = right[j]
			j += 1
			k += 1

def binary_search(arr: List[int], item: int) -> Tuple[bool, Union[int, None]]:
	if len(arr) == 0:
		return False, None
	mid = len(arr) // 2
	if arr[mid] == item:
		return True, mid
	if item < arr[mid]:
		return binary_search(arr[:mid], item)
	else:
		return binary_search(arr[mid + 1:], item)


unsorted_list_list = [64, 34, 25, 0, 258, -54, 12, 22, 11, 90, 11, -21]

@fixture
def unsorted_list():
	return unsorted_list_list.copy()

@fixture
def sorted_list():
	test_list = unsorted_list_list.copy()
	merge_sort(test_list)
	return test_list


def test_bubble_sort(unsorted_list: List[int]):
	assert sorted(unsorted_list) == bubble_sort(unsorted_list)

def test_quick_sort(unsorted_list: List[int]):
	assert sorted(unsorted_list) == quick_sort(unsorted_list)

def test_merge_sort(unsorted_list: List[int]):
	expected_sorted_list = sorted(unsorted_list)
	merge_sort(unsorted_list)
	assert unsorted_list == expected_sorted_list

def test_binary_search(sorted_list: List[int]):
	assert True == binary_search(sorted_list, 11)[0]
	assert 1 == binary_search(sorted_list, -21)[1]
	assert False == binary_search(sorted_list, 3)[0]
	assert None == binary_search(sorted_list, 3)[1]


