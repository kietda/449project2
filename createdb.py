import sqlite3

conn = sqlite3.connect('project1.db')
c = conn.cursor()
c.execute("PRAGMA foreign_keys = 1")
conn.commit()

def drop_tables():
    c.execute('DROP TABLE IF EXISTS posts')
    c.execute('DROP TABLE IF EXISTS users')    
    conn.commit()

def create_users_table():
    c.execute('CREATE TABLE users(username TEXT PRIMARY KEY,\
                email TEXT,\
                karma INTEGER,\
                activated INTEGER DEFAULT 1)')
    conn.commit()
    
def create_posts_table():
    c.execute('CREATE TABLE posts\
            (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, text TEXT,\
            community TEXT, url TEXT, username TEXT,\
            date TEXT DEFAULT (strftime(\'%Y-%m-%d\',\'now\',\'localtime\')),\
            FOREIGN KEY (username) REFERENCES  users(username))')
    conn.commit()

#add users
def users_data_entry():
    c.execute('INSERT INTO users(username,email, karma) VALUES("tester1", "tester1@gmail.com", 0)')
    c.execute('INSERT INTO users(username,email, karma) VALUES("tester2", "tester2@gmail.com", 0)')    
    conn.commit() 

#add posts
def posts_data_entry():
    c.execute('INSERT INTO posts VALUES(1, "Buy groceries", "Milk", "Sales", "http://walmart.com","tester1","2020-03-01")')
    c.execute('INSERT INTO posts VALUES(2, "Learn Python", "Need to find a good Python tutorial on the web", "Technology", "https://miro.medium.com/max/768/1*CrK1VuTTMSg-zL9-z3ohQQ.png","tester1","2020-03-02")')
    c.execute('INSERT INTO posts VALUES(3, "Learn Flask", "Need to find a good Flask tutorial on the web", "Technology", "https://miro.medium.com/max/768/1*CrK1VuTTMSg-zL9-z3ohQQ.png","tester2","2020-03-03")')
    c.execute('INSERT INTO posts(id,title, text, community, url, username) VALUES(4, "Buy things", "Ball", "Sales", "http://walmart.com","tester2")')
    conn.commit()
   
drop_tables()
create_posts_table()
create_users_table()
users_data_entry()
posts_data_entry()

c.close()
conn.close()
