# encoding=utf8
import sys
import tagme
import os
from bs4 import BeautifulSoup
import time
import json
import requests  # Don't know if this will work?
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
import io

'''
Builds a comparison structure between documents that should be easily relatable.
'''


def main():
    reload(sys)
    sys.setdefaultencoding('utf8')

    # Set the authorization token for subsequent calls globally
    tagme.GCUBE_TOKEN = "1c7074e0-10bb-4131-a498-5179035a001a-843339462"

    # with io.open("test_dict.json", encoding='utf-8') as file:
    #     json_string = file.read().encode('utf-8')
    #
    # json_object = json.loads(json_string, encoding="utf-8")
    #
    # with io.open("test_dict.json", encoding='utf-8') as file:
    #     json_strong = file.read().encode('utf-8')
    #
    # json_object2 = json.loads(json_string, encoding="utf-8")
    #
    # json_key = json_object[0]['clueweb09-en0000-00-06386'].keys()
    #
    # json_key2 = json_object2[0]['clueweb09-en0000-00-06386'].keys()

    # Actually load the program inside, after my sanity checks
    with io.open("dict.json", encoding='utf-8') as file:
        document_string = file.read().encode('utf-8')

    document_corpus = json.loads(document_string, encoding="utf-8")
    # Loads our dictionary. Struct is document : annotation : count
    # You can submit a list of pairs of any size, but the TagMe web service will be issued one query every 100 pairs. If one entity does not exist, the result will be None.

    # First, I'll find all the entities that are common between each doc. Sets.
    # Then, build unique tuples, create a list of these tuples, send to TAGME.
    # TAGME returns the relatedness between each of them.
    # Add them all, and divide them by the size of the TAGME packet.
    # Append this to my Graph.

    hashededgemap = common_between_dicts(document_corpus)

    return 1

def common_between_dicts(dictionary):
    # Go through all the docs and build a hashmap for them
    commonelements = {}
    for iterable in dictionary.iteritems():
        for iterable2 in dictionary.iteritems():
            # no duplicates
            if iterable != iterable2:
                # This approach is incorrect, because it is succeptible to comparing keys within the same document!
                # intersection = {set(iterable[1].keys()).intersection(iterable2[1].keys())}
                # commonelements[iterable] = {iterable2: intersection}


if __name__ == "__main__":
    main()


class Graph:
    def __init__(self):
        self.nodes = 0


class Node:
    def __init__(self):
        self.edges = []


class Edge:
    def __init__(self):
        self.startingnode = ""
        self.endingnode = ""
        self.weight = 0
