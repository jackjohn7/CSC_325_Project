from typing import NamedTuple
from friendly_splay import ConcurrentSplayTree
from threading import Thread
from random import randint
from os import getpid
from pprint import pprint

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

    for k, _ in filter(lambda x: not x.delete_me, kvs):
        if not tree.find(k):
            print(f"Something went wrong in thread {getpid()}")

if __name__ == "__main__":
    # create a splay tree
    tree = ConcurrentSplayTree()

    dummy_data = [TestNode(x, randint(1, 4) == 1) for x in range(NUM_THREADS * 4)]

    # spawn {NUM_THREADS} threads, each of which will insert strings into tree
    #  this dummy data will need to change
    threads = [Thread(target=thread_work, args=[[dummy_data[x], dummy_data[x + (NUM_THREADS//4)], dummy_data[x + (NUM_THREADS//2)], dummy_data[x + (3 * NUM_THREADS//4)]], tree]) for x in range(NUM_THREADS)]
    for t in threads:
        t.start()

    # wait for each thread to finish
    print(f"Waiting for {NUM_THREADS} threads to finish executing")
    for t in threads:
        t.join()
    print(f"{NUM_THREADS} threads finished executing successfully")

    # ensure tree is still in valid form
    generated = [n for n in tree.inorder_gen()]

    # Go through test data. Ensure that elements are there unless they're deleted
    for k, should_be_deleted in dummy_data:
        if tree.find(k):
            if should_be_deleted:
                raise Exception(f"FAIL: Key {k} should have been deleted")
        elif not should_be_deleted:
            raise Exception(f"FAIL: Key {k} was not found when it should have been")


    x, y = 0, 1
    while y < len(generated):
        assert generated[x] < generated[y]
        x += 1
        y += 1
    print("Tree is still in valid BST form")

    print("OK: Tests Pass")

    print("dataset")
    print(dummy_data)
    print(generated)
