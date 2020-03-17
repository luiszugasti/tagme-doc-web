# Tagme-doc-web
Part of an ongoing project for Ryerson Capstone project EB02.

## Introduction
This repo contains a flask application which allows a user to obtain the
document entities of a set of documents in our Clueweb09 corpus.  
The user only needs to know of the specific document name that they wish
to obtain entities for. Tagme-doc-web caches each specified `documentID :
entity` set inside a Sqlite database server, for faster document entity
retrieval.

More information about the API is below.

## API
The application is structured as a flask application. Hence, there are 
flask command line commands available as well as remote endpoint commands.

### Flask API
#### `db_create`
Initializes the SQLite database with the default models. These models are `User`, `Entity` and `Document`.
#### `db_seed`
Initializes the SQLite database with dummy data.
#### `db_drop`
Drops all the tables created, if they exist.

### Remote API
####`<server>/get_doc_entity/<params: document_names>`
The bread and butter of the API. By calling with any amount of document names, the server will check if each
of them exist within the cached database. For any documents not in the local database, a separate call to TAGME will
be made. Once all documents' entities are available, the server will return the requested entities.  
Hint: the TAGME server itself is somewhat slow, hence, it is advisable that for hundreds of documents, a high timeout
is configured. As more and more documents are cached into the database, this delay is expected to decrease.
The format that the api returns documents is a wrapped dictionary of 
`{documentname : entitie(s) : occurrence of entities}`, as below:

    {
        "clueweb09-en0000-00-15766": {
            "Frost/Nixon (film)": 9,
            "Nixon, Pennsylvania": 1,
            "Frank Langella": 4,
            "Michael Sheen": 4,
            ...
        },
        "clueweb09-en0000-00-18760": {
            "Frost/Nixon (film)": 3,
            "Nixon, Pennsylvania": 2,
            "Frank Langella": 89,
            "Michael Sheen": 4,
            ...
        },
        ...
    }

####`<server>/get_all_doc_entities`
Returns a list of all the cached document entities found in the corpus.

####`<server>/get_all_docs`
Returns a list of all cached document titles found in the corpus. 

##Installation
To get started with the API, first clone this github repo to an appropriate location on your computer.
You will need to run the requirements.txt file with `pip install -r requirements`. Make sure you're in a virtual 
environment!
The project is tested with Python 3.7.