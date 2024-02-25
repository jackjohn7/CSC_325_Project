from typing import NamedTuple
from friendly_splay import ConcurrentSplayTree
from threading import Thread
from random import choice, randint
from os import getpid
from pprint import pprint
from copy import deepcopy
from traceback import format_exc
from argparse import ArgumentParser

NUM_THREADS: int = 20
VERBOSE = True
RESPONSIBILITY_FACTOR = 20

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
    responsibility_factor = RESPONSIBILITY_FACTOR

    rands = [choice([True, False]) for _ in range(NUM_THREADS * responsibility_factor)]

    dummy_data = []
    for x in range(NUM_THREADS * responsibility_factor):
        a = dummy_data[-1].key+1 if len(dummy_data) > 0 else 0
        dummy_data.append(TestNode(randint(a, a + 4), rands[x]))
        
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
                if not tree.find(k):
                    raise Exception(f"FAIL: Key {k} was not found when it should have been")


        x, y = 0, 1
        while y < len(generated):
            assert generated[x] < generated[y]
            x += 1
            y += 1
        verbose_log("Tree is still in valid BST form")

        verbose_log(f"{n} OK: Test Passed")
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
    parser = ArgumentParser(
        prog='Concurrent Splay Tree Test',
        description='Tests the integrity of concurrency-friendly splay tree after many concurrent operations',
        epilog='Written by John Branch, Cameron White, and Bradford Stephens'
    )
    parser.add_argument('-t', '--threads', default=20)
    parser.add_argument('-r', '--responsibility', default=20)
    parser.add_argument('-n', '--number', default=100)
    parser.add_argument('-v', '--verbose', action='store_true')

    args = parser.parse_args()
    num_tests = int(args.number)

    VERBOSE = args.verbose
    NUM_THREADS = int(args.threads)
    RESPONSIBILITY_FACTOR = int(args.responsibility)

    successes = 0
    for i in range(num_tests):
        print(f"RUNNING: {successes}/{num_tests} tests passed", end='\r')
        if test(i+1):
            successes += 1
    print(f"COMPLETE: {successes}/{num_tests} tests passed")
