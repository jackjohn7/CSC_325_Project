from typing import NamedTuple
from friendly_splay import ConcurrentSplayTree
from threading import Thread
from random import seed, randint

NUM_THREADS: int = 20

class TestNode(NamedTuple):
    key: int
    delete_me: bool

def thread_work(kvs: list[TestNode], tree: ConcurrentSplayTree):
    """
    Put the provided splay tree under load by inserting data provided, and deleting elements set to be deleted
    """
    for k, _ in kvs:
        tree.insert(k)

    for k, _ in filter(lambda x: x.delete_me, kvs):
        tree.delete(k)

if __name__ == "__main__":
    # create a splay tree
    tree = ConcurrentSplayTree()

    dummy_data = [TestNode(x, randint(1, 4) == 0) for x in range(NUM_THREADS * 4)]

    # spawn {NUM_THREADS} threads, each of which will insert strings into tree
    #  this dummy data will need to change
    threads = [Thread(target=thread_work, args=[[dummy_data[x], dummy_data[x + (NUM_THREADS//4)], dummy_data[x + (NUM_THREADS//2)], dummy_data[x + (3 * NUM_THREADS//4)]], tree]) for x in range(NUM_THREADS)]
    for t in threads:
        t.start()

    # wait for each thread to finish
    for t in threads:
        t.join()

    # Go through test data. Ensure that elements are there unless they're deleted
    for k, should_be_deleted in dummy_data:
        if tree.find(k):
            if should_be_deleted:
                raise Exception(f"Key {k} should have been deleted")

    print("Tests passed")
