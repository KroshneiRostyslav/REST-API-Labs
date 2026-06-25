from flask import request
from flask_restful import Resource

from app.dependencies import get_book_service

service = get_book_service()


class BookListResource(Resource):

  def get(self):
    """
    Get all books
    ---
    tags:
      - Books

    parameters:
      - name: limit
        in: query
        type: integer

      - name: offset
        in: query
        type: integer

    responses:
      200:
        description: Books list
    """

    limit = int(
        request.args.get("limit", 10)
    )

    offset = int(
        request.args.get("offset", 0)
    )

    result = service.get_all_books(
        limit,
        offset
    )

    return result, 200

  def post(self):
    """
    Create book
    ---
    tags:
      - Books

    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
              example: Test name

            author:
              type: string
              example: Super author

            year:
              type: integer
              example: 2020

          required:
            - title
            - author

    responses:
      201:
        description: Book created
    """

    data = request.get_json()

    result = service.add_book(data)

    return result, 201


class BookResource(Resource):

  def get(self, book_id):
      """
      Get book by id
      ---
      tags:
        - Books

      parameters:
        - name: book_id
          in: path
          required: true

      responses:
        200:
          description: Book
        404:
          description: Not found
      """

      book = service.get_book_by_id(
          book_id
      )

      if not book:
          return {
              "message": "Book not found"
          }, 404

      return book, 200

  def delete(self, book_id):
      """
      Delete book
      ---
      tags:
        - Books

      parameters:
        - name: book_id
          in: path
          required: true

      responses:
        204:
          description: Deleted
      """

      service.delete_book_by_id(
          book_id
      )

      return "", 204