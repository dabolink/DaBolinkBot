from flask import Flask, jsonify, make_response
import multiprocessing
import sqlite3
import Controller

channels = []
app = Flask(__name__)

@app.route("/")
def index():
    return "Welcome to DaBolinkBot"

@app.route('/dabolinkbot/api/v1.0/bot/<channel>/<operation>')
def bot_operation(channel, operation):
    if not channel or not operation:
        return jsonify({'result': 'failure'})
    if operation == "start":
        try:
            print "started bot in ", channel
            p = multiprocessing.Process(target=Controller.startup, args=(channel, True))
            p.start()
            channels.append((channel, p))
            print channels
            return jsonify({'result': 'success'})
        except:
            return jsonify({'result': 'failure'})
    #TODO
    # if operation == "end":
    #     print request.json
    #     try:
    #         if not request.json or not 'channel' in request.json:
    #             return jsonify({'result': 'failure'})
    #         return jsonify({'result': 'success'})
    #     except:
    #         return jsonify({'result': 'failure'})

@app.route('/dabolinkbot/api/v1.0/channel/<channel>/<user>/')
def get_channel_userstats(channel, user):
    conn = sqlite3.connect("Database/Databases/{}.db".format(channel))
    cur = conn.cursor()
    if not user:
        return jsonify({'result': 'failure'})
    result = cur.execute("SELECT * FROM Users WHERE user = ?", (user,)).fetchone()
    return jsonify({
        "user": result[0],
        channel: {
            "hours": result[1],
            "credits": result[2],
            "lines_of_text": result[3]
        }
    })
    pass
# @app.route('/todo/api/v1.0/user/get', methods=['GET'])
# def get_tasks():
#     return jsonify({'tasks': tasks})
#
# @app.route('/todo/api/v1.0/tasks/post', methods=['POST'])
# def create_task():
#     print request.json
#     if not request.json or not 'title' in request.json:
#         abort(400)
#     task = {
#         'id': tasks[-1]['id'] + 1,
#         'title': request.json['title'],
#         'description': request.json.get('description', ""),
#         'done': False
#     }
#     tasks.append(task)
#     return jsonify({'task': task}), 201
@app.route("/dabolinkbot/api/v1.0/user/<user>")
def get_userstats(user):
    import glob
    print glob.glob('./*')
    channels = []
    for database in glob.glob('Database/Databases/*.db'):
        print database
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        print database[19:-3]
        result = cur.execute("SELECT * FROM Users WHERE user = ?", (user,)).fetchone()
        if result:
            channelJSON = {}
            channelJSON[database[19:-3]] = {
                "hours": result[0],
                "credits": result[1],
                "lines of text": result[2],
            }
            channels.append(channelJSON)
    if not channels == {}:
        return jsonify({
            "user": user,
            "channels": channels
        })
    else:
        return make_response(jsonify({'error': 'User Not found'}), 404)


@app.errorhandler(404)
def not_found(error):
    print error
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    app.run(debug=True)