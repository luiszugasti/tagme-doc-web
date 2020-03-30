import os

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from flask_marshmallow import Marshmallow
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
import core_document.document_tags as document_tags
from collections import Counter

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'document_corpus.db')

db = SQLAlchemy(app)
ma = Marshmallow(app)
Session = sessionmaker()


# ======================================================================================================================
# Commands for Flask CLI
@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('database created!')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('database dropped!')


@app.cli.command('db_seed')
def db_seed():
    test_doc1 = Document(document_name='test1')
    test_doc2 = Document(document_name='test2')
    test_doc3 = Document(document_name='test3')
    test_doc4 = Document(document_name='test4')
    test_doc5 = Document(document_name='test5')

    db.session.add(test_doc1)
    db.session.add(test_doc2)
    db.session.add(test_doc3)
    db.session.add(test_doc4)
    db.session.add(test_doc5)

    entity1 = Entity(entity_title='Arial')
    entity2 = Entity(entity_title='Helvetica')
    entity3 = Entity(entity_title='Sans-serif')
    entity4 = Entity(entity_title='Height')
    entity5 = Entity(entity_title='The Da Vinci Code')
    entity6 = Entity(entity_title='Dan Brown')
    entity7 = Entity(entity_title='Robert Langdon')
    entity8 = Entity(entity_title='Ron Howard')
    entity9 = Entity(entity_title='Film director')
    entity10 = Entity(entity_title='Brian Grazer')
    entity11 = Entity(entity_title='John Calley')
    entity12 = Entity(entity_title='David Koepp')

    db.session.add(entity1)
    db.session.add(entity2)
    db.session.add(entity3)
    db.session.add(entity4)
    db.session.add(entity5)
    db.session.add(entity6)
    db.session.add(entity7)
    db.session.add(entity8)
    db.session.add(entity9)
    db.session.add(entity10)
    db.session.add(entity11)
    db.session.add(entity12)

    doc_ent_rel1 = DocumentEntityRelationship(document_id=1, entity_id=1, quantity=6)
    doc_ent_rel2 = DocumentEntityRelationship(document_id=2, entity_id=2, quantity=3)
    doc_ent_rel3 = DocumentEntityRelationship(document_id=3, entity_id=3, quantity=8)
    doc_ent_rel4 = DocumentEntityRelationship(document_id=4, entity_id=4, quantity=4)
    doc_ent_rel5 = DocumentEntityRelationship(document_id=5, entity_id=5, quantity=2)
    doc_ent_rel6 = DocumentEntityRelationship(document_id=1, entity_id=6, quantity=6)
    doc_ent_rel7 = DocumentEntityRelationship(document_id=2, entity_id=7, quantity=3)
    doc_ent_rel8 = DocumentEntityRelationship(document_id=3, entity_id=8, quantity=4)
    doc_ent_rel9 = DocumentEntityRelationship(document_id=4, entity_id=9, quantity=5)
    doc_ent_rel10 = DocumentEntityRelationship(document_id=1, entity_id=11, quantity=6)
    doc_ent_rel11 = DocumentEntityRelationship(document_id=2, entity_id=12, quantity=7)
    doc_ent_rel12 = DocumentEntityRelationship(document_id=3, entity_id=1, quantity=8)
    doc_ent_rel13 = DocumentEntityRelationship(document_id=4, entity_id=2, quantity=9)
    doc_ent_rel14 = DocumentEntityRelationship(document_id=5, entity_id=3, quantity=1)
    doc_ent_rel15 = DocumentEntityRelationship(document_id=1, entity_id=4, quantity=3)
    doc_ent_rel16 = DocumentEntityRelationship(document_id=1, entity_id=5, quantity=4)
    doc_ent_rel17 = DocumentEntityRelationship(document_id=4, entity_id=6, quantity=6)
    doc_ent_rel18 = DocumentEntityRelationship(document_id=1, entity_id=7, quantity=7)
    doc_ent_rel19 = DocumentEntityRelationship(document_id=1, entity_id=8, quantity=8)
    doc_ent_rel20 = DocumentEntityRelationship(document_id=1, entity_id=9, quantity=3)
    doc_ent_rel21 = DocumentEntityRelationship(document_id=1, entity_id=10, quantity=4)
    doc_ent_rel22 = DocumentEntityRelationship(document_id=3, entity_id=10, quantity=5)
    doc_ent_rel23 = DocumentEntityRelationship(document_id=1, entity_id=12, quantity=1)
    doc_ent_rel24 = DocumentEntityRelationship(document_id=5, entity_id=10, quantity=6)

    db.session.add(doc_ent_rel24)
    db.session.add(doc_ent_rel23)
    db.session.add(doc_ent_rel22)
    db.session.add(doc_ent_rel21)
    db.session.add(doc_ent_rel20)
    db.session.add(doc_ent_rel19)
    db.session.add(doc_ent_rel18)
    db.session.add(doc_ent_rel17)
    db.session.add(doc_ent_rel16)
    db.session.add(doc_ent_rel15)
    db.session.add(doc_ent_rel14)
    db.session.add(doc_ent_rel13)
    db.session.add(doc_ent_rel12)
    db.session.add(doc_ent_rel11)
    db.session.add(doc_ent_rel10)
    db.session.add(doc_ent_rel9)
    db.session.add(doc_ent_rel8)
    db.session.add(doc_ent_rel7)
    db.session.add(doc_ent_rel6)
    db.session.add(doc_ent_rel5)
    db.session.add(doc_ent_rel4)
    db.session.add(doc_ent_rel3)
    db.session.add(doc_ent_rel2)
    db.session.add(doc_ent_rel1)

    test_user = User(first_name='John', last_name='Hamshrit', email='gmail@gmail.com', password='superclever123')

    db.session.add(test_user)

    db.session.commit()
    print('database seeded!')


# ======================================================================================================================
# App decorators
@app.route('/')
def hello_world():
    return 'Hello World'


@app.route('/get_doc_entity/', methods=['GET'])
def get_doc_entities():
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

    return jsonify(final_entities)

    # return jsonify(entities)
    #
    #
    # # check if the document exists within our database.
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


@app.route('/get_all_doc_entities', methods=['GET'])
def get_all_doc_entities():
    doc_entities_list = Entity.query.all()
    result = entities_schema.dump(doc_entities_list)
    return jsonify(result)


@app.route('/get_all_docs', methods=['GET'])
def get_all_docs():
    doc_list = Document.query.all()
    result = entities_schema.dump(doc_list)
    return jsonify(result)


# # database models - remember to make this modular later...
class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)


class Document(db.Model):
    __tablename__ = 'document'
    document_id = Column(Integer, primary_key=True)
    document_name = Column(String(100), unique=True)


class Entity(db.Model):
    __tablename__ = 'entity'
    entity_id = Column(Integer, primary_key=True)
    entity_title = Column(String, unique=True)


class DocumentEntityRelationship(db.Model):
    __tablename__ = 'doc_ent_rel'
    __table_args__ = (UniqueConstraint('document_id', 'entity_id', name='uk_document_entity_id'),)
    relationship_id = Column(Integer, primary_key=True)
    document_id = Column('document_id', Integer, ForeignKey("document.document_id"))
    entity_id = Column('entity_id', Integer, ForeignKey("entity.entity_id"))
    quantity = Column(Integer, nullable=False)


# # Marshmallow definitions
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'password')


class DocumentSchema(ma.Schema):
    class Meta:
        fields = ('document_id', 'document_name')


class EntitySchema(ma.Schema):
    class Meta:
        fields = ('entity_id', 'entity_title')


user_schema = UserSchema()
users_schema = UserSchema(many=True)

document_schema = DocumentSchema()
documents_schema = DocumentSchema(many=True)

entity_schema = EntitySchema()
entities_schema = EntitySchema(many=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
