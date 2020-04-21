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
    return "Hello everyone for accessing our votes api!"

# Upvote a post
@app.route('/todo/api/v1.0/upvote', methods=['PUT'])
def upvote():
    ppostid = request.json['postid']
    to_filter = []
    to_filter.append(ppostid)
    #get the upvote of a post
    conn = sqlite3.connect('project.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    results = cur.execute('SELECT * FROM votes WHERE postid=?;',to_filter).fetchall()
    if len(results)==0:
        conn.commit()
        conn.close()
        abort(404)
    pupvote = int(results[0]['upvote']) + 1    
    query = "UPDATE votes SET upvote=? WHERE postid=?;"
    to_filter2 = []
    to_filter2.append(pupvote)
    to_filter2.append(ppostid)
    cur.execute(query,to_filter2)
    conn.commit()
    conn.close()
    return jsonify({'result':True}),200 

# Downvote a post
@app.route('/todo/api/v1.0/downvote', methods=['PUT'])
def downvote():
    ppostid = request.json['postid']
    to_filter = []
    to_filter.append(ppostid)
    conn = sqlite3.connect('project.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    results = cur.execute('SELECT * FROM votes WHERE postid=?;',to_filter).fetchall()
    if len(results)==0:
        conn.commit()
        conn.close()
        abort(404)
    pdownvote = int(results[0]['downvote']) - 1    
    query = "UPDATE votes SET downvote=? WHERE postid=?;"
    to_filter2 = []
    to_filter2.append(pdownvote)
    to_filter2.append(ppostid)
    cur.execute(query,to_filter2)
    conn.commit()
    conn.close()
    return jsonify({'result':True}),200 

# Report the number of upvotes and downvotes for a post
@app.route('/todo/api/v1.0/get/<int:post_id>', methods=['GET'])
def get_updownvote(post_id):
    conn = sqlite3.connect('project.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    query = "SELECT upvote,downvote FROM votes WHERE postid=?;"
    to_filter = []
    to_filter.append(post_id)
    results = cur.execute(query, to_filter).fetchall()
    conn.commit()
    conn.close()     
    if len(results)==0:
        abort(404)
    return jsonify(results),200

# List the n top-scoring posts to any community
@app.route('/todo/api/v1.0/get/top/<posts_amount>', methods=['GET'])
def get_top_posts(posts_amount):
    conn = sqlite3.connect('project.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    query = "SELECT id, title, upvote, downvote FROM posts INNER JOIN votes on posts.id = votes.postid ORDER BY (upvote-downvote) DESC LIMIT ?;"
    to_filter = []
    to_filter.append(posts_amount)
    results = cur.execute(query, to_filter).fetchall()
    conn.commit()
    conn.close()         
    if len(results)==0:
        abort(404)
    return jsonify(results),200

# Given a list of post identifiers, return the list sorted by score.
@app.route('/todo/api/v1.0/sort', methods=['GET'])
def sort_by_score():
    postids = request.json['postids']
    list_postids = postids.split(',')
    if not postids:
        abort(404)
    conn = sqlite3.connect('project.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()   
    query = "SELECT postid, upvote, downvote FROM votes INNER JOIN posts on votes.postid = posts.id WHERE posts.id IN ({seq}) ORDER BY (upvote-downvote) DESC;".format(
    seq=','.join(['?']*len(list_postids)))
    results = cur.execute(query,list_postids).fetchall()
    conn.commit()
    conn.close()
    if len(results)!=len(list_postids):
        abort(404)
    return jsonify(results),200

if __name__ == '__main__':
    app.run(debug=True)