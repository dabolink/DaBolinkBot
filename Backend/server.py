from datetime import timedelta
from flask import Flask, jsonify, make_response, request, current_app
import multiprocessing
from functools import update_wrapper
import sqlite3
import Controller
import Objects.Queues

channels = []
app = Flask(__name__)

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        f.required_methods = ["OPTIONS"]
        return update_wrapper(wrapped_function, f)
    return decorator

@app.route("/")
def index():
    return "Welcome to DaBolinkBot"

@app.route('/dabolinkbot/api/v1.0/bot/start/<channel>')
def bot_start(channel):
    if not channel:
        return jsonify({'result': 'failure'})
    try:
        for c in channels:
            if c[0] == channel:
                print "bot already in channel"
                return jsonify({'result': 'failure', 'message': 'bot already in channel'})
        print "started bot in ", channel
        q = Objects.Queues.queues()
        p = multiprocessing.Process(target=Controller.startup, args=(channel, True, q))
        p.start()
        print channels
        channels.append((channel, p, q))
        print channels
        return jsonify({'result': 'success'})
    except:
        return jsonify({'result': 'failure'})

@app.route('/dabolinkbot/api/v1.0/bot/end/<channel>')
def bot_end(channel):
    for c in channels:
        if c[0] == channel:
            print "ending bot in", c[0]
            c[2].kill_queue.put(("",))
            print channels
            channels.remove(c)
            print "remove", channel, "from channel"
            print channels
            return jsonify({'result': 'success'})
    return jsonify({'result': 'failure'})

@app.route('/dabolinkbot/api/v1.0/bot/status/<channel>')
def bot_status(channel):
    for c in channels:
        if c[0] == channel:
            if c[1].is_alive():
                return jsonify({'online': True})
            else:
                channels.remove(c)
                print channels
    return jsonify({'online': False})

@app.route('/dabolinkbot/api/v1.0/channel/<channel>/<user>')
def get_channel_userstats(channel, user):
    conn = sqlite3.connect("Database/Databases/{}.db".format(channel))
    cur = conn.cursor()
    if not user:
        return jsonify({'result': 'failure'})
    result = cur.execute("SELECT * FROM Users WHERE user = ?", (user,)).fetchone()
    if result:
        return jsonify({
            "user": result[0],
            channel: {
                "hours": result[1],
                "credits": result[2],
                "lines_of_text": result[3]
            }
        })
    return make_response(jsonify({'error': 'User Not found'}), 404)

@crossdomain(origin="*")
@app.route('/dabolinkbot/api/v1.0/channel/settings/<channel>', methods=["GET", "POST", "OPTIONS"])
def get_channel_settings(channel):
    print "here"
    conn = sqlite3.connect("Database/Master.db")
    cur = conn.cursor()
    print "request",request
    if request.method == 'GET':
        result = cur.execute("SELECT * FROM Channels WHERE channel = ?", (channel,)).fetchone()
        if not result:

            res = cur.execute('PRAGMA table_info(Channels)').fetchall()
            print res
            defaults = (channel,)
            for val in res:
                print val[4]
                if val[4]:
                    defaults += (val[4],)
            print defaults
            cur.execute("""INSERT INTO Channels VALUES (?, ?, ?, ?)""", defaults)
            conn.commit()
            result = cur.execute("SELECT * FROM Channels WHERE channel = ?", (channel,)).fetchone()
        j = {
            "channel": result[0],
            "timeout_time": result[1],
            "freq_viewer_time": result[2],
            "follow_message": result[3]
        }
        return jsonify(j)
    if request.method == 'POST':
        result = request.json
        if not result:
            return make_response(jsonify({'error': 'JSON not found'}), 404)
        if "timeout_time" not in result and "freq_viewer_time" not in result and "follow_message" not in result:
            return make_response(jsonify({'error': 'JSON missing values'}))
        if "timeout_time" in result:
            cur.execute("""UPDATE Channels SET timeout_time = ? WHERE channel = ?""", (result['timeout_time'], channel))
        if "freq_viewer_time" in result:
            cur.execute("""UPDATE Channels SET freq_viewer_time = ? WHERE channel = ?""", (result["freq_viewer_time"], channel))
        if "follow_message" in result:
            cur.execute("""UPDATE Channels SET folow_message = ? WHERE channel = ?""", (result["follow_message"], channel))
        conn.commit()
        return jsonify({'result': 'success'})
    if request.method == "OPTIONS":
        print "options!"
        response = app.make_default_options_response()
        print response
        print response
        return response
    if not channel:
        return make_response(jsonify({'error': 'Channel not found'}), 404)

@app.route("/dabolinkbot/api/v1.0/user/<user>")
def get_userstats(user):
    import glob
    print glob.glob('./*')
    read_channels = []
    for database in glob.glob('Database/Databases/*.db'):
        print database
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        print database[19:-3]
        result = cur.execute("SELECT * FROM Users WHERE user = ?", (user,)).fetchone()
        if result:
            channelJSON = dict()
            channelJSON[database[19:-3]] = {
                "hours": result[1],
                "credits": result[2],
                "lines of text": result[3],
            }
            read_channels.append(channelJSON)
    if not read_channels == []:
        return jsonify({
            "user": user,
            "channels": read_channels
        })
    else:
        return make_response(jsonify({'error': 'User Not found'}), 404)

@app.errorhandler(404)
def not_found(error):
    print error
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    app.debug = True
    # app.run()
    app.run(host='0.0.0.0')