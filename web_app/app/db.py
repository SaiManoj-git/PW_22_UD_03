from flask import current_app, g
from werkzeug.local import LocalProxy

from pymongo import MongoClient, DESCENDING, ASCENDING
from pymongo.write_concern import WriteConcern
from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.objectid import ObjectId
from bson.errors import InvalidId
from pymongo.read_concern import ReadConcern

def get_db():
    """
    Configuration method to return db instance
    """
    db = getattr(g, "_database", None)
    IMGRES_DB_URI = current_app.config["IMGRES_DB_URI"]
    IMGRES_DB_NAME = current_app.config["IMGRES_NS"]
    if db is None:
        """
        Timeouts

        prevent the program from waiting indefinitely by setting the write concern timeout limit to 2500 milliseconds.
        """
        db = g._database = MongoClient(
        IMGRES_DB_URI,
        # TODO: Connection Pooling
        # Set the maximum connection pool size to 50 active connections.
        # TODO: Timeouts
        # Set the write timeout limit to 2500 milliseconds.
        )[IMGRES_DB_NAME]
    return db



# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)


# USER MANAGEMENT

def get_user(email):
    """
    Given an email, returns a document from the `users` collection.
    """
    # TODO: User Management
    # Retrieve the user document corresponding with the user's email.
    return db.users.find_one({ "some_field": "some_value" })
