import pandas as pd
from flask import Flask, request
from flask_restplus import Api, Resource, fields, reqparse, inputs
import json


app = Flask(__name__)
api = Api(app, default='Books', title='Book Dataset',
          description='This is just a simple example to show how publish data as a service.')

book_model = api.model('Book', {
    'Flickr_URL': fields.String,
    'Publisher': fields.String,
    'Author': fields.String,
    'Title': fields.String,
    'Date_of_Publication': fields.Integer,
    'Identifier': fields.Integer,
    'Place_of_Publication': fields.String
})

parser = reqparse.RequestParser()
parser.add_argument('order', choices=list(column for column in book_model.keys()))
parser.add_argument('ascending', type=inputs.boolean)


@api.route('/books')
class BookList(Resource):
    @api.response(200, 'Successful')
    @api.doc(description='Get all books')
    def get(self):
        # get books as JSON string
        args = parser.parse_args()

        # retrieve the query parameters
        order_by = args.get('order')
        ascending = args.get('ascending', True)

        if order_by:
            df.sort_values(by=order_by, inplace=True, ascending=ascending)

        json_str = df.to_json(orient='index')

        # convert the string JSON to a real JSON
        ds = json.loads(json_str)

        ret = []
        for idx in ds:
            book = ds[idx]
            book['Identifier'] = int(idx)
            ret.append(book)

        return ret

    @api.response(201, 'Book Created Successfully')
    @api.response(400, 'Validation Error')
    @api.doc(description='Add a new book')
    @api.expect(book_model)
    def post(self):
        book = request.json

        if 'Identifier' not in book:
            return {"message": 'Missing Identifier'}, 400

        id = book['Identifier']
        if id in df.index:
            return {"message": 'Identifier {} is already existed'.format(id)}, 400

        for key in book:
            if key not in book_model.keys():
                return {"message": 'Property {} is invalid'.format(key)}, 400
            # not introduce a new column called 'Identifier'
            if not key == 'Identifier':
                df.loc[id, key] = book[key]
        return {"message": 'Book {} has been added'.format(id)}, 200


@api.route('/book/<int:id>')
@api.param('id', 'The Book identifier')
class Books(Resource):
    @api.response(404, 'Book was not found')
    @api.response(200, 'Successful')
    @api.doc(description="Get a book by its ID")
    def get(self, id):
        if id not in df.index:
            # api.abort(404, "Book {} doesn't exist".format(id))
            return {"message": "Book {} doesn't exist".format(id)}, 404

        book = dict(df.loc[id])
        return book

    @api.response(404, 'Book was not found')
    @api.response(200, 'Successful')
    @api.doc(description="Delete a book by its ID")
    def delete(self, id):
        if id not in df.index:
            # api.abort(404, "Book {} doesn't exist".format(id))
            return {"message": "Book {} doesn't exist".format(id)}, 404

        df.drop(id, inplace=True)
        return {'message': 'Book {} has been removed'.format(id)}, 200

    @api.response(404, 'Book was not found')
    @api.response(200, 'Successful')
    @api.response(400, 'Validation Error')
    @api.doc(description='Update a book by its ID')
    @api.expect(book_model)
    def put(self, id):
        if id not in df.index:
            # api.abort(404, "Book {} doesn't exist".format(id))
            return {"message": "Book {} doesn't exist".format(id)}, 404

        # or use "book = api.payload"
        book = request.json

        if 'Identifier' in book and id != book['Identifier']:
            return {"message": "Identifier {} cannot be changed".format(id)}, 400

        for key in book:
            if key not in book_model.keys():
                return {"message": "Property {} is invalid".format(key)}, 400
            # not introduce a new column called 'Identifier'
            if not key == 'Identifier':
                df.loc[id, key] = book[key]

        return {"message": "Book {} has been updated".format(id)}, 200


if __name__ == '__main__':
    columns_to_drop = ['Edition Statement',
                       'Corporate Author',
                       'Corporate Contributors',
                       'Former owner',
                       'Engraver',
                       'Contributors',
                       'Issuance type',
                       'Shelfmarks'
                       ]
    csv_file = "Books.csv"
    df = pd.read_csv(csv_file)

    # drop unnecessary columns
    df.drop(columns_to_drop, inplace=True, axis=1)

    # clean the date of publication & convert it to numeric data
    new_date = df['Date of Publication'].str.extract(r'^(\d{4})', expand=False)
    new_date = pd.to_numeric(new_date)
    new_date = new_date.fillna(0)
    df['Date of Publication'] = new_date

    # replace spaces in the name of columns
    df.columns = [c.replace(' ', '_') for c in df.columns]

    # set the index column; this will help us to find books with their ids
    df.set_index('Identifier', inplace=True)

    # run the application
    app.run(debug=True)
