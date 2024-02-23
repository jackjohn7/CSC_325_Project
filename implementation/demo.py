from typing import NamedTuple
from friendly_splay import ConcurrentSplayTree
from threading import Thread
from random import seed, randint

NUM_THREADS: int = 20

class TestData(NamedTuple):
    key: int
    value: str
    delete_me: bool

def thread_work(kvs: list[TestData], tree: ConcurrentSplayTree):
    """
    Put the provided splay tree under load by inserting data provided, and deleting elements set to be deleted
    """
    for k, v, _ in kvs:
        tree.insert(k, v)

    for k, _, _ in filter(lambda x: x.delete_me, kvs):
        tree.delete(k)

if __name__ == "__main__":
    # create a splay tree
    tree = ConcurrentSplayTree()

    # spawn {NUM_THREADS} threads, each of which will insert strings into tree
    #  this dummy data will need to change
    threads = [Thread(target=thread_work, args=[[TestData(x, 'temp', False)], tree]) for x in range(NUM_THREADS)]
    for t in threads:
        t.start()

    # wait for each thread to finish
    for t in threads:
        t.join()

    # TODO: validate that the tree is in a valid state given our dummy data
    print(tree.find(2))

    pass
