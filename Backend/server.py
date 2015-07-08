from flask import Flask, jsonify, make_response
import multiprocessing
import sqlite3
import Controller
import Objects.Queues

channels = []
app = Flask(__name__)

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
                return jsonify({'result': 'failure', 'message': 'bot already in channel'})
        print "started bot in ", channel
        q = Objects.Queues.queues()
        p = multiprocessing.Process(target=Controller.startup, args=(channel, True, q))
        p.start()
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
            del c
            print channels
            return jsonify({'result': 'success'})
    return jsonify({'result': 'failure'})

@app.route('/dabolinkbot/api/v1.0/bot/status/<channel>')
def bot_status(channel):
    for c in channels:
        if c[0] == channel:
            return jsonify({'online': True})
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
    app.run(debug=True)