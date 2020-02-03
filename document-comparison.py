# encoding=utf8
import sys
import tagme
import os
from bs4 import BeautifulSoup
import time
import json
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
import io

'''
Builds a comparison structure between documents that should be easily relatable.
'''


class Graph:
    def __init__(self):
        # Hashed dictionary of nodes - it will get big!
        self.nodes = {}


class Node:
    def __init__(self):
        self.edges = {}


class Edge:
    def __init__(self):
        self.starting_node = ""
        self.ending_node = ""
        self.weight = 0


def main():
    reload(sys)
    sys.setdefaultencoding('utf8')

    # Set the authorization token for subsequent calls globally
    tagme.GCUBE_TOKEN = "1c7074e0-10bb-4131-a498-5179035a001a-843339462"

    with io.open("dict.json", encoding='utf-8') as file:
        document_string = file.read().encode('utf-8')

    document_corpus = json.loads(document_string, encoding="utf-8")
    # Loads our dictionary. Struct is document : annotation : count
    # You can submit a list of pairs of any size, but the TagMe web
    # service will be issued one query every 100 pairs. If one entity does not exist, the result will be None.

    # First, I'll find all the entities that are common between each doc. Sets.
    # Then, build unique tuples, create a list of these tuples, send to TAGME.
    # TAGME returns the relatedness between each of them.
    # Add them all, and divide them by the size of the TAGME packet.
    # Append this to my Graph.

    doc_map = common_between_dicts(document_corpus)

    return 1


def common_between_dicts(dictionary):
    # Go through all the docs and build an empty graph for them
    doc_map = Graph()

    for iterable in dictionary.iteritems():
        for iterable2 in dictionary.iteritems():
            # compare two different documents
            if iterable != iterable2:
                # Now iterate through the iterable and iterable2 to build tuples of all their entities:
                # format: (iterable_entity : iterable2_entity)
                # for each of this iterable, we'll loop through ALL the iterable2 possibles (thus threaded approach!)
                # for each built tuple that we get, we send it to tagme, and in return, add this edge to the node.
                # Since we want to not go over a document again (and do n! instead of n^2 complexity)
                # We have to mark a document

                pool = ThreadPool(40)
                edge_list = pool.map(package_up_tuples_and_send_to_tagme, [dictionary.iteritems(), dictionary.iteritems()])
                common_tuple = ()

    return 1


def package_up_tuples_and_send_to_tagme(doc_list):
    # Overly descriptive name...
    # Loop all of doc1 and doc2's entities, and package them up into a list of entities.

    pass


if __name__ == "__main__":
    main()
