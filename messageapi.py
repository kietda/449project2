#designing a web application with python and flask

from flask import Flask, jsonify, request
from flask import abort, make_response
from datetime import datetime
import sqlite3
    
app = Flask(__name__)
app.config["DEBUG"] = True

conn = sqlite3.connect('project.db')
cur = conn.cursor()
cur.execute("PRAGMA foreign_keys = 1")
conn.commit()
conn.close()

#let the connection object know to use the dict_factory function, which
#return items from the database as dictionaries rather than lists
#=> these work better when we output them to JSON
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/')
def index():
    return "Hello everyone for accessing our messages api!"


# send message
@app.route('/todo/api/v1.0/send',methods=['POST'])
def send_message():
    if not request.json or not 'user_from' in request.json \
        or not 'user_to' in request.json \
        or not 'content' in request.json:        
        abort(400)
        
    puser_from = request.json['user_from']
    puser_to = request.json['user_to']
    to_filter = []
    to_filter.append(puser_from)
    to_filter2 = []
    to_filter2.append(puser_to)
    conn = sqlite3.connect('project.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    #check if user_from and user_to exists in users table
    result1 = cur.execute('SELECT * FROM users WHERE username=?;',to_filter).fetchall()
    result2 = cur.execute('SELECT * FROM users WHERE username=?;',to_filter2).fetchall()
    
    if (len(result1)==0) | (len(result2)==0) :  # user_from or user_to does not exist
        conn.close()
        abort(409)
    if int(result1[0]['activated']) == 0:    # sender is not activated
        conn.close()
        abort(409)        
    pcontent = request.json['content']    
    query = "INSERT INTO messages (user_from, user_to, content) VALUES (?,?,?);"
    to_filter2 = []
    to_filter2.append(puser_from)
    to_filter2.append(puser_to)
    to_filter2.append(pcontent)   
    results = cur.execute(query, to_filter2)
    conn.commit()
    conn.close()
    return jsonify({'post':True}),201

# get the latest added message_id => for testing
@app.route('/todo/api/v1.0/getlatest',methods=['GET'])
def get_latest_messageid():
    conn = sqlite3.connect('project.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    query = "SELECT message_id FROM messages ORDER BY message_id DESC LIMIT 1;"
    results = cur.execute(query).fetchall()
    conn.commit()
    conn.close()
    if len(results)==0:
        return ("-1")
    return str(results[0]['message_id'])

# delete message
@app.route('/todo/api/v1.0/delete/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    conn = sqlite3.connect('project.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()    
    to_filter = []
    to_filter.append(message_id)
    query = "SELECT * FROM messages WHERE message_id=?;"
    results = cur.execute(query, to_filter).fetchall()
    if len(results)==0:        
        conn.close()
        abort(404)     
    query = "DELETE FROM messages WHERE message_id=?;"
    cur.execute(query,to_filter).fetchall()
    conn.commit()
    conn.close()
    return jsonify({'result':True}),200

#set favorite message
@app.route('/todo/api/v1.0/setfavorite', methods=['PUT'])
def set_favorite_message():
    pmessage_id = request.json['message_id']
    to_filter = []
    to_filter.append(pmessage_id)  
    conn = sqlite3.connect('project.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    query = "SELECT * FROM messages WHERE message_id=?;"
    results = cur.execute(query, to_filter).fetchall()
    if len(results)==0:        
        conn.close()
        abort(404) 
    query = "UPDATE messages SET flag= 1 WHERE message_id=?;"
    cur.execute(query,to_filter)
    conn.commit()
    conn.close()
    return jsonify({'result':True}),200

# get favorite message
@app.route('/todo/api/v1.0/get/favorite/<user_to>', methods=['GET'])
def get_favorite_message(user_to):
    conn = sqlite3.connect('project.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    to_filter = []
    to_filter.append(user_to)
    query = "SELECT * FROM users WHERE username=?;"
    results = cur.execute(query, to_filter).fetchall()
    if len(results)==0:
        conn.close() 
        abort(404)    
    query = "SELECT * FROM messages WHERE user_to=? AND flag = 1;"
    results = cur.execute(query,to_filter).fetchall()
    conn.commit()
    conn.close() 
    return jsonify(results),200


if __name__ == '__main__':
    app.run(debug=True)