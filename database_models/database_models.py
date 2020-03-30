import os

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from flask_marshmallow import Marshmallow
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
import core_document.document_tags as document_tags
from collections import Counter

from app import app

db = SQLAlchemy(app)
ma = Marshmallow(app)


# database models - remember to make this modular later...
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