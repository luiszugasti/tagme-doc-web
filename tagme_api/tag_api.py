import tagme_api.core_document.document_tags as document_tags
from collections import Counter
import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

from tagme_api.db import get_db

from flask import (
    Blueprint, request, jsonify
)

bp = Blueprint('tagme_api', __name__)


# get_doc_entity: return the document entities for a document.
@bp.route('/get_doc_entity/', methods=['GET'])
def get_doc_entities():
    if not request.args:
        return jsonify("message=Error. You have not specified any documents as your arguments. Refer to the "
                       "documentation for more information.")

    documents = (request.args.to_dict())
    # if the top key is entered in the request, then the function behaves to return the "top" amount of entries.
    # aka if top = 5 then it returns the top 5 hits, sorted by decreasing entity occurrences.
    return_top_docs = int(documents.pop('top', None))
    documents = list(documents.keys())

    final_entities = {}
    entities = document_tags.iterate_specific_docs(documents)

    # sort through the entities *if* we have a return_top_docs entry.
    if return_top_docs:
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

    for key in entities.keys():

        if db.execute(
            'SELECT * FROM document WHERE document_name = ?', (key,)
        ).fetchone() is None:
            # not in the database yet. put it in.
            db.execute(
                'INSERT INTO document (document_name) VALUES (?)', (key,)
            )
            db.commit()

        for doc_entity in entities[key].keys():

            if db.execute(
                'SELECT * FROM entity WHERE entity_title = ?', (doc_entity,)
            ).fetchone() is None:
                # not in the database yet as well. put it in.
                db.execute(
                    'INSERT INTO entity (entity_title) VALUES (?)', (doc_entity,)
                )
                db.commit()

            sample_doc_id = db.execute(
                'SELECT document_id FROM document WHERE document_name = ?', (key,)
            )
            sample_entity_id = db.execute(
                'SELECT entity_id FROM entity WHERE entity_title = ?', (doc_entity,)
            )
            db.execute(
                'INSERT INTO doc_ent_rel (document_id, entity_id, quantity) VALUES (?, ?, ?)', (key, doc_entity, entities[key][doc_entity])
            )

    return jsonify(final_entities)

    # check if the document exists within our database.
    # document_entity_set = Document.query.filter_by(document_name=document_name).first()
    # if document_entity_set:
    #
    #
    #     return jsonify(message="This feature is under testing.")
    #     # if the document exists, then we can surely serve the entities back.
    #     session = Session()
    #     # this is broken.... :$
    #     result = session.query(DocumentEntityRelationship).filter_by(document_id=1).all()
    #     return jsonify(result)
    # else:
    #     #document may exist in the corpus but not in the database...
    #
    #     return jsonify(message="Document {} was not found in the database.".format(document_name)), 404
    # # if it exists, then we can serve the entities back.
    #
    # # if not, then call the related document processing function from document-tags.
    #
    # # with the returned params, we send them back to the client...
    #
    # # and commit them to the sql database.
    # pass


@click.command('entity-batch')
@click.argument("num_docs")
@with_appcontext
def batch_doc_entities_command(num_docs):
    try:
        num_docs = int(num_docs)
        if num_docs < 1:
            raise ValueError('Input is a number, but not valid')
    except ValueError as error:
        print('Please try again with a new value')
        if error:
            print('While handling the above exception, another exception occurred:\n'
                  + repr(error))

    print("Seeding {0} new entries into the database.".format(num_docs))
    """For the documents that are not in the database yet, add them to the database and save all their entities."""

    pass


def init_app(app):
    app.cli.add_command(batch_doc_entities_command)
