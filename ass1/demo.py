import requests
import sqlite3
from sqlite3 import Error
from flask import Flask, request
from flask_restplus import Api, Resource, fields
import json
import datetime


def create_table(db_file):
    try:
        con = sqlite3.connect(db_file)
        c = con.cursor()
        c.execute('''CREATE TABLE if not exists WorldBank
        (collection_id integer primary key autoincrement,
        indicator_id text,
        indicator_value text,
        creation_time text,
        entries text);''')
    except Error as e:
        print(e)
    finally:
        con.commit()
        con.close()


app = Flask(__name__)
api = Api(app, default='Collections', title='WorldBank Database',
          description='This is the Flask-Restplus data service that '
                      'allows a client to read and store collections from WorldBand Database.')

indicator_type = api.model('indicators', {'indicator_id': fields.String})


@api.route('/collections')
class DataWithoutID(Resource):
    @api.response(404, 'Invalid indicator id.')
    @api.response(400, 'Wrong DataType.')
    @api.response(200, 'Data has already imported.')
    @api.response(201, 'Created')
    @api.expect(indicator_type)
    @api.doc(description='Import a collection from the data service.')
    def post(self):

        try:
            indicator_id_json = request.json
        except:
            return {'message': "Wrong DataType"}, 400

        try:
            indicator_id = indicator_id_json['indicator_id']
        except KeyError:
            return {'message': 'Wrong DataType.'}, 400

        url = 'http://api.worldbank.org/v2/countries/all/' \
              'indicators/{}?date=2012:2017&format=json&per_page=1000'.format(indicator_id)
        r = requests.get(url)

        # if indicator_id doesn't exist
        if 'message' in r.json()[0]:
            return {'message': "The input indicator {} doesn't exist.".format(indicator_id)}, 404

        con = sqlite3.connect(db_file)
        c = con.cursor()

        # if indicator_id has already imported
        c.execute('select indicator_id from WorldBank')
        indicator_id_list = [r[0] for r in c.fetchall()]
        if indicator_id in indicator_id_list:
            return {'message': "The input indicator '{}' has already imported.".format(indicator_id)}, 200

        # if indicator_id is valid
        data = r.json()[1]
        temp = {}
        temp['entries'] = []
        for record in data:
            temp['indicator_id'] = record['indicator']['id']
            temp['indicator_value'] = record['indicator']['value']
            entity = {}
            entity['country'] = record['country']['value']
            entity['date'] = int(record['date'])
            entity['value'] = record['value']
            if not entity['value'] == None:
                temp['entries'].append(entity)

        i_id = temp['indicator_id']
        i_value = temp['indicator_value']
        creation_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entries = json.dumps(temp['entries'])

        insert_data = [i_id, i_value, creation_time, entries]
        c.execute('insert into WorldBank(indicator_id, indicator_value, creation_time, entries) \
                    values(?, ?, ?, ?)', insert_data)
        con.commit()

        c.execute("select * from WorldBank where indicator_id = '%s'" %indicator_id)
        result = c.fetchall()[0]
        # print(result)
        output = {}
        output['uri'] = '/collection/' + str(result[0])
        output['id'] = result[0]
        output['creation_time'] = result[3]
        output['indicator_id'] = result[1]
        con.close()
        return output, 201

    @api.response(404, 'Invalid input')
    @api.response(200, 'OK')
    @api.param('order_by', '"order_by" is a comma separated string value to \
                sort the collection based on the given criteria. ')
    @api.doc(description='Retrieve the list of available collections according to the order.')
    def get(self):

        order = request.args.get('order_by')
        # print(order)

        con = sqlite3.connect(db_file)
        c = con.cursor()

        if not order == None:
            order_list = order.replace(' ', '').split(',')
            order_sql = ''
            order_dict = {'+id': 'collection_id asc,', '-id': 'collection_id desc,',
                          '+creation_time': 'creation_time asc,', '-creation_time': 'creation_time desc,',
                          '+indicator': 'indicator_id asc,', '-indicator': 'indicator_id desc,'}
            for i in order_list:
                try:
                    order_sql += order_dict[i]
                except KeyError:
                    return {'message': 'Invalid input.'}, 400
            # to remove ',' at the end
            order_sql = order_sql[:-1]
            sql_s = 'select collection_id, indicator_id, creation_time from WorldBank order by ' + order_sql
            # print(sql_s)
            c.execute("%s" %sql_s)
        else:
            c.execute("select collection_id, indicator_id, creation_time from WorldBank")
        result = c.fetchall()

        output = []
        for r in result:
            temp = {}
            temp['uri'] = '/collections/' + str(r[0])
            temp['id'] = r[0]
            temp['creation_time'] = r[2]
            temp['indicator'] = r[1]
            output.append(temp)
        con.close()
        return output, 200


@api.route('/collections/<int:id>')
@api.param('id', 'Indicator id')
class DataWithID(Resource):
    @api.response(200, 'OK')
    @api.response(400, 'Bad request: No such id')
    @api.doc(description='Deleting a collection with the data service.')
    def delete(self, id):
        con = sqlite3.connect(db_file)
        c = con.cursor()
        c.execute("select collection_id from WorldBank")
        records = c.fetchall()
        id_list = []
        for r in records:
            id_list.append(r[0])
        if id in id_list:
            c.execute("delete from WorldBank where collection_id = '%d'" %id)
            con.commit()
            con.close()
            return {"message": "The collection {} was removed from the database!".format(id),
                    "id": id}, 200
        else:
            con.close()
            return {"message": "The collection {} is not in the database!".format(id)}, 400

    @api.response(200, 'OK')
    @api.response(400, 'Bad request: No such id')
    @api.doc(description='Retrieve a collection.')
    def get(self, id):
        con = sqlite3.connect(db_file)
        c = con.cursor()
        c.execute("select collection_id from WorldBank")
        records = c.fetchall()
        id_list = []
        for r in records:
            id_list.append(r[0])
        if id in id_list:
            output = {}
            c.execute("select * from WorldBank where collection_id = '%d'" %id)
            collection = c.fetchall()[0]
            output['id'] = collection[0]
            output['indicator'] = collection[1]
            output['indicator_value'] = collection[2]
            output['creation_time'] = collection[3]
            output['entries'] = json.loads(collection[4])
            con.close()
            return output, 200
        else:
            con.close()
            return {"message": "The collection {} is not in the database!".format(id)}, 400


@api.route('/collections/<int:id>/<int:year>/<string:country>')
@api.param('country', 'Country')
@api.param('year', 'Year')
@api.param('id', 'Indicator id')
class DataWithMulti(Resource):
    @api.response(200, 'OK')
    @api.response(400, 'Bad request')
    @api.doc(description='Retrieve economic indicator value for given country and a year.')
    def get(self, id, year, country):
        con = sqlite3.connect(db_file)
        c = con.cursor()
        c.execute("select collection_id from WorldBank")
        records = c.fetchall()
        id_list = []
        for r in records:
            id_list.append(r[0])
        if id in id_list:
            c.execute("select * from WorldBank where collection_id = '%d'" %id)
            collection = c.fetchall()[0]
            indicator = collection[1]
            entries = json.loads(collection[4])
            for e in entries:
                if e['date'] == year and e['country'] == country:
                    output = {}
                    output['id'] = id
                    output['indicator'] = indicator
                    output['country'] = country
                    output['year'] = year
                    output['value'] = e['value']
                    con.close()
                    return output, 200
            con.close()
            return {"message": "No pair of Year({}) and Country({}) in indicator {}".format(year, country, id)}, 400
        else:
            con.close()
            return {"message": "The collection {} is not in the database!".format(id)}, 400



@api.route('/collections/<int:id>/<int:year>')
@api.param('year', 'Year')
@api.param('id', 'Indicator_id')
class DataWithIdYear(Resource):
    @api.response(200, 'OK')
    @api.response(400, 'Bad request')
    @api.param('q', 'The q should be an integer value between 1 and 100.')
    @api.doc(description='Retrieve top/bottom economic indicator values for a given year.')
    def get(self, id, year):
        con = sqlite3.connect(db_file)
        c = con.cursor()
        c.execute("select collection_id from WorldBank")
        records = c.fetchall()
        id_list = []
        for r in records:
            id_list.append(r[0])
        if id in id_list:
            q = request.args.get('q')
            c.execute("select * from WorldBank where collection_id = '%d'" %id)
            collection = c.fetchall()[0]
            indicator = collection[1]
            indicator_value = collection[2]
            entries = json.loads(collection[4])

            output = {}
            output['indicator'] = indicator
            output['indicator_value'] = indicator_value

            output_entries = []
            for e in entries:
                temp = {}
                if e['date'] == year:
                    temp['country'] = e['country']
                    temp['value'] = e['value']
                    output_entries.append(temp)

            if q == None:
                output['entries'] = output_entries
                con.close()
                return output, 200

            try:
                number = int(q)
            except ValueError:
                con.close()
                return {"message": "Input is not an Integer"}, 400
            reverse = False if '-' in q else True
            output_entries.sort(key=lambda x: x['value'], reverse=reverse)
            output['entries'] = output_entries[:abs(number)]
            con.close()
            return output, 200
        else:
            con.close()
            return {"message": "The collection {} is not in the database!".format(id)}, 400


if __name__ == '__main__':
    db_file = 'z5231733.db'
    create_table(db_file)
    app.run(debug=True)