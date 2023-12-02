# Copyright 2021, Martin Kilian
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

""" Heap based priority queue implementation.

See **Algorithms in C**, *Parts 1--4* by Robert Sedgewick for the array based
heap implementation used in this module. An alternative implementation is
provided in the :py:mod:`heapq` module.
"""

class PriorityQueue:
    """ Heap based priority queue implementation.

    Only `hashable <https://docs.python.org/3/glossary.html#term-hashable>`_
    items can be added to a priority queue. All user defined types are
    hashable. Trying to add an objects that produces the same hash value as
    an item that is already queued will update the queued item's priority
    instead of adding a duplicate with a different priority.
    """

    def __init__(self, *args):
        """ Constructor.

        Initializes an empty priority queue. By default larger values signify
        higher priority. The :py:attr:`top` element of a priority queue is the
        item of highest priority.

        Parameters
        ----------
        *args
            Variable length argument list. Add ``'minheap'`` to reverse the
            sorting of priority values.
        """
        # Internally the priority queue is modelled as a binary tree that is
        # stored in an array. heap[0] = [] is never used, it's only there
        # to simplify modulo computations when determining parent/child index.
        self._heap = [[]]
        self._hpos = dict()

        # Set heap management functions according to the chosen sorting of
        # priority values.
        if 'minheap' in args:
            self._update = self._update_minheap
            self._fixdown = self._fixdown_minheap
            self._fixup = self._fixup_minheap
        else:
            self._update = self._update_maxheap
            self._fixdown = self._fixdown_maxheap
            self._fixup = self._fixup_maxheap

    def __bool__(self):
        """ Implicit empty heap check.

        Returns
        -------
        bool
            :py:obj:`True` when there are items in the queue.
        """
        return len(self._heap) > 1

    def __contains__(self, item):
        """ Containment check.

        Parameters
        ----------
        item : object, needs to be hashable
            Query item.

        Returns
        -------
        bool
            :py:obj:`True` if ``item`` is a heap element.
        """
        return item in self._hpos

    def __len__(self):
        """ Size of queue.

        Returns
        -------
        int
            The number of queued items.
        """
        return len(self._heap)-1

    def __str__(self):
        """ String representation.

        Returns
        -------
        str
            String representation of a priority queue.
        """
        try:
            srep = f'[1: {self._heap[1]}'
        except IndexError:
            srep = '['

        for i in range(2, len(self._heap)):
            srep += f', {i}: {self._heap[i]}'

        return srep + ']'

    def __repr__(self):
        """ Object representation.

        Returns
        -------
        str
            Detailed string representation of a priority queue.
        """
        try:
            item = self._heap[1][1]
            srep = f'[[1, {self._hpos[item]}]: {self._heap[1]}'
        except IndexError:
            srep = '['

        for i in range(2, len(self._heap)):
            item = self._heap[i][1]
            srep += f', [{i}, {self._hpos[item]}]: {self._heap[i]}'

        return srep + ']'

    @property
    def top(self):
        """ Access element of highest priority.

        Raises
        ------
        IndexError
            When trying to access the top element of an empty queue.
        """
        return self._heap[1][1]

    def peek(self):
        """ Inspect top item and assigned priority.

        Returns
        -------
        item : object
            The data item of highest priority.
        priority : float
            The assigned priority.

        Raises
        ------
        IndexError
            When trying to access an empty queue.
        """
        return self._heap[1][1], self._heap[1][0]

    def pop(self):
        """ Remove item of highest priority.

        Returns
        -------
        object
            The item of highest priority.

        Raises
        ------
        IndexError
            When trying to remove items from an empty queue.
        """
        # Cannot pop an empty heap
        if len(self._heap) == 1: raise IndexError

        # Remove the top element by swapping it to the end. Then shorten
        # the list and dictionary and restore the heap property.
        self._swap(1, len(self._heap)-1)
        top = self._heap.pop()
        del self._hpos[top[1]]
        self._fixdown(1)

        # Return top element, i.e., the second entry of the (priority, item)
        # tuple data elements stored in the heap.
        return top[1]

    def push(self, item, priority):
        """ Add item to the priority queue.

        Pushing a data item already in the queue will update its priority
        instead.

        Parameters
        ----------
        item : object, needs to be hashable
            Data to be added to the priority queue.
        priority : float
            Priority of the data.

        Raises
        ------
        TypeError
            If ``item`` is not derived from a hashable data type.
        """
        if item in self._hpos:
            self._update(item, priority)
        else:
            self._hpos[item] = len(self._heap)
            self._heap.append((priority, item))
            self._fixup(len(self._heap)-1)

    def update(self, item, priority):
        """ Update priority value of an item.

        Parameters
        ----------
        item : object, needs to be hashable
            Element whose priority should be updated.
        priority : float
            New priority value.

        Raises
        ------
        KeyError
            If the given item is not an element of the queue.
        """
        self._update(item, priority)

    def _update_maxheap(self, item, priority):
        """ Update priority value of an item -- max heap version.

        Parameters
        ----------
        item : object, needs to be hashable
            Element whose priority should be updated.
        priority : float
            New priority value.

        Raises
        ------
        KeyError
            If the given item is not an element of the queue.
        """
        # This can raise a KeyError
        k = self._hpos[item]

        # Set new priority
        old_priority = self._heap[k][0]
        self._heap[k] = (priority, self._heap[k][1])

        # Restore heap property depending on new priority
        if priority > old_priority: self._fixup_maxheap(k)
        if priority < old_priority: self._fixdown_maxheap(k)

    def _update_minheap(self, item, priority):
        """ Update priority value of an item -- min heap version.

        Parameters
        ----------
        item : object, needs to be hashable
            Element whose priority should be updated.
        priority : float
            New priority value.

        Raises
        ------
        KeyError
            If the given item is not an element of the queue.
        """
        # This can raise a KeyError
        k = self._hpos[item]

        # Set new priority
        old_priority = self._heap[k][0]
        self._heap[k] = (priority, self._heap[k][1])

        # Restore heap property depending on new priority
        if priority < old_priority: self._fixup_minheap(k)
        if priority > old_priority: self._fixdown_minheap(k)

    def _swap(self, i, j):
        """ Swap position of heap items.

        Swapping two heap elements will invalidate the heap property. This
        has to be fixed by subsequent calls to either :py:meth:`_fixup` or
        :py:meth:`_fixdown`.

        Parameters
        ----------
        i : int
            Position of a heap element
        j : int
            Position of a heap element

        Raises
        ------
        IndexError
            If any of the given indices are out of bounds.
        """
        # Update position information in dictionary
        self._hpos[self._heap[i][1]] = j
        self._hpos[self._heap[j][1]] = i

        # Swap items without temporary storage
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]

    def _fixup_maxheap(self, k):
        """ Restore heap property.

        Fixes the heap property upwards starting from the item at the
        given position.

        Parameters
        ----------
        k : int
            Index of heap element that violates the heap property.
        """
        # Swap the item at position k with its predecessor as long as it's
        # of higher priority.
        while k > 1 and self._heap[k//2][0] < self._heap[k][0]:
            self._swap(k, k//2)
            k = k//2

    def _fixup_minheap(self, k):
        """ Restore heap property.

        Fixes the heap property upwards starting from the item at the
        given position.

        Parameters
        ----------
        k : int
            Index of heap element that violates the heap property.
        """
        # Swap the item at position k with its predecessor as long as it's
        # of lower priority.
        while k > 1 and self._heap[k//2][0] > self._heap[k][0]:
            self._swap(k, k//2)
            k = k//2

    def _fixdown_maxheap(self, k):
        """ Restore heap property.

        Fixes the heap property downwards starting from the item at
        the given position.

        Parameters
        ----------
        k : int
            Index of heap element that violates the heap property.
        """
        N = len(self._heap)-1

        # Swap the item at position k with its successor of higher priority
        # as long as its own priority is lower. Successors of item with
        # index k have index 2k and 2k+1.
        while 2*k <= N:
            # Index of the left child of item with index k.
            j = 2*k

            # There are two successors if j < N. Get index j of child with
            # higher priority
            if j < N and self._heap[j][0] < self._heap[j+1][0]:
                j = j+1

            # If no swap is indicated the heap property is restored.
            if self._heap[k][0] >= self._heap[j][0]:
                break

            # Swap with child of higher priority.
            self._swap(j, k)
            k = j

    def _fixdown_minheap(self, k):
        """ Restore heap property.

        Fixes the heap property downwards starting from the item at
        the given position.

        Parameters
        ----------
        k : int
            Index of heap element that violates the heap property.
        """
        N = len(self._heap)-1

        # Swap the item at position k with its successor of lower priority
        # as long as its own priority is higher. Successors of item with
        # index k have index 2k and 2k+1.
        while 2*k <= N:
            # Index of the left child of item with index k.
            j = 2*k

            # There are two successors if j < N. Get index j of child with
            # lower priority
            if j < N and self._heap[j][0] > self._heap[j+1][0]:
                j = j+1

            # If no swap is indicated the heap property is restored.
            if self._heap[k][0] <= self._heap[j][0]:
                break

            # Swap with child of lower priority, if any
            self._swap(j, k)
            k = j
