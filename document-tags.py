import tagme
import os
from bs4 import BeautifulSoup
import time
import json
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
import io
import datetime
import traceback

from multiprocessing import Pool

'''
Simple run of testing tagme API on test corpus.
'''


def main():
    # Set the authorization token for subsequent calls globally
    tagme.GCUBE_TOKEN = "1c7074e0-10bb-4131-a498-5179035a001a-843339462"

    iterate_thru_docs()


def iterate_thru_docs():
    path = os.getcwd() + "/clueweb09PoolFilesTest"
    print(os.getcwd())
    all_docs_annotated = []

    documents = os.listdir(path)

    # Although we can expect compression rates from document to graph to be at around 10 times, for performance reasons,
    # we cannot have all the documents opened in the list. Thus, we Loop through the documents list, in 1000 document
    # chunks, writing to a new JSON file as necessary.

    # Time the TAGME Process
    start_time = time.time()

    pool = ThreadPool(40)
    dict_list = pool.map(process_document, documents)
    # This returns a list of dictionaries, now merge them
    all_docs_annotated = {}
    for i in dict_list:
        all_docs_annotated = merge_two_dicts(all_docs_annotated, i)

    # Save results to file
    with io.open('shortrun.json', 'w', encoding='utf8') as json_file:
        data = json.dumps(all_docs_annotated, ensure_ascii=False, indent=4)
        # auto-decodes data to unicode
        data = data.decode('utf-8')
        json_file.write(data)

    print (time.time() - start_time)

    # Once TAGME Process is completed, can now run the full document process when re-opening the JSON Object.
    return 1


def process_document(document):
    start_time = time.time()
    print("Process for " + document + " has started.\n")

    path = os.getcwd() + "/clueweb09PoolFilesTest"
    # open doc
    f = open(path + '/' + document, 'r')

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

    for ann in annotations.get_annotations(0.3):

        try:
            occurrence_entity = doc_annotations[unicode(ann.entity_title).encode('utf-8')]
            doc_annotations[unicode(ann.entity_title).encode('utf-8')] = occurrence_entity + 1
        except KeyError:
            doc_annotations[unicode(ann.entity_title).encode('utf-8')] = 1

    return doc_annotations


def get_annotations(doc, time_to_wait=1):
    try:
        annotations = tagme.annotate(doc, lang="en")
    except: # Catch-all... not PEP Compliant
        print("Connection error, trying again in: " + str(time_to_wait) + " seconds time.\n")
        time.sleep(time_to_wait)
        traceback.print_exc()
        annotations = get_annotations(doc, time_to_wait + 1)

    # TAGME Server error, returns None type
    if annotations is None:
        print("Connection error, TAGME API service returned None type to the annotations variable.\n"
              "Will try again in " + str(time_to_wait) + " seconds time.\n"
              "Time stamp: " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
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
