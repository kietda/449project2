# create database with bogust data
import sqlite3
from faker import Faker
random = Faker()
# postid = random.random_int(min=1, max=100, step=1)
communities = ['Sales','Technology','Computer','Game' ]

conn = sqlite3.connect('project.db')
c = conn.cursor()
c.execute("PRAGMA foreign_keys = 1")
conn.commit()

def drop_tables():
    c.execute('DROP TABLE IF EXISTS votes')
    c.execute('DROP TABLE IF EXISTS posts')
    c.execute('DROP TABLE IF EXISTS messages')
    c.execute('DROP TABLE IF EXISTS users')
    conn.commit()

def create_users_table():
    c.execute('CREATE TABLE users(userid INTEGER PRIMARY KEY AUTOINCREMENT,\
                username TEXT,\
                email TEXT,\
                karma INTEGER,\
                activated INTEGER DEFAULT 1,\
                UNIQUE(username))')
    conn.commit()
    
def create_messages_table():
    c.execute('CREATE TABLE messages(message_id INTEGER PRIMARY KEY AUTOINCREMENT,\
                user_from TEXT,\
                user_to TEXT,\
                timestamp TEXT DEFAULT (datetime(\'now\',\'localtime\')),\
                content TEXT,\
                flag INTEGER DEFAULT 0,\
                FOREIGN KEY (user_from) REFERENCES users(username),\
                FOREIGN KEY (user_to) REFERENCES users(username))')
    conn.commit()
    
def create_posts_table():
    c.execute('CREATE TABLE posts\
            (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, text TEXT,\
            community TEXT, url TEXT, username TEXT,\
            date TEXT DEFAULT (strftime(\'%Y-%m-%d\',\'now\',\'localtime\')),\
            FOREIGN KEY (username) REFERENCES  users(username))')
    conn.commit()

def create_votes_table():
    c.execute('CREATE TABLE votes\
            (postid INTEGER,\
            upvote INTEGER DEFAULT 0,\
            downvote INTEGER DEFAULT 0,\
            FOREIGN KEY (postid) REFERENCES  posts(id))')
    conn.commit()

#add users
def users_data_entry():
    for x in range(1, 101):
        ausername = "tester{}".format(x)
        akarma = random.random_int(min=1, max=100, step=1)
        c.execute('INSERT INTO users(username,email, karma) VALUES("{}", "{}@gmail.com", {})'.format(ausername,ausername,akarma))    
    conn.commit()
    
#add messages
def messages_data_entry():
    for x in range(1, 101):
        auser_from = random.random_int(min=1, max=100, step=1)
        auser_to = random.random_int(min=1, max=100, step=1)
        acontent = random.sentence(nb_words=3, variable_nb_words=True, ext_word_list=None)
        c.execute('INSERT INTO messages(user_from,user_to,content) VALUES("tester{}", "tester{}", "This is a message from tester{} to tester{}.Content: {}")'.format(auser_from,auser_to, auser_from, auser_to,acontent))
    conn.commit() 

#add posts
def posts_data_entry():
    for x in range(1, 101):
        # communities = ['Sales','Technology','Computer','Game' ]
        atitle = random.sentence(nb_words=3, variable_nb_words=True, ext_word_list=None)
        atext = random.sentence(nb_words=4, variable_nb_words=True, ext_word_list=None)
        acommunity = communities[random.random_int(min=0, max=3, step=1)]
        aurl = "http://{}com".format(random.sentence(nb_words=1, variable_nb_words=True, ext_word_list=None))
        ausername = 'tester{}'.format(random.random_int(min=1, max=100, step=1))
        adate = random.date()
        c.execute('INSERT INTO posts(title,text,community,url,username,date) VALUES("{}", "{}", "{}", "{}","{}","{}")'.format(atitle,atext,acommunity,aurl,ausername,adate))
    conn.commit()
    
#add votes
def votes_data_entry():
    for x in range(1, 101):
        avoteup = random.random_int(min=1, max=100, step=1)
        avotedown = random.random_int(min=1, max=100, step=1)
        c.execute('INSERT INTO votes VALUES({}, {}, {})'.format(x,avoteup,avotedown))
    conn.commit()
   
drop_tables()
create_users_table()
create_messages_table()
create_posts_table()
create_votes_table()

users_data_entry()
messages_data_entry()
posts_data_entry()
votes_data_entry()

c.close()
conn.close()
