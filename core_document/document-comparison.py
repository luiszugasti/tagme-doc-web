import io
import json
import os
import random
import string
import time
from multiprocessing.dummy import Pool as ThreadPool

import networkx as nx
import tagme

'''
Builds a comparison structure between documents that should be easily relatable.
'''


def main():
    # Set the authorization token for subsequent calls globally
    tagme.GCUBE_TOKEN = "1c7074e0-10bb-4131-a498-5179035a001a-843339462"

    root_path = os.getcwd()
    if root_path.endswith('core_document'):
        root_path = root_path[:-14]

    path = root_path + "\\test_output\\"

    with io.open(path + "dict.json", encoding='utf-8') as file:
        document_string = file.read().encode('utf-8')

    document_corpus = json.loads(document_string, encoding="utf-8")

    doc_map = common_between_dicts(document_corpus)

    return 1


def common_between_dicts(doc_dictionary):
    # Go through all the docs and build an empty graph for them
    doc_map = nx.Graph()

    secondary_dictionary = []
    tuple_document = []
    for doc_name in doc_dictionary:
        for doc_name2 in secondary_dictionary:
            if doc_name != doc_name2 and not (doc_name in secondary_dictionary):
                tuple_document.append(((doc_name, doc_dictionary[doc_name]), (doc_name2, doc_dictionary[doc_name2])))
        secondary_dictionary.append(doc_name)

    start_time = time.time()
    pool = ThreadPool(1)
    edge_list = pool.map(package_up_tuples_and_send_to_tagme, tuple_document)
    elapsed_time = time.time() - start_time

    doc_map.add_edges_from(edge_list)

    print("Job to get edges completed in {0} seconds\n# of Operations: {1}".format(str(elapsed_time),
                                                                                   str(len(edge_list))))

    return doc_map


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

    returned_edge = (str(two_docs[0][0]), str(two_docs[1][0]), {'weight': weight})

    elapsed_time = time.time() - start_time
    print("Thread for " + str(two_docs[0][0]) + " and " + str(two_docs[1][0]) + " completed in " + str(
        elapsed_time) + " seconds\n")
    return returned_edge


def get_entity_relatedness(list_of_tuples, time_to_wait=1):
    try:
        entity_ratings = tagme.relatedness_title(list_of_tuples)
    except:  # Too broad an exception clause
        print("Connection error, trying again in: " + str(time_to_wait) + " seconds time.\n")
        time.sleep(time_to_wait)
        entity_ratings = get_entity_relatedness(list_of_tuples, time_to_wait * 2)
    return entity_ratings


def id_generator(size=7, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


if __name__ == "__main__":
    main()
