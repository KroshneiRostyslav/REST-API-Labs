from flask import Flask
from flask_restful import Api
from flasgger import Swagger

from app.api.books import (
    BookListResource,
    BookResource
)

app = Flask(__name__)

swagger = Swagger(app)

api = Api(app)

api.add_resource(
    BookListResource,
    "/books"
)

api.add_resource(
    BookResource,
    "/books/<string:book_id>"
)


@app.route("/")
def root():
    return {
        "message": "Library API"
    }


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )