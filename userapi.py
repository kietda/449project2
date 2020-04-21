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
    return "Hello everyone for accessing our users api!"

# get all user, // delete later
@app.route('/todo/api/v1.0/get', methods = ['GET'])
def get_users():
    conn = sqlite3.connect('project.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_users = cur.execute('SELECT * FROM users;').fetchall()
    conn.commit()
    conn.close()
    return jsonify(all_users)  

#Create user
@app.route('/todo/api/v1.0/create',methods=['POST'])
def create_user():
    if not request.json or not 'username' in request.json \
        or not 'email' in request.json \
        or not 'karma' in request.json:        
        abort(400)
    conn = sqlite3.connect('project.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()    
    # conn.commit()           
    username = request.json['username']
    email = request.json['email']
    karma =request.json['karma']
    activated = 1;
    query = "INSERT INTO users (username, email, karma, activated) VALUES (?,?,?,?);"
    to_filter2 = []
    to_filter2.append(username)
    to_filter2.append(email)
    to_filter2.append(karma)
    to_filter2.append(activated)  
    try:
        results = cur.execute(query, to_filter2)
        conn.commit()
        conn.close()
        return jsonify({'post':True}),201
    except:
        conn.close()
        abort(409)
        
# get the latest userid => for testing
@app.route('/todo/api/v1.0/getlatest',methods=['GET'])
def get_latest_userid():
    conn = sqlite3.connect('project.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    query = "SELECT userid FROM users ORDER BY userid DESC LIMIT 1;"
    results = cur.execute(query).fetchall()
    conn.commit()
    conn.close()
    if len(results)==0:
        return ("-1")
    return str(results[0]['userid'])

#update email
@app.route('/todo/api/v1.0/updatemail', methods=['PUT'])
def update_email():
    email = request.json['email']
    username = request.json['username']
    to_filter = []
    to_filter.append(email)
    to_filter.append(username)
    to_filter2 = []
    to_filter2.append(username)
    conn = sqlite3.connect('project.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    results = cur.execute('SELECT * FROM users WHERE username=?;',to_filter2).fetchall()
    if len(results)==0:
        conn.commit()
        conn.close()
        abort(404)
    query = "UPDATE users SET email=? WHERE username=?;"
    results = cur.execute(query,to_filter).fetchall()
    conn.commit()
    conn.close()
    return jsonify({'result':True}),200

#Increment Karma
@app.route('/todo/api/v1.0/update/inckarma', methods=['PUT'])
def inc_karma():
    username = request.json['username']
    to_filter = []
    to_filter.append(username)
    
    #get the karma of user
    conn = sqlite3.connect('project.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    results = cur.execute('SELECT * FROM users WHERE username=?;',to_filter).fetchall()
    if len(results)==0:
        conn.close()
        abort(404)
    inckarma = int(results[0]['karma']) + 1    
    query = "UPDATE users SET karma=? WHERE username=?;"
    to_filter2 = []
    to_filter2.append(inckarma)
    to_filter2.append(username)
    cur.execute(query,to_filter2)
    conn.commit()
    conn.close()
    return jsonify({'result':True}),200

#Decrement Karma
@app.route('/todo/api/v1.0/update/deckarma', methods=['PUT'])
def dec_karma():
    username = request.json['username']
    to_filter = []
    to_filter.append(username)
    
    #get the karma of user
    conn = sqlite3.connect('project.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    results = cur.execute('SELECT * FROM users WHERE username=?;',to_filter).fetchall()
    if len(results)==0:
        conn.close()
        abort(404)
    inckarma = int(results[0]['karma']) - 1    
    query = "UPDATE users SET karma=? WHERE username=?;"
    to_filter2 = []
    to_filter2.append(inckarma)
    to_filter2.append(username)
    cur.execute(query,to_filter2)
    conn.commit()
    conn.close()
    return jsonify({'result':True}),200

#Deactivate account
@app.route('/todo/api/v1.0/account/deactivate', methods=['PUT'])
def deactivate():
    username = request.json['username']
    to_filter = []
    to_filter.append(username)
    conn = sqlite3.connect('project.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    results = cur.execute('SELECT * FROM users WHERE username=?;',to_filter).fetchall()
    if len(results)==0:
        conn.close()
        abort(404)
    query = "UPDATE users SET activated=0 WHERE username=?;"
    results = cur.execute(query,to_filter).fetchall()
    conn.commit()
    conn.close()
    return jsonify({'result':True}),200

if __name__ == '__main__':
    app.run(debug=True)