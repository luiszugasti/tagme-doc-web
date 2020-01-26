import tagme
import os
from bs4 import BeautifulSoup
import time
import json
import requests  # Don't know if this will work?
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

from multiprocessing import Pool

'''
Simple run of testing tagme API on test corpus. Let's see how a linear process runs.
'''


def main():
    # Set the authorization token for subsequent calls globally
    tagme.GCUBE_TOKEN = "1c7074e0-10bb-4131-a498-5179035a001a-843339462"

    iterate_thru_docs()


def iterate_thru_docs():
    start_time = time.time()

    path = os.getcwd() + "/clueweb09PoolFilesTest"
    print(os.getcwd())
    all_docs_annotated = {}

    documents = os.listdir(path)
    full_document_path = [path + '/' + document for document in documents]

    # Threading in Python
    pool = ThreadPool(4)
    all_docs_annotated = pool.map(process_document, documents)

    # Save results to file
    output = json.dumps(dict)
    f = open("dict.json", "w")
    f.write(output)
    f.close()
    return 1


def process_document(document):
    print document

    # open doc
    f = open(document, 'r')

    # Get the raw text from the document
    content = f.read()
    soup = BeautifulSoup(content, features="html.parser")
    just_text = soup.get_text()

    # get the list of this specific document

    all_docs_annotated[document] = (get_tag_me(just_text))

    elapsed_time = time.time() - start_time

    return


''' Computes a tagme dictionary on a document per document basis'''


def get_tag_me(doc):
    annotations = get_annotations(doc)

    doc_annotations = {}  # Dictionary!

    for ann in annotations.get_annotations(0.3):
        # print "mention: " + unicode(ann.mention).encode('utf-8')\
        #       + ". entity_Title: '" + unicode(ann.entity_title).encode('utf-8') + "'"
        try:
            occurrence_entity = doc_annotations[unicode(ann.entity_title).encode('utf-8')]
            doc_annotations[unicode(ann.entity_title).encode('utf-8')] = occurrence_entity + 1
        except KeyError:
            doc_annotations[unicode(ann.entity_title).encode('utf-8')] = 1

    return doc_annotations


def get_annotations(doc, time_to_wait=1):
    try:
        annotations = tagme.annotate(doc, lang="en")
    except:
        print("Connection error, trying again in: " + str(time_to_wait) + " seconds time.\n")
        time.sleep(time_to_wait)
        annotations = get_annotations(doc, time_to_wait + 1)
    return annotations


if __name__ == "__main__":
    main()
