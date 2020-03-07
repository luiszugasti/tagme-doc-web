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
import string
import random
import math

'''
Builds a comparison structure between documents that should be easily relatable.
'''


class Graph:
    def __init__(self):
        # Hashed dictionary of nodes - it will get big!
        self.nodes = {} # nodeID : node -> doc_name : structure with doc_name, and edges

    def add_node(self, node):
        # add a single key to the dictionary
        if node.nodeID in self.nodes:
            print("Apparently you're adding a duplicate node? Not allowed\n")
        else:
            self.nodes[node.nodeID] = node # just a one, makes the data structure somewhat simpler?

# I feel I should be throwing these as exceptions... maybe if this was production ready code


class Node:
    def __init__(self, node, edges=None):
        if edges is None:
            self.edges = {}
        else:
            self.edges = edges
        self.nodeID = node.nodeID

    def add_edge(self, edge):
        """

        :type edge: Edge
        """
        # key for the edge will be the destination
        if edge.ending_node in self.edges:
            print("You're trying to add a duplicate edge. Not allowed\n")
        else:
            self.edges[edge.ending_node] = edge


class Edge:
    def __init__(self, starting_node, ending_node, weight):
        self.starting_node = starting_node
        self.ending_node = ending_node
        self.weight = weight


def main(disallow_insignificant_weights):
    reload(sys)
    sys.setdefaultencoding('utf8')

    # Set the authorization token for subsequent calls globally
    tagme.GCUBE_TOKEN = "1c7074e0-10bb-4131-a498-5179035a001a-843339462"

    with io.open("production.json", encoding='utf-8') as file:
        document_string = file.read().encode('utf-8')

    document_corpus = json.loads(document_string, encoding="utf-8")

    doc_map = common_between_dicts(document_corpus, disallow_insignificant_weights)

    return 1


def common_between_dicts(dictionary, disallow_insignificant_weights):
    # Go through all the docs and build an empty graph for them
    doc_map = Graph()

    # What I can do is iterate through all the document names and build a list of tuples to iterate thru,
    # these are technically my edges!
    tuple_document = []
    for doc_name in dictionary.iteritems():
        for doc_name2 in dictionary.iteritems():
            if doc_name != doc_name2: # This prevents loops of a document to itself, but we will still have swapped edges
                tuple_document.append((doc_name, doc_name2))

    start_time = time.time()
    pool = ThreadPool(60)
    edge_list = pool.map(package_up_tuples_and_send_to_tagme, tuple_document)
    elapsed_time = time.time() - start_time

    print("Job to get edges completed in {0} seconds\n# of Operations: {1}".format(str(elapsed_time),
                                                                                   str(len(edge_list))))

    return 1


def package_up_tuples_and_send_to_tagme(two_docs):
    start_time = time.time()
    # Overly descriptive name...
    # Loop all of doc1 and doc2's entities, and package them up into a list of entities.
    doc_entities_to_compare = []
    for entity in two_docs[0][1]:
        for entity2 in two_docs[1][1]:
            doc_entities_to_compare.append((entity, entity2))

    # Send to TAGME API to get the weight of this connection!
    entity_weights = get_entity_relatedness(doc_entities_to_compare)

    # Weight calculation
    weight = 0.0
    for rel in entity_weights.relatedness:
        weight += rel.rel

    weight = weight / len(entity_weights.relatedness)

    # Limitation - if there's 13 million docs, then this will be HUGE.

    returned_edge = Edge(two_docs[0][0], two_docs[1][0], weight)

    elapsed_time = time.time() - start_time
    print("Thread for " + two_docs[0][0] + " and " + two_docs[1][0] + " completed in " + str(
        elapsed_time) + " seconds\n")
    return returned_edge


def get_entity_relatedness(list_of_tuples, time_to_wait=1):
    try:
        entity_ratings = tagme.relatedness_title(list_of_tuples)
    except:
        print("Connection error, trying again in: " + str(time_to_wait) + " seconds time.\n")
        time.sleep(time_to_wait)
        entity_ratings = get_entity_relatedness(list_of_tuples, time_to_wait * 2)
    return entity_ratings


def id_generator(size=7, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


if __name__ == "__main__":
    disallow_insignificant_weights = 1  # If 1, disallow insignificant weights
    main(disallow_insignificant_weights)
