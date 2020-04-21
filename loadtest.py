# load test simulating 100 users with bogust data
from locust import HttpLocust, TaskSet, task, between
from faker import Faker
import requests
import uuid 

random = Faker()
communities = ['Sales','Technology','Computer','Game' ]
# resp = requests.get('http://localhost:2015/messages/todo/api/v1.0/getlatest')
# latest_messageid = int(resp.content)
# resp = requests.get('http://localhost:2015/posts/todo/api/v1.0/getlatest')
# latest_postid = int(resp.content)
# resp = requests.get('http://localhost:2015/users/todo/api/v1.0/getlatest')
# latest_userid = int(resp.content)
# postid = random.random_int(min=1, max=100, step=1)
# userid = random.random_int(min=1, max=100, step=1)
# apost = {"title":"Socimedia","text":"Reddit ran wild with Boston","community":"Technology",\
#          "url":"https://www.theverge.com/tech","username":"tester{}".format(userid)}
class ApiTaks(TaskSet):
    #POST TASKS
    @task(2)
    def create_post(self):        
        atitle = random.sentence(nb_words=3, variable_nb_words=True, ext_word_list=None)
        atext = random.sentence(nb_words=4, variable_nb_words=True, ext_word_list=None)
        acommunity = communities[random.random_int(min=0, max=3, step=1)]
        aurl = "http://{}com".format(random.sentence(nb_words=1, variable_nb_words=True, ext_word_list=None))
        ausername = 'tester{}'.format(random.random_int(min=1, max=100, step=1))
        adate = random.date()
        userid = random.random_int(min=2, max=100, step=1)
        apost = {"title":atitle,"text":atext,"community":acommunity,\
         "url":aurl,"username":"tester{}".format(userid),"date":adate}
        # c.execute('INSERT INTO posts(title,text,community,url,username,date) VALUES("{}", "{}", "{}", "{}","{}","{}")'.format(atitle,atext,acommunity,aurl,ausername,adate))
        self.client.post('http://localhost:2015/posts/todo/api/v1.0/create', json=apost, name='Create A Post')
        
    @task(1)
    def delete_post(self):
        resp = requests.get('http://localhost:2015/posts/todo/api/v1.0/getlatest')
        latest_postid = int(resp.content)
        self.client.delete('http://localhost:2015/posts/todo/api/v1.0/delete/{}'.format(latest_postid),name='Delete A Post')
        
    @task(10)
    def get_post(self):
        postid = random.random_int(min=1, max=90, step=1)
        self.client.get("/posts/todo/api/v1.0/get/{}".format(postid),name='Get A Post')
    
    @task(5)
    def get_community_recent_post(self):
        anumber = random.random_int(min=1, max=100, step=1)
        acommunity = communities[random.random_int(min=0, max=3, step=1)]        
        self.client.get("/posts/todo/api/v1.0/get/recent/{}/{}".format(acommunity,anumber), name = 'Get community recent posts')
        
    @task(5)
    def get_any_recent_post(self):
        anumber = random.random_int(min=1, max=100, step=1)  
        self.client.get("http://localhost:2015/posts/todo/api/v1.0/get/recent/{}".format(anumber), name = 'Get any recent post')
    
    #USER TASKS
    @task(2)
    def create_a_user(self):
        new_userid = uuid.uuid1()
        auser = {"username":"tester{}".format(new_userid),"email":"tester{}@gmail.com".format(new_userid),"karma":0}
        self.client.post("http://localhost:2015/users/todo/api/v1.0/create", json= auser, name = 'Create a user')
    
    @task(2)
    def update_email(self):
        userid = random.random_int(min=2, max=100, step=1)
        update_from_user = {"email":"tester{}_update@gmail.com".format(userid),"username":"tester{}".format(userid)}
        # resp = requests.put('http://localhost:2015/users/todo/api/v1.0/updatemail', json=update_from_user)
        self.client.put("http://localhost:2015/users/todo/api/v1.0/updatemail", json= update_from_user, name = 'Update email of a user')
    
    @task(5)
    def increase_karma(self):
        userid = random.random_int(min=2, max=100, step=1)
        increase_karma = {"username":"tester{}".format(userid)}
        # resp = requests.put('http://localhost:2015/users/todo/api/v1.0/update/inckarma', json=increase_karma)
        self.client.put("http://localhost:2015/users/todo/api/v1.0/update/inckarma", json= increase_karma, name = 'Increase karma of a user')

    @task(5)
    def decrease_karma(self):
        userid = random.random_int(min=2, max=100, step=1)
        decrease_karma = {"username":"tester{}".format(userid)}
        # resp = requests.put('http://localhost:2015/users/todo/api/v1.0/update/inckarma', json=increase_karma)
        self.client.put("http://localhost:2015/users/todo/api/v1.0/update/deckarma", json= decrease_karma, name = 'Decrease karma of a user')    
    
    @task(1)
    def deactive_account(self):
        deactive_username = {"username":"tester1"}
        # resp = requests.put('http://localhost:2015/users/todo/api/v1.0/account/deactivate', json=deactive_username)
        self.client.put("http://localhost:2015/users/todo/api/v1.0/account/deactivate", json= deactive_username, name = 'Deactivate a user')    
    
    # MESSAGE TASKS
    @task(4)
    def send_message(self):
        afrom = random.random_int(min=2, max=100, step=1)
        ato = random.random_int(min=2, max=100, step=1)
        amessage = {"user_from":"tester{}".format(afrom),"user_to":"tester{}".format(ato),"content":"user tester{} send a message to user tester {}".format(afrom,ato)}
        # resp = requests.post('http://localhost:2015/messages/todo/api/v1.0/send', json=amessage)
        self.client.post("http://localhost:2015/messages/todo/api/v1.0/send", json= amessage, name = 'Send a message')

    @task(2)
    def delete_message(self):
        resp = requests.get('http://localhost:2015/messages/todo/api/v1.0/getlatest')
        latest_messageid = int(resp.content)
        # resp = requests.delete('http://localhost:2015/messages/todo/api/v1.0/delete/{}'.format(int(resp.content)))    
        self.client.delete('http://localhost:2015/messages/todo/api/v1.0/delete/{}'.format(latest_messageid),name='Delete A Message')
    
    @task(2)
    def set_favorite_message(self):
        messageid = random.random_int(min=2, max=90, step=1)
        mid = {"message_id":messageid}
        # resp = requests.put('http://localhost:2015/messages/todo/api/v1.0/setfavorite', json=mid)
        self.client.put("http://localhost:2015/messages/todo/api/v1.0/setfavorite", json= mid, name = 'Set a favorite message')    
    
    @task(2)
    def get_favorite_message(self):
        userid = random.random_int(min=2, max=100, step=1)
        # resp = requests.get('http://localhost:2015/messages/todo/api/v1.0/get/favorite/tester4')        
        self.client.get("http://localhost:2015/messages/todo/api/v1.0/get/favorite/tester{}".format(userid), name = 'Get a favorite message')    
    
    # VOTE TASKS
    @task(2)
    def upvote_post(self):
        apostid = random.random_int(min=2, max=90, step=1)
        upvote_from_postid = {"postid":apostid}
        # resp = requests.put('http://localhost:2015/votes/todo/api/v1.0/upvote', json=upvote_from_postid)
        self.client.put("http://localhost:2015/votes/todo/api/v1.0/upvote", json= upvote_from_postid, name = 'Upvote a post')
    
    @task(2)
    def downvote_post(self):
        apostid = random.random_int(min=2, max=90, step=1)
        downvote_from_postid = {"postid":apostid}        
        self.client.put("http://localhost:2015/votes/todo/api/v1.0/downvote", json= downvote_from_postid, name = 'Downvote a post')
    
    @task(10)    
    def updown_vote_post(self):
        apostid = random.random_int(min=2, max=90, step=1)
        # resp = requests.get('http://localhost:2015/votes/todo/api/v1.0/get/2')
        self.client.get("http://localhost:2015/votes/todo/api/v1.0/get/{}".format(apostid), name = 'Get upvote and downvote of a post')    

    @task(10)    
    def top_posts(self):        
        anumber = random.random_int(min=1, max=100, step=1)
        # resp = requests.get('http://localhost:2015/votes/todo/api/v1.0/get/top/3')
        self.client.get("http://localhost:2015/votes/todo/api/v1.0/get/top/{}".format(anumber), name = 'Top-scoring posts to any community')    
    
    @task(10)
    def sort_posts(self):
        apostid1 = random.random_int(min=2, max=90, step=1)
        apostid2 = random.random_int(min=2, max=90, step=1)
        apostid3 = random.random_int(min=2, max=90, step=1)
        list_postid = {"postids":"{},{},{}".format(apostid1,apostid2,apostid3)}
        # resp = requests.get('http://localhost:2015/votes/todo/api/v1.0/sort', json=list_postid)
        self.client.get("http://localhost:2015/votes/todo/api/v1.0/sort",json=list_postid, name = 'Sort a list of posts')    
        
    

class ApiUsers(HttpLocust):        
    task_set = ApiTaks
    wait_time = between(5, 15)