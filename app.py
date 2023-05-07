import mimetypes
import pathlib
import sqlite3

from flask import Flask, request, redirect

DB_PATH = 'data/db.sqlite3'


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


def get_db(db_path):
    con = sqlite3.connect(db_path)
    con.row_factory = dict_factory
    cur = con.cursor()
    return con, cur


def db_init(db_path):
    inited = pathlib.Path('data/db.sqlite3').exists()
    if not inited:
        con, cur = get_db(db_path)
        with open('store/schema.sql', 'r') as f:
            script = f.read()
        cur.executescript(script)
        con.commit()
        con.close()


db_init(DB_PATH)

mimetypes.add_type('application/javascript', '.js')

app = Flask(__name__, static_url_path='', static_folder='static')


@app.route('/')
def index():
    return redirect('/index.html')


@app.get('/api/db/<string:table>')
def select(table: str):
    args = request.args
    try:
        columns = args.getlist('columns', type=str)
        targets = ', '.join(columns) if len(columns) > 0 else '*'
        args = args.to_dict()
        args.pop('columns', None)
        options = [f'{key} = ?' for key in args.keys()]
        filters = ', '.join(options) if len(options) > 0 else '1'
    except Exception as e:
        print(e)
        return 'Invalid arguments', 400

    query = f'SELECT {targets} FROM {table} WHERE {filters}'
    params = tuple(args.values())

    try:
        con, cur = get_db(DB_PATH)
        cur.execute(query, params)
        rows = cur.fetchall()
    except sqlite3.Error as e:
        print(f'SQLite3 error: {e.args}')
        print(f'Exception class is: {e.__class__}')
        return f'Unknown error: {e.args}', 500
    finally:
        con.close()

    return rows


@app.post('/api/db/<string:table>')
def insert(table: str):
    data = request.json
    try:
        if 'id' in data:
            del data['id']
        keys = ', '.join(data.keys())
        values = ', '.join(['?' for _ in data])
    except Exception as e:
        print(e)
        return 'Invalid arguments', 400

    query = f'INSERT INTO {table} ({keys}) VALUES ({values})'
    params = tuple(data.values())

    try:
        con, cur = get_db(DB_PATH)
        cur.execute(query, params)
        con.commit()
        data = {'lastrowid': cur.lastrowid}
    except sqlite3.Error as e:
        print(f'SQLite3 error: {e.args}')
        print(f'Exception class is: {e.__class__}')
        return f'Unknown error: {e.args}', 500
    finally:
        con.close()

    return data


@app.put('/api/db/<string:table>')
def update(table: str):
    data = request.json
    try:
        if 'id' not in data:
            return 'Id not found', 400
        else:
            id = data['id']
            del data['id']
        pairs = ', '.join([f'{key} = ?' for key in data.keys()])
    except Exception as e:
        print(e)
        return 'Invalid arguments', 400

    query = f'UPDATE {table} SET {pairs} WHERE id = ?'
    params = tuple(data.values()) + (id,)

    try:
        con, cur = get_db(DB_PATH)
        cur.execute(query, params)
        con.commit()
        data = {'rowcount': cur.rowcount}
    except sqlite3.Error as e:
        print(f'SQLite3 error: {e.args}')
        print(f'Exception class is: {e.__class__}')
        return f'Unknown error: {e.args}', 500
    finally:
        con.close()

    return data


@app.delete('/api/db/<string:table>')
def delete(table: str):
    data = request.json
    try:
        if 'ids' not in data:
            return 'Ids not found', 400
        else:
            ids = data['ids']
        conds = ', '.join([str(id) for id in ids])
    except Exception as e:
        print(e)
        return 'Invalid arguments', 400

    query = f'DELETE FROM {table} WHERE id in ({conds})'
    params = ()

    try:
        con, cur = get_db(DB_PATH)
        cur.execute(query, params)
        con.commit()
        data = {'rowcount': cur.rowcount}
    except sqlite3.Error as e:
        print(f'SQLite3 error: {e.args}')
        print(f'Exception class is: {e.__class__}')
        return f'Unknown error: {e.args}', 500
    finally:
        con.close()

    return data
