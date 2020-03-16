import pandas as pd
from flask import Flask, request
from flask_restplus import Api, Resource, fields


app = Flask(__name__)
api = Api(app)

book_model = api.model('Book', {
    'Flickr_URL': fields.String,
    'Publisher': fields.String,
    'Author': fields.String,
    'Title': fields.String,
    'Date_of_Publication': fields.Integer,
    'Identifier': fields.Integer,
    'Place_of_Publication': fields.String
})


@api.route('/book/<int:id>')
class Books(Resource):
    def get(self, id):
        if id not in df.index:
            api.abort(404, "Book {} doesn't exist".format(id))

        book = dict(df.loc[id])
        return book

    def delete(self, id):
        if id not in df.index:
            api.abort(404, "Book {} doesn't exist".format(id))

        df.drop(id, inplace=True)
        return {'Note': 'Book {} has been removed'.format(id)}

    @api.expect(book_model)
    def put(self, id):
        if id not in df.index:
            api.abort(404, "Book {} doesn't exist".format(id))

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
