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
    return "Hello everyone for accessing our posts api!"

#get all posts  //delete later
@app.route('/todo/api/v1.0/get', methods = ['GET'])
def get_allposts():
    conn = sqlite3.connect('project.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_posts = cur.execute('SELECT * FROM posts;').fetchall()
    conn.commit()
    conn.close()
    return jsonify(all_posts)    

#since a web service client applications will expect that we always
#respond with JSON, so we need to improve our 404 error handler
# @app.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({'error:':'Not found'}), 404)

#create a new post => concurrently create a row with this post_id in a votes table
@app.route('/todo/api/v1.0/create',methods=['POST'])
def create_post():
    if not request.json or not 'title' in request.json \
        or not 'text' in request.json \
        or not 'community' in request.json \
        or not 'username' in request.json:        
        abort(400)
        
    pusername = request.json['username']
    to_filter = []
    to_filter.append(pusername)
    conn = sqlite3.connect('project.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    #check if username exists in users table
    results = cur.execute('SELECT * FROM users WHERE username=?;',to_filter).fetchall()
    if len(results)==0:
        conn.close()
        abort(409)
    if int(results[0]['activated']) == 0:    #this username is not actiavted
        conn.close()
        abort(409)        
    ptitle = request.json['title']
    ptext = request.json['text']
    pcommunity =request.json['community']
    purl = request.json.get('url',"")    
    pdate = request.json.get('date',datetime.date(datetime.now()))
    query = "INSERT INTO posts (title, text, community, url, username, date) VALUES (?,?,?,?,?,?);"
    to_filter2 = []
    to_filter2.append(ptitle)
    to_filter2.append(ptext)
    to_filter2.append(pcommunity)
    to_filter2.append(purl)
    to_filter2.append(pusername)
    to_filter2.append(pdate)    
    results = cur.execute(query, to_filter2)
    # conn.commit()
    results = cur.execute("SELECT * FROM posts ORDER BY id DESC limit 1;").fetchall()
    ppostid = results[0]['id']
    query = "INSERT INTO votes (postid) VALUES (?);"
    to_filter3 = []
    to_filter3.append(ppostid)
    results = cur.execute(query, to_filter3)
    conn.commit()
    conn.close()
    return jsonify({'post':True}),201

#delete an existing post
@app.route('/todo/api/v1.0/delete/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    conn = sqlite3.connect('project.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()    
    to_filter = []
    to_filter.append(post_id)
    query = "SELECT * FROM posts WHERE id=?;"
    results = cur.execute(query, to_filter).fetchall()
    if len(results)==0:        
        conn.close()
        abort(404)
    query = "DELETE FROM votes WHERE postid=?;" # rows in votes table depends on row in posts table
    cur.execute(query,to_filter).fetchall()
    query = "DELETE FROM posts WHERE id=?;"
    cur.execute(query,to_filter).fetchall()
    conn.commit()
    conn.close()
    return jsonify({'result':True}),200

#Retrieve an existing post
@app.route('/todo/api/v1.0/get/<int:post_id>', methods=['GET'])
def get_post(post_id):
    conn = sqlite3.connect('project.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    query = "SELECT * FROM posts WHERE id=?;"
    to_filter = []
    to_filter.append(post_id)
    results = cur.execute(query, to_filter).fetchall()
    conn.commit()
    conn.close()     
    if len(results)==0:
        abort(404)       
    return jsonify(results),200

# get the latest postid => for testing
@app.route('/todo/api/v1.0/getlatest',methods=['GET'])
def get_latest_postid():
    conn = sqlite3.connect('project.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    query = "SELECT id FROM posts ORDER BY id DESC LIMIT 1;"
    results = cur.execute(query).fetchall()
    conn.commit()
    conn.close()
    if len(results)==0:
        return ("-1")
    return str(results[0]['id'])

#List the n most recent posts to a particular community
@app.route('/todo/api/v1.0/get/recent/<community_name>/<posts_amount>', methods=['GET'])
def get_community_recent_post(community_name, posts_amount):
    conn = sqlite3.connect('project.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    query = "SELECT id, title, community, username, date FROM posts WHERE community=? ORDER BY id DESC limit ?;"
    to_filter = []
    to_filter.append(community_name)
    to_filter.append(posts_amount)
    results = cur.execute(query, to_filter).fetchall()
    conn.commit()
    conn.close() 
    if len(results)==0:
        abort(404)
    return jsonify(results),200

#List the n most recent posts to any community
@app.route('/todo/api/v1.0/get/recent/<posts_amount>', methods=['GET'])
def get_any_recent_post(posts_amount):
    conn = sqlite3.connect('project.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    query = "SELECT id, title, community, username, date FROM posts ORDER BY id DESC limit ?;"
    to_filter = []
    to_filter.append(posts_amount)
    results = cur.execute(query, to_filter).fetchall()
    conn.commit()
    conn.close()         
    if len(results)==0:
        abort(404)
    return jsonify(results),200

if __name__ == '__main__':
    app.run(debug=True)