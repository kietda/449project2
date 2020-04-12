#designing a web application with python and flask

from flask import Flask, jsonify, request
from flask import abort, make_response
from datetime import datetime
import sqlite3
    
app = Flask(__name__)
app.config["DEBUG"] = True

conn = sqlite3.connect('project1.db')
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
    return "Hello everyone accessing our project 1!"

#temporary operation, delete later
@app.route('/todo/api/v1.0/users', methods = ['GET'])
def get_users():
    conn = sqlite3.connect('project1.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_users = cur.execute('SELECT * FROM users;').fetchall()
    conn.commit()
    conn.close()
    return jsonify(all_users)  

#Create user
@app.route('/todo/api/v1.0/users',methods=['POST'])
def create_user():
    if not request.json or not 'username' in request.json \
        or not 'email' in request.json \
        or not 'karma' in request.json:        
        abort(400)
    conn = sqlite3.connect('project1.db')
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

#update email
@app.route('/todo/api/v1.0/users', methods=['PUT'])
def update_email():
    email = request.json['email']
    username = request.json['username']
    to_filter = []
    to_filter.append(email)
    to_filter.append(username)    
    conn = sqlite3.connect('project1.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()         
    query = "UPDATE users SET email=? WHERE username=?;"
    cur.execute(query,to_filter)
    conn.commit()
    conn.close()
    return jsonify({'result':True}),200

#Increment Karma
@app.route('/todo/api/v1.0/users/inckarma', methods=['PUT'])
def inc_karma():
    username = request.json['username']
    to_filter = []
    to_filter.append(username)
    
    #get the karma of user
    conn = sqlite3.connect('project1.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    results = cur.execute('SELECT * FROM users WHERE username=?;',to_filter).fetchall()
    
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
@app.route('/todo/api/v1.0/users/deckarma', methods=['PUT'])
def dec_karma():
    username = request.json['username']
    to_filter = []
    to_filter.append(username)
    
    #get the karma of user
    conn = sqlite3.connect('project1.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    results = cur.execute('SELECT * FROM users WHERE username=?;',to_filter).fetchall()
    
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
@app.route('/todo/api/v1.0/users/deactivate', methods=['PUT'])
def deactivate():
    username = request.json['username']
    to_filter = []
    to_filter.append(username)
    conn = sqlite3.connect('project1.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()   
    query = "UPDATE users SET activated=0 WHERE username=?;"
    cur.execute(query,to_filter)
    conn.commit()
    conn.close()
    return jsonify({'result':True}),200

if __name__ == '__main__':
    app.run(port = 5100, debug=True)