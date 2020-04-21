import requests
import sqlite3



CPASS = '\033[94m'
CFAIL = '\033[32m'
CEND = '\033[0m'


def post_microservice():
    print(CFAIL +'NEGATIVE TEST:\n' + CEND)
    print('POST MICRO SERVICE')
    print('1. Create new post using a nonexistent username:') 
    apost = {"title":"Socimedia","text":"Reddit ran wild with Boston bombing conspiracy theories in 2013","community":"Technology",\
             "url":"https://www.theverge.com/tech/2020/2/26/21153525/firefox-dns-encryption-amazon-go-browsing-shopping-privacy",\
             "username":"tester9999"}
    resp = requests.post('http://localhost:2015/posts/todo/api/v1.0/create', json=apost)
    if resp.status_code != 201:
        print(CFAIL +' Failed.'+CEND+' Status code: {}'.format(resp.status_code))
    else:
        print(CPASS + ' Passed.'+CEND+' Status code:{}'.format(resp.status_code))
    
    
    print('2. Delete a nonexistent post:')   # delete the latest added post
    conn = sqlite3.connect('project.db')
    cur = conn.cursor()
    query = "SELECT id FROM posts ORDER BY id DESC LIMIT 1;"
    result = cur.execute(query).fetchall()
    conn.commit()
    conn.close()
    resp = requests.delete('http://localhost:2015/posts/todo/api/v1.0/delete/9999')
    if resp.status_code != 200:
        print(CFAIL +' Failed.'+CEND+' Status code: {}'.format(resp.status_code))
    else:
        print(CPASS +' Passed.'+CEND+' Status code:{}'.format(resp.status_code) )
    
    print('3. Retrieve a nonexistent post:')    
    resp = requests.get('http://localhost:2015/posts/todo/api/v1.0/get/9999')
    if resp.status_code != 200:
        print(CFAIL + ' Failed.'+CEND+' Status code: {}'.format(resp.status_code))
    else:
        print(CPASS +' Passed.'+CEND+' Status code:{}'.format(resp.status_code))
        
    print('4. List the n most recent posts to a particular community (without existence):')    
    resp = requests.get('http://localhost:2015/posts/todo/api/v1.0/get/recent/Nonexistent/3')
    if resp.status_code != 200:
        print(CFAIL + ' Failed.'+CEND+' Status code: {}'.format(resp.status_code))
    else:
        print(CPASS +' Passed.'+CEND+' Status code:{}'.format(resp.status_code))
        
    print('5. List the 0 most recent posts to any community:')    
    resp = requests.get('http://localhost:2015/posts/todo/api/v1.0/get/recent/0')
    if resp.status_code != 200:
        print(CFAIL +' Failed.'+CEND+' Status code: {}'.format(resp.status_code))
    else:
        print(CPASS +' Passed.'+CEND+' Status code:{}'.format(resp.status_code))    

def user_microservice():
    print('\nUSER MICRO SERVICE')
    print('1. Create an existent user:')
    auser = {"username":"tester1","email":"tester3@gmail.com","karma":0}
    resp = requests.post('http://localhost:2015/users/todo/api/v1.0/create', json=auser)
    if resp.status_code != 201:
        print(CFAIL +' Fail.'+CEND+' Status code: {}'.format(resp.status_code))
    else:
        print(CPASS+' Passed.'+CEND+' Status code:{}'.format(resp.status_code))
    
    print('2. Update email using a nonexistent user:')
    update_from_user = {"email":"tester3_update@gmail.com","username":"tester9999"}
    resp = requests.put('http://localhost:2015/users/todo/api/v1.0/updatemail', json=update_from_user)
    if resp.status_code != 200:
        print(CFAIL + ' Failed.'+CEND+' Status code: {}'.format(resp.status_code))
    else:
        print(CPASS+' Passed.'+CEND+' Status code:{}'.format(resp.status_code))
    
    print('3. Increment karma of a nonexistent user:')    
    increase_karma = {"username":"tester9999"}
    resp = requests.put('http://localhost:2015/users/todo/api/v1.0/update/inckarma', json=increase_karma)
    if resp.status_code != 200:
        print(CFAIL + ' Failed.'+CEND+' Status code: {}'.format(resp.status_code))
    else:
        print(CPASS +' Passed.'+ CEND+' Status code:{}'.format(resp.status_code))
        
    print('4. Decrement Karma of a nonexistent user::')    
    decrease_karma = {"username":"tester9999"}
    resp = requests.put('http://localhost:2015/users/todo/api/v1.0/update/deckarma', json=decrease_karma)
    if resp.status_code != 200:
        print(CFAIL +' Failed.' + CEND +' Status code: {}'.format(resp.status_code))
    else:
        print(CPASS +' Passed.' + CEND +' Status code:{}'.format(resp.status_code))
    
    print('5. Deactivate a nonexistent account:')    
    deactive_username = {"username":"tester9999"}
    resp = requests.put('http://localhost:2015/users/todo/api/v1.0/account/deactivate', json=deactive_username)
    if resp.status_code != 200:
        print(CFAIL +' Failed.'+ CEND +' Status code: {}'.format(resp.status_code))
    else:
        print(CPASS +' Passed.'+CEND+' Status code:{}'.format(resp.status_code))

def message_microservice():
    print('\nMESSAGE MICRO SERVICE')
    print('1. Send message to a nonexistent user:')
    amessage = {"user_from":"tester2","user_to":"tester9999","content":"user tester2 send a message to user tester 4"}
    resp = requests.post('http://localhost:2015/messages/todo/api/v1.0/send', json=amessage)
    if resp.status_code != 201:
        print(CFAIL +' Fail.'+CEND+' Status code: {}'.format(resp.status_code))
    else:
        print(CPASS+' Passed.'+CEND+' Status code:{}'.format(resp.status_code))
    print('2. Delete a nonexistent message:')
    resp = requests.delete('http://localhost:2015/messages/todo/api/v1.0/delete/9999')
    if resp.status_code != 200:
        print(CFAIL +' Fail.'+CEND+' Status code: {}'.format(resp.status_code))
    else:
        print(CPASS+' Passed.'+CEND+' Status code:{}'.format(resp.status_code))
    print('3. Set a nonexistent favorite message:')    
    mid = {"message_id":"9999"}
    resp = requests.put('http://localhost:2015/messages/todo/api/v1.0/setfavorite', json=mid)
    if resp.status_code != 200:
        print(CFAIL +' Failed.'+ CEND +' Status code: {}'.format(resp.status_code))
    else:
        print(CPASS +' Passed.'+CEND+' Status code:{}'.format(resp.status_code))
    print('4. Get favorite message (of a nonexistent user):')    
    resp = requests.get('http://localhost:2015/messages/todo/api/v1.0/get/favorite/tester9999')
    if resp.status_code != 200:
        print(CFAIL + ' Failed.'+CEND+' Status code: {}'.format(resp.status_code))
    else:
        print(CPASS +' Passed.'+CEND+' Status code:{}'.format(resp.status_code))

def vote_microservice():
    print('\nVOTE MICRO SERVICE')
    print('1. Upvote a nonexistent post:')
    upvote_from_postid = {"postid":"9999"}
    resp = requests.put('http://localhost:2015/votes/todo/api/v1.0/upvote', json=upvote_from_postid)
    if resp.status_code != 200:
        print(CFAIL + ' Failed.'+CEND+' Status code: {}'.format(resp.status_code))
    else:
        print(CPASS+' Passed.'+CEND+' Status code:{}'.format(resp.status_code))
    
    print('2. Downvote a nonexistent post:')
    downvote_from_postid = {"postid":"9999"}
    resp = requests.put('http://localhost:2015/votes/todo/api/v1.0/downvote', json=downvote_from_postid)
    if resp.status_code != 200:
        print(CFAIL + ' Failed.'+CEND+' Status code: {}'.format(resp.status_code))
    else:
        print(CPASS+' Passed.'+CEND+' Status code:{}'.format(resp.status_code))
    
    print('3. Report the number of upvotes and downvotes for a nonexistent post:')    
    resp = requests.get('http://localhost:2015/votes/todo/api/v1.0/get/9999')
    if resp.status_code != 200:
        print(CFAIL + ' Failed.'+CEND+' Status code: {}'.format(resp.status_code))
    else:
        print(CPASS +' Passed.'+CEND+' Status code:{}'.format(resp.status_code))
    
    print('4. List the 0 top-scoring posts to any community:')    
    resp = requests.get('http://localhost:2015/votes/todo/api/v1.0/get/top/0')
    if resp.status_code != 200:
        print(CFAIL + ' Failed.'+CEND+' Status code: {}'.format(resp.status_code))
    else:
        print(CPASS +' Passed.'+CEND+' Status code:{}'.format(resp.status_code))
        
    print('5. Given a list of post identifiers (one of them non-exists), return the list sorted by score:')    
    list_postid = {"postids":"2,3,9999"}
    resp = requests.get('http://localhost:2015/votes/todo/api/v1.0/sort', json=list_postid)
    if resp.status_code != 200:
        print(CFAIL +' Failed.' + CEND +' Status code: {}'.format(resp.status_code))
    else:
        print(CPASS +' Passed.' + CEND +' Status code:{}'.format(resp.status_code))

post_microservice()
user_microservice()
message_microservice()
vote_microservice()