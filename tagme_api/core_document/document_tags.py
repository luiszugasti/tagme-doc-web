import datetime
import io
import json
import os
import time
import traceback
from multiprocessing.dummy import Pool as ThreadPool

import tagme
from bs4 import BeautifulSoup

'''
Simple run of testing tagme API on test corpus.
'''


def main():
    iterate_thru_docs()


# Batch job
def iterate_thru_docs():
    # assume we run this file from root://core_document
    root_path = os.getcwd()
    if root_path.endswith('core_document'):
        root_path = root_path[:-14]

    path = root_path + "//test_corpuses//test_folder//"

    documents = [path + listed_doc for listed_doc in os.listdir(path)]

    # TODO: Although we can expect compression rates from document to graph to be at around 10 times,
    #  for performance reasons, we cannot have all the documents opened in the list. Thus, we Loop through the
    #  documents list, in 1000 document chunks, writing to a new JSON file as necessary.

    # Time the TAGME Process
    start_time = time.time()

    pool = ThreadPool(40)
    dict_list = pool.map(process_document, documents)
    # This returns a list of dictionaries, now merge them
    all_docs_annotated = {}
    if bool(all_docs_annotated):
        raise ValueError("The associated dictionary is empty")
    for i in dict_list:
        all_docs_annotated = merge_two_dicts(all_docs_annotated, i)

    # Save results to file
    with io.open(root_path + "//test_output//srun.json", 'w', encoding='utf8') as json_file:
        data = json.dumps(all_docs_annotated, ensure_ascii=False, indent=4)
        json_file.write(data)

    print(time.time() - start_time)

    # Once TAGME Process is completed, can now run the full document process when re-opening the JSON Object.
    return 1


# Single job
def iterate_specific_docs(list_of_docs):
    # assume we get a list of iterable docs (just their qualified names)
    root_path = os.getcwd()
    if root_path.endswith('core_document'):
        root_path = root_path[:-14]

    path = root_path + "//test_corpuses//test_folder//"

    # Time the TAGME Process
    start_time = time.time()

    pool = ThreadPool(40)
    # starmap - like map() except that the elements of the iterable are expected to be iterables that
    # are unpacked as arguments.
    arguments = [(path, listed_doc) for listed_doc in list_of_docs]
    dict_list = pool.starmap(process_document, arguments)
    # This returns a list of dictionaries, now merge them
    all_docs_annotated = {}
    if bool(all_docs_annotated):
        raise ValueError("The associated dictionary is empty")
    for i in dict_list:
        all_docs_annotated = merge_two_dicts(all_docs_annotated, i)

    return all_docs_annotated


def process_document(base_path, document):
    start_time = time.time()
    print("Process for '" + document + "' has started.\n")

    f = open(base_path + document, 'r')

    # Get the raw text from the document
    content = f.read()
    soup = BeautifulSoup(content, features="html.parser")
    just_text = soup.get_text()

    # get the list of this specific document

    annotation = (get_tag_me(just_text))

    elapsed_time = time.time() - start_time

    print("Thread for " + document + " completed in " + str(elapsed_time) + " seconds\n")

    return {document: annotation}


''' Computes a tagme dictionary on a document per document basis'''


def get_tag_me(doc):
    try:
        annotations = get_annotations(doc)
    except AttributeError:
        print("The TAGME service returned nothing. This is a server error; however, it should have been caught!")
        return

    doc_annotations = {}  # Dictionary!

    # hard coded check
    for ann in annotations.get_annotations(0.3):

        try:
            occurrence_entity = doc_annotations[ann.entity_title]
            doc_annotations[ann.entity_title] = occurrence_entity + 1
        except KeyError:
            doc_annotations[ann.entity_title] = 1

    return doc_annotations


def get_annotations(doc, time_to_wait=1):
    try:
        annotations = tagme.annotate(doc, lang="en")
    except:  # Catch-all... not PEP Compliant
        print("Connection error, trying again in: " + str(time_to_wait) + " seconds time.\n")
        time.sleep(time_to_wait)
        traceback.print_exc()
        annotations = get_annotations(doc, time_to_wait + 1)

    # TAGME Server error, returns None type
    if annotations is None:
        print("Connection error, TAGME API service returned None type to the annotations variable.\n"
              "Will try again in " + str(time_to_wait) + " seconds time.\n"
                                                         "Time stamp: " + datetime.datetime.now().strftime(
                                                            '%Y-%m-%d %H:%M:%S'))
        time.sleep(time_to_wait)
        annotations = get_annotations(doc, time_to_wait + 1)

    return annotations


# https://stackoverflow.com/questions/38987/how-do-i-merge-two-dictionaries-in-a-single-expression
def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z


if __name__ == "__main__":
    main()
