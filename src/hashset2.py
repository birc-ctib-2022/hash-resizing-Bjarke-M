"""Hash table implementation of a set."""

from typing import (
    Generic, Iterable, TypeVar, Iterator, NamedTuple, Any
)

T = TypeVar('T')


class HashSet(Generic[T]):
    """Set implementation using a hash table."""

    size: int
    used: int
    array: list[list[T]]

    def __init__(self, seq: Iterable[T] = (), initial_size: int = 16):
        """Create a set from a sequence, optionally with a specified size."""
        seq = list(seq)

        if 2 * len(seq) > initial_size:
            initial_size = 2 * len(seq)

        self.size = initial_size
        self.used = 0
        self.array = [list() for _ in range(initial_size)]

        for value in seq:
            self.add(value)

    def _get_bin(self, element: T) -> list[T]:
        """Get the list (bin) that element should sit in."""
        hash_val = hash(element)
        index = hash_val % self.size
        return self.array[index]

    def _resize(self, new_size: int) -> None:
        """Change the table size to new_size bins."""
        old_array = self.array
        self.size = new_size
        self.used = 0
        self.array = [list() for _ in range(new_size)]
        for b in old_array: # running through all the hashed lists in the array
            for x in b:     # running thourgh the values inside the lists
                hash_val = b[x] # saving the already hashed values and assign it
                index = hash_val%self.size # redo size 
                self.array[index][x] = hash_val # assign the value to the index
                self.used += 1 #update how many values we use 

    def add(self, element: T) -> None:
        """Add element to the set."""
        hash_val = hash(element) # hash the new element 
        index = hash_val % self.size  # find the index 
        bin = self.array[index] # find the right bin
        if element not in bin:  # check whether it is in the array  
            bin[element] = hash_val # put the value in the bin  
            self.used += 1 #update amount of vals we use 
            if self.used > self.size / 2: # make sure we have at least 1/2 the array free
                self._resize(int(2 * self.size)) # resize

    def remove(self, element: T) -> None:
        """Remove element from the set."""
        b = self._get_bin(element)  # find the element 
        if element not in b:  # check if its there at all
            raise KeyError(element)
        del b[element] # delete element if its there
        self.used -= 1 # update used 
        if self.used < self.size / 4: # resize if we use less than 25% of the entire size
            self._resize(int(self.size / 2))

    def __iter__(self) -> Iterator[T]:
        """Iterate through all the elements in the set."""
        for b in self.array:
            yield from b

    def __bool__(self) -> bool:
        """Test if the set is non-empty."""
        return self.used > 0

    def __contains__(self, element: T) -> bool:
        """Test if element is in the set."""
        return element in self._get_bin(element)

    def __repr__(self) -> str:
        """Get representation string."""
        return 'HashTableSet(' + repr(tuple(self)) + ')'
