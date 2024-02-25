# Concurrency-friendly Splay Trees

This is a splay tree designed to function well in highly concurrent applications.
This is achieved through lazy splaying and lazy deletion along with partially
blocking operations.

# Testing

We wrote a test to validate the above claims about the splay tree. Threads are 
spawned with some amount of data to insert and randomly delete from the splay 
tree. After all of these operations are performed, we check that data that 
shouldn't have been deleted is still contained in the structure. If it has been 
deleted, it should not be present. We also check that the tree doesn't violate 
the definition of a Binary Search Tree. We use a preorder traversal generator
to get a list representation of the tree. We check that each element in the 
resulting list is less than the next element in the list.

There are no external dependencies. Python's standart library is sufficient.

Execute the following to run tests:
```bash
python implementation/demo.py # on windows
python3 implementation/demo.py # on unix/unix-like
```

