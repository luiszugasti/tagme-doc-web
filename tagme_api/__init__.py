import os

from flask import Flask, jsonify, request


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'document_corpus.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple json request to test the app works
    @app.route('/hello')
    def hello():
        return jsonify("message= Hello, world!")

    from . import db
    db.init_app(app)

    from . import tag_api
    app.register_blueprint(tag_api.bp)
    tag_api.init_app(app)

    # FOR DEBUGGING PURPOSES
    @app.route('/test_entity_batch')
    def test_entity_batch():
        print("TESTING: MAKE SURE TO REMOVE THIS ENDPOINT")
        tag_api.batch_doc_entities_command()

    # FOR DEBUGGING PURPOSES
    @app.route('/test_graph_build')
    def test_graph_build():
        print("TESTING: MAKE SURE TO REMOVE THIS ENDPOINT")
        tag_api.build_graph_from_db_command()

    return app
