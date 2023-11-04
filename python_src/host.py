from flask import Flask, request, g, render_template, abort, redirect, send_from_directory
from os.path import join, exists
import os
import sqlite3
from common import kill_all, run_hook
from shutil import copytree
from random import randint
import signal


app = Flask(__name__, static_folder=None)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('db.sqlite')
    return db


@app.teardown_appcontext
def close_connection(exception):  # noqa
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    conn = get_db()
    cur = conn.execute(query, args)
    result = cur.fetchall()
    conn.commit()
    cur.close()
    return (result[0] if result else None) if one else result


connection = sqlite3.connect('db.sqlite')
with open('schema.sql') as f:
    connection.executescript(f.read())
connection.commit()
connection.close()


ALLOWED = 'abcdefghijklmnopqrstuvwxyz0123456789/.-_'


def new_computer(computer_id):
    path = join(app.root_path, 'drives', computer_id)
    if not exists(path):
        copytree(join(app.root_path, 'drives/example'), path)
    result = query_db('SELECT id FROM computers WHERE id=?', (computer_id,), True)
    if not result:
        query_db('INSERT INTO computers VALUES (?, ?, ?, ?)', (computer_id, 1, 0, randint(10_000_000, 99_999_999)))


def get_computer_path(computer_id):
    return join(app.root_path, 'drives', computer_id)


@app.before_request
def before_request():
    if request.full_path.startswith('/api/') and ('CreateComputers' not in request.user_agent.string):
        return {'error': 'access denied'}, 401


@app.route('/ping', methods=['GET'])
def route_ping():
    return {'name': 'Create: Computers', 'copyright': 'Copyright 2023 Merkli', 'license': 'MIT License',
            'version': '0.0.1-1.19.2'}, 200


@app.route('/api/computer/new', methods=['POST'])
def route_api_computer_new():
    data = request.json()
    computer_id = f"{data['dim']}_{data['x']}_{data['y']}_{data['z']}"
    new_computer(computer_id)
    return {'success': 'success'}, 200


@app.route('/api/computer/start', methods=['POST'])
def route_api_computer_start():
    data = request.json()
    computer_id = f"{data['dim']}_{data['x']}_{data['y']}_{data['z']}"
    new_computer(computer_id)
    result = query_db('SELECT running FROM computers WHERE id=?', (computer_id,), True)
    if result[0] == 0:
        query_db('UPDATE computers SET running=1 WHERE id=?', (computer_id,))
        run_hook(app.root_path, computer_id, 'boot')
    return {'success': 'success'}, 200


@app.route('/api/computer/stop', methods=['POST'])
def route_api_computer_stop():
    data = request.json()
    computer_id = f"{data['dim']}_{data['x']}_{data['y']}_{data['z']}"
    result = query_db('SELECT running FROM computers WHERE id=?', (computer_id,), True)
    if result:
        query_db('UPDATE computers SET running=1 WHERE id=?', (computer_id,))
    kill_all(computer_id)
    return {'success': 'success'}, 200


@app.route('/api/stop', methods=['GET'])
def route_api_stop():
    kill_all()
    os.kill(os.getpid(), signal.SIGINT)
    return {'success': 'success'}, 200


@app.route('/api/start', methods=['GET'])
def route_api_start():
    result = query_db('SELECT id FROM computers WHERE running=1')
    for computer_id in result:
        run_hook(app.root_path, computer_id[0], 'boot')
    return {'success': 'success'}, 200


@app.route('/api/computer/id', methods=['POST'])
def route_api_computer_id():
    data = request.json()
    computer_id = f"{data['dim']}_{data['x']}_{data['y']}_{data['z']}"
    result1 = query_db('SELECT id FROM computers WHERE id=?', (computer_id,), True)
    if not result1:
        new_computer(computer_id)
    result2 = query_db('SELECT web FROM computers WHERE id=?', (computer_id,), True)
    return {'success': 'success', 'data': result2[0]}, 200


@app.route('/', methods=['GET'])
def route_():
    return render_template('_root.html')


@app.route('/post', methods=['POST'])
def route_post():
    web = request.form.get('id')
    type_ = request.form.get('id')
    match type_:
        case 'computer':
            result = query_db('SELECT id FROM computers WHERE web=?', (web,), True)
            if not result:
                abort(404)
            return redirect(f"/device/computer/{web}")
    abort(404)


@app.route('/device/computer/<web>', methods=['GET'])
def route_device_computer(web):
    result = query_db('SELECT id, running FROM computers WHERE web=?', (web,), True)
    if not result:
        abort(404)
    return render_template('device_computer.html', computer_id=result[0], running=result[1])


@app.route('/device/computer/<web>/upload', methods=['POST'])
def route_device_computer_upload(web):
    result = query_db('SELECT id FROM computers WHERE web=?', (web,), True)
    if not result:
        abort(404)
    path = request.form['path']
    file = request.files['file']
    if not file.filename:
        abort(400)
    if not all(c in ALLOWED for c in path):
        abort(400)
    if '..' in path:
        abort(400)
    file.save(join(get_computer_path(result[0]), path))
    return redirect('/device/computer/' + web)


@app.route('/device/computer/<web>/files/<path:path>', methods=['GET'])
def route_device_computer_files(web, path):
    result = query_db('SELECT id FROM computers WHERE web=?', (web,), True)
    if not result:
        abort(404)
    file = join(get_computer_path(result[0]), path)
    if not exists(file):
        abort(404)
    if os.path.isdir(file):
        files = os.listdir(file)
        return render_template('_listdir.html', file=file, web=web, files=files)
    if os.path.isfile(file):
        return send_from_directory(get_computer_path(result[0]), path)
    abort(400)


@app.route('/device/computer/<web>/start', methods=['GET'])
def route_device_computer_start(web):
    result = query_db('SELECT id, running FROM computers WHERE web=?', (web,), True)
    if not result:
        abort(404)
    if result[1] == 0:
        query_db('UPDATE computers SET running=1 WHERE id=?', (result[0],))
        run_hook(app.root_path, result[0], 'boot')
        return redirect('/device/computer/' + web)
    abort(400)


@app.route('/device/computer/<web>/stop', methods=['GET'])
def route_device_computer_stop(web):
    result = query_db('SELECT id FROM computers WHERE web=?', (web,), True)
    if not result:
        abort(404)
    query_db('UPDATE computers SET running=0 WHERE id=?', (result[0],))
    kill_all(result[1])
    return redirect('/device/computer/' + web)


if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=25000)
    except RuntimeError as e:
        print(e)

