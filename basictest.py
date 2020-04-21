import requests
import sqlite3



CPASS = '\033[94m'
CFAIL = '\033[32m'
CEND = '\033[0m'

def post_microservice():
    print('POST MICRO SERVICE')
    print('1. Create new post:')
    apost = {"title":"Socimedia","text":"Reddit ran wild with Boston bombing conspiracy theories in 2013","community":"Technology", "url":"https://www.theverge.com/tech","username":"tester2"}
    resp = requests.post('http://localhost:2015/posts/todo/api/v1.0/create', json=apost)
    if resp.status_code != 201:
        print(CFAIL +' Fail.'+CEND+' Status code: {}'.format(resp.status_code))
    else:
        print(CPASS + ' Passed.'+CEND+' Status code:{}'.format(resp.status_code))
    
    print('2. Delete an existing post:')   # delete the latest added post
    conn = sqlite3.connect('project.db')
    cur = conn.cursor()
    query = "SELECT id FROM posts ORDER BY id DESC LIMIT 1;"
    result = cur.execute(query).fetchall()
    conn.commit()
    conn.close()
    get_postid = result[0][0]
    resp = requests.delete('http://localhost:2015/posts/todo/api/v1.0/delete/{}'.format(get_postid))
    if resp.status_code != 200:
        print(CFAIL +' Failed.'+CEND+' Status code: {}'.format(resp.status_code))
    else:
        print(CPASS +' Passed.'+CEND+' Status code:{}'.format(resp.status_code) )
    
    print('3. Retrieve an existing post:')    
    resp = requests.get('http://localhost:2015/posts/todo/api/v1.0/get/2')
    if resp.status_code != 200:
        print(CFAIL + ' Failed.'+CEND+' Status code: {}'.format(resp.status_code))
    else:
        print(CPASS +' Passed.'+CEND+' Status code:{}'.format(resp.status_code))
        
    print('4. List the n most recent posts to a particular community:')    
    resp = requests.get('http://localhost:2015/posts/todo/api/v1.0/get/recent/Technology/3')
    if resp.status_code != 200:
        print(CFAIL + ' Failed.'+CEND+' Status code: {}'.format(resp.status_code))
    else:
        print(CPASS +' Passed.'+CEND+' Status code:{}'.format(resp.status_code))
        
    print('5. List the n most recent posts to any community:')    
    resp = requests.get('http://localhost:2015/posts/todo/api/v1.0/get/recent/6')
    if resp.status_code != 200:
        print(CFAIL +' Failed.'+CEND+' Status code: {}'.format(resp.status_code))
    else:
        print(CPASS +' Passed.'+CEND+' Status code:{}'.format(resp.status_code))    

def user_microservice():
    print('\nUSER MICRO SERVICE')
    print('1. Create a user:')
    resp = requests.get('http://localhost:2015/users/todo/api/v1.0/getlatest')
    latest_userid = int(resp.content) + 1
    auser = {"username":"tester{}".format(latest_userid),"email":"tester{}@gmail.com".format(latest_userid),"karma":0}
    resp = requests.post('http://localhost:2015/users/todo/api/v1.0/create', json=auser)
    if resp.status_code != 201:
        print(CFAIL +' Fail.'+CEND+' Status code: {}'.format(resp.status_code))
    else:
        print(CPASS+' Passed.'+CEND+' Status code:{}'.format(resp.status_code))
    
    print('2. Update email:')
    update_from_user = {"email":"tester3_update@gmail.com","username":"tester3"}
    resp = requests.put('http://localhost:2015/users/todo/api/v1.0/updatemail', json=update_from_user)
    if resp.status_code != 200:
        print(CFAIL + ' Failed.'+CEND+' Status code: {}'.format(resp.status_code))
    else:
        print(CPASS+' Passed.'+CEND+' Status code:{}'.format(resp.status_code))
    
    print('3. Increment Karma:')    
    increase_karma = {"username":"tester3"}
    resp = requests.put('http://localhost:2015/users/todo/api/v1.0/update/inckarma', json=increase_karma)
    if resp.status_code != 200:
        print(CFAIL + ' Failed.'+CEND+' Status code: {}'.format(resp.status_code))
    else:
        print(CPASS +' Passed.'+ CEND+' Status code:{}'.format(resp.status_code))
        
    print('4. Decrement Karma:')    
    decrease_karma = {"username":"tester3"}
    resp = requests.put('http://localhost:2015/users/todo/api/v1.0/update/deckarma', json=decrease_karma)
    if resp.status_code != 200:
        print(CFAIL +' Failed.' + CEND +' Status code: {}'.format(resp.status_code))
    else:
        print(CPASS +' Passed.' + CEND +' Status code:{}'.format(resp.status_code))
    
    print('5. Deactivate account:')    
    deactive_username = {"username":"tester1"}
    resp = requests.put('http://localhost:2015/users/todo/api/v1.0/account/deactivate', json=deactive_username)
    if resp.status_code != 200:
        print(CFAIL +' Failed.'+ CEND +' Status code: {}'.format(resp.status_code))
    else:
        print(CPASS +' Passed.'+CEND+' Status code:{}'.format(resp.status_code))

def message_microservice():
    print('\nMESSAGE MICRO SERVICE')
    print('1. Send message:')
    amessage = {"user_from":"tester2","user_to":"tester4","content":"user tester2 send a message to user tester 4"}
    resp = requests.post('http://localhost:2015/messages/todo/api/v1.0/send', json=amessage)
    if resp.status_code != 201:
        print(CFAIL +' Fail.'+CEND+' Status code: {}'.format(resp.status_code))
    else:
        print(CPASS+' Passed.'+CEND+' Status code:{}'.format(resp.status_code))
        
    print('2. Delete message:')
    amessage = {"user_from":"tester2","user_to":"tester4","content":"user tester2 send a message to user tester 4"}
    resp = requests.post('http://localhost:2015/messages/todo/api/v1.0/send', json=amessage)
    resp = requests.get('http://localhost:2015/messages/todo/api/v1.0/getlatest')
    resp = requests.delete('http://localhost:2015/messages/todo/api/v1.0/delete/{}'.format(int(resp.content)))
    if resp.status_code != 200:
        print(CFAIL +' Fail.'+CEND+' Status code: {}'.format(resp.status_code))
    else:
        print(CPASS+' Passed.'+CEND+' Status code:{}'.format(resp.status_code))
        
    print('3. Set favorite message (of a user):')
    mid = {"message_id":"2"}
    resp = requests.put('http://localhost:2015/messages/todo/api/v1.0/setfavorite', json=mid)
    if resp.status_code != 200:
        print(CFAIL +' Failed.'+ CEND +' Status code: {}'.format(resp.status_code))
    else:
        print(CPASS +' Passed.'+CEND+' Status code:{}'.format(resp.status_code))
        
    print('4. Get favorite message (of a user):')    
    resp = requests.get('http://localhost:2015/messages/todo/api/v1.0/get/favorite/tester4')
    if resp.status_code != 200:
        print(CFAIL + ' Failed.'+CEND+' Status code: {}'.format(resp.status_code))
    else:
        print(CPASS +' Passed.'+CEND+' Status code:{}'.format(resp.status_code))

def vote_microservice():
    print('\nVOTE MICRO SERVICE')
    print('1. Upvote a post:')
    upvote_from_postid = {"postid":"2"}
    resp = requests.put('http://localhost:2015/votes/todo/api/v1.0/upvote', json=upvote_from_postid)
    if resp.status_code != 200:
        print(CFAIL + ' Failed.'+CEND+' Status code: {}'.format(resp.status_code))
    else:
        print(CPASS+' Passed.'+CEND+' Status code:{}'.format(resp.status_code))
    
    print('2. Downvote a post:')
    downvote_from_postid = {"postid":"2"}
    resp = requests.put('http://localhost:2015/votes/todo/api/v1.0/downvote', json=downvote_from_postid)
    if resp.status_code != 200:
        print(CFAIL + ' Failed.'+CEND+' Status code: {}'.format(resp.status_code))
    else:
        print(CPASS+' Passed.'+CEND+' Status code:{}'.format(resp.status_code))
    
    print('3. Report the number of upvotes and downvotes for a post:')    
    resp = requests.get('http://localhost:2015/votes/todo/api/v1.0/get/2')
    if resp.status_code != 200:
        print(CFAIL + ' Failed.'+CEND+' Status code: {}'.format(resp.status_code))
    else:
        print(CPASS +' Passed.'+CEND+' Status code:{}'.format(resp.status_code))
    
    print('4. List the n top-scoring posts to any community:')    
    resp = requests.get('http://localhost:2015/votes/todo/api/v1.0/get/top/3')
    if resp.status_code != 200:
        print(CFAIL + ' Failed.'+CEND+' Status code: {}'.format(resp.status_code))
    else:
        print(CPASS +' Passed.'+CEND+' Status code:{}'.format(resp.status_code))
        
    print('5. Given a list of post identifiers, return the list sorted by score:')    
    list_postid = {"postids":"2,3,4"}
    resp = requests.get('http://localhost:2015/votes/todo/api/v1.0/sort', json=list_postid)
    if resp.status_code != 200:
        print(CFAIL +' Failed.' + CEND +' Status code: {}'.format(resp.status_code))
    else:
        print(CPASS +' Passed.' + CEND +' Status code:{}'.format(resp.status_code))

post_microservice()
user_microservice()
message_microservice()
vote_microservice()