import os
from collections import Counter

import click
from flask import (
    Blueprint, request, jsonify
)
from flask import g
from flask.cli import with_appcontext

import tagme_api.core_document.document_tags as document_tags
import tagme_api.core_document.document_comparison as document_comparison
from tagme_api.db import get_db
import time
import networkx as nx

bp = Blueprint('tagme_api', __name__)


# helper function for querying a database, from the good folks at flask.
def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


# query the database - but this time use executemany
def query_db_many(query, args=(), one=False):
    cur = g.db.executemany(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


# get_doc_entity: return the document entities for a document.
@bp.route('/get_doc_entity/', methods=['GET'])
def get_doc_entities():
    if not request.args:
        return jsonify("message=Error. You have not specified any documents as your arguments. Refer to the "
                       "documentation for more information.")

    documents = (request.args.to_dict())
    # if the top key is entered in the request, then the function behaves to return the "top" amount of entries.
    # aka if top = 5 then it returns the top 5 hits, sorted by decreasing entity occurrences.
    return_top_docs = int(documents.pop('top', 0))
    documents = list(documents.keys())

    final_entities = {}
    entities = document_tags.iterate_specific_docs(documents)

    # sort through the entities *if* we have a return_top_docs entry.
    if return_top_docs > 0:
        # iterate through each of the documents, sorting the entities and removing anything less than 'top'.
        # https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
        # iterate in place?
        for document in entities:
            temp = Counter(entities[document])
            temp_entity_list = {}
            # that's ok because collections does it for me.
            # https://stackoverflow.com/questions/11902665/top-values-from-dictionary
            for entity, occurrences in temp.most_common(return_top_docs):
                temp_entity_list[entity] = occurrences
            final_entities[document] = temp_entity_list
    else:
        final_entities = entities

    # test: insert into the database, the entries for the document we have.
    db = get_db()

    for doc_name in entities.keys():

        if db.execute(
                'SELECT * FROM document WHERE document_name = ?', (doc_name,)
        ).fetchone() is None:
            # not in the database yet. put it in.
            db.execute(
                'INSERT INTO document (document_name) VALUES (?)', (doc_name,)
            )
            db.commit()

        for doc_entity in entities[doc_name].keys():

            if db.execute(
                    'SELECT * FROM entity WHERE entity_title = ?', (doc_entity,)
            ).fetchone() is None:
                # not in the database yet as well. put it in.
                db.execute(
                    'INSERT INTO entity (entity_title) VALUES (?)', (doc_entity,)
                )
                db.commit()

            # Prepare to enter the document_id, entity_id tuples into the doc_ent_rel table.
            sample_doc_id = query_db(
                'SELECT document_id FROM document WHERE document_name = ?', (doc_name,), one=True
            )['document_id']
            sample_entity_id = query_db(
                'SELECT entity_id FROM entity WHERE entity_title = ?', (doc_entity,), one=True
            )['entity_id']

            if db.execute(
                    'SELECT * FROM doc_ent_rel WHERE document_id = ? and '
                    'entity_id = ?;', (sample_doc_id, sample_entity_id)
            ).fetchone() is None:
                db.execute(
                    'INSERT INTO doc_ent_rel (document_id, entity_id, quantity) VALUES (?, ?, ?)',
                    (sample_doc_id, sample_entity_id, entities[doc_name][doc_entity])
                )

    return jsonify(final_entities)


@click.command('entity-batch')
@with_appcontext
def batch_doc_entities_command():
    def docs_at_a_time_50():
        return 50

    # get all the documents in the doc corpus specified.
    # assume we run this file from tagme_api folder
    root_path = os.getcwd()
    if root_path.endswith('tagme_api'):
        root_path = root_path[:-10]

    path = root_path + "//test_corpuses//test_folder//"

    # get the documents within the whole directory.
    documents = [listed_doc for listed_doc in os.listdir(path)]

    db = get_db()

    db_document_list = query_db(
        'SELECT DISTINCT document_name FROM document_entity'
    )
    db_document_names = []
    print("Getting docs...")
    for dictionary in db_document_list:
        db_document_names.append(dictionary['document_name'])
        print("{0} is currently in the database.".format(dictionary))

    # find the entries that are NOT in the database.
    required_docs = list(set(documents).difference(db_document_names))

    # get the documents that are currently in the SQL database.
    print("Seeding {0} new entries into the database.".format(len(required_docs)))
    # For the documents that are not in the database yet, add them to the database and save all their entities.
    # Do this in 50 document chunks. Iterate thru the list and send this to the tagme service.

    for i in range(0, len(required_docs), docs_at_a_time_50()):
        # build the list...
        required_docs_processed = required_docs[i:i + docs_at_a_time_50() - 1]
        for doc in required_docs_processed:
            print(doc)
        # send it to the document_tags service.
        document_entity_structure = document_tags.iterate_specific_docs(required_docs_processed)

        # insert all the found documents within the database.
        for doc_name in document_entity_structure:
            for entity in document_entity_structure[doc_name]:
                db.execute('INSERT INTO document_entity(document_name, entity_id, quantity) VALUES (?, ?, ?)',
                           [doc_name
, entity, document_entity_structure[doc_name][entity]])

        # commit.
        db.commit()
        print("Status: {0}".format(i))


# @click.command('build-graph-db')
# @with_appcontext
def build_graph_from_db_command():

    db = get_db()

    start_time = time.time()

    # Rebuild the document entity structure
    db_document_list = query_db(
        'SELECT DISTINCT document_name FROM document_entity'
    )

    document_entity_structure = {}

    # if it's too slow: do it in parallel.
    for doc_name in db_document_list:
        dn = doc_name['document_name']
        entities = query_db(
        'SELECT entity_id, quantity FROM document_entity WHERE document_name = ?', (dn,)
    )
        document_entity_structure[dn] = {}
        for entity in entities:
            document_entity_structure[dn][entity['entity_id']] = entity['quantity']

    # document_entity_structure has been rebuilt.
    end_time = time.time()
    print("Rebuilt all docs in {0}".format(end_time-start_time))

    # now to build a graph...
    doc_map = nx.Graph()
    doc_map = document_comparison.common_between_dicts(document_entity_structure)


    print("Graph has been built in {0}".format(end_time - start_time))



def init_app(app):
    app.cli.add_command(batch_doc_entities_command)
    # app.cli.add_command(build_graph_from_db_command)
    pass
