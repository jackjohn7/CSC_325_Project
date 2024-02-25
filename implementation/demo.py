from typing import NamedTuple
from friendly_splay import ConcurrentSplayTree
from threading import Thread
from random import choice
from os import getpid
from pprint import pprint
from copy import deepcopy
from traceback import format_exc

NUM_THREADS: int = 20
VERBOSE = True

def verbose_log(text: str):
    if VERBOSE:
        print(text)

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
        print(f"deleting {k} because {_}")
        tree.delete(k)

    for k, _ in filter(lambda x: not x.delete_me, kvs):
        if not tree.find(k):
            print(f"Something went wrong in thread {getpid()}")
    for k, _ in filter(lambda x: x.delete_me, kvs):
        if tree.find(k):
            print(f"Something went wrong in thread {getpid()}")

def test(n: int) -> bool:
    # create a splay tree
    tree = ConcurrentSplayTree()
    # states how many datapoints a thread is responsible for
    responsibility_factor = 4

    rands = [choice([True, False]) for _ in range(NUM_THREADS * responsibility_factor)]

    dummy_data = [TestNode(x, rands[x]) for x in range(NUM_THREADS * responsibility_factor)]
    print(dummy_data)
    copy_data = deepcopy(dummy_data)

    try:
        # spawn {NUM_THREADS} threads, each of which will insert strings into tree
        #  this dummy data will need to change
        threads = [Thread(target=thread_work, args=[[copy_data.pop() for _ in range(responsibility_factor)], tree]) for _ in range(NUM_THREADS)]
        for t in threads:
            t.start()

        # wait for each thread to finish
        verbose_log(f"Waiting for {NUM_THREADS} threads to finish executing")
        for t in threads:
            t.join()
        verbose_log(f"{NUM_THREADS} threads finished executing successfully")

        # ensure tree is still in valid form
        generated = [n for n in tree.inorder_gen()]

        # Go through test data. Ensure that elements are there unless they're deleted
        for k, should_be_deleted in dummy_data:
            if should_be_deleted:
                if tree.find(k):
                    raise Exception(f"FAIL: Key {k} should have been deleted")
                else:
                    print(f"key {k} was not found which is good")
            else:
                if not tree.find(k):
                    raise Exception(f"FAIL: Key {k} was not found when it should have been")


        x, y = 0, 1
        while y < len(generated):
            assert generated[x] < generated[y]
            x += 1
            y += 1
        verbose_log("Tree is still in valid BST form")

        verbose_log(f"{n} OK: Test Passed")
        print(generated)
        return True

    except Exception as e:
        generated = [n for n in tree.inorder_gen()]
        print(f"{n} FAIL")
        print(e)
        x = format_exc()
        print(x)
        print("dataset")
        pprint(dummy_data)
        print("inorder data")
        print(generated)
        return  False

if __name__ == "__main__":
    num_tests = 100
    successes = 0
    for i in range(num_tests):
        if test(i+1):
            successes += 1
    print(f"{successes}/{num_tests} tests passed")
