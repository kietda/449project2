# Overview
This is the project we’re going to build services for a web application similar to reddit.
The test environment for this project in this course is a Linux VM such as Ubuntu 20.04.1 LTS

# Install neccessary packages:
Following these steps to install neccessary packages:
1. Install python:
$ sudo apt-get install python3
2. Install pip3:
$ sudo apt install python3-pip
3. Install flask:
$ pip3 install flask
4. Install Gunicorn3
$ sudo apt install --yes gunicorn3
5. Install foreman 
$ sudo apt install ruby-foreman
6. Installing Caddy1
$ curl https://getcaddy.com | bash -s personal
7. Install Python script for the Requests library
$ pip3 install --user requests
8. Install faker (for getting bogus data):
$ pip3 install faker
9. Install locustio:
$ pip3 install locustio


# Run the services:
1. For running the three instances for every microservices, open a terminal in project folder and run command:
$ sudo foreman start -m post=3,user=3,message=3,vote=3
2. Open another terminal in project folder and run the command:
$ ulimit -n 8192 && caddy
3. Open another terminal to test our api service

# HOW TO USE OUR API SERVICE
POST MICRSOSERVICE:
1. Create new post:
$ curl -i -H "Content-Type:application/json" -X POST -d '{"title":"Socimedia","text":"Reddit ran wild with Boston bombing conspiracy theories in 2013","community":"Technology", "url":"https://www.theverge.com/tech/2020/2/26/21153525/firefox-dns-encryption-amazon-go-browsing-shopping-privacy","username":"tester1"}' http://localhost:2015/posts/todo/api/v1.0/create
2. Delete an existing post:
$ curl -i -X DELETE http://localhost:2015/posts/todo/api/v1.0/delete/1
3. Retrieve an existing post
$ curl -i http://localhost:2015/posts/todo/api/v1.0/get/2
4. List the n most recent posts to a particular community:
$ curl -i http://localhost:2015/posts/todo/api/v1.0/get/recent/Technology/3
5. List the n most recent posts to any community:
$ curl -i http://localhost:2015/posts/todo/api/v1.0/get/recent/6

USER MICRO SERVICE:
1. Create user
$ curl -i -H "Content-Type:application/json" -X POST -d '{"username":"tester101","email":"tester101@gmail.com","karma":0}' http://localhost:2015/users/todo/api/v1.0/create
2. Update email
$ curl -i -H "Content-Type:application/json" -X PUT -d '{"email":"tester5_update@gmail.com","username":"tester5"}' http://localhost:2015/users/todo/api/v1.0/updatemail
3. Increment Karma
$ curl -i -H "Content-Type:application/json" -X PUT -d '{"username":"tester5"}' http://localhost:2015/users/todo/api/v1.0/update/inckarma
4. Decrement Karma
$ curl -i -H "Content-Type:application/json" -X PUT -d '{"username":"tester5"}' http://localhost:2015/users/todo/api/v1.0/update/deckarma
5. Deactivate account
$ curl -i -H "Content-Type:application/json" -X PUT -d '{"username":"tester1"}' http://localhost:2015/users/todo/api/v1.0/account/deactivate

MESSAGE MICRO SERVICE:
1. Send message
$ curl -i -H "Content-Type:application/json" -X POST -d '{"user_from":"tester2","user_to":"tester4","content":"user tester2 send a message to user tester 4"}' http://localhost:2015/messages/todo/api/v1.0/send
2. Delete message
$ curl -i -X DELETE http://localhost:2015/messages/todo/api/v1.0/delete/1
3. Set favorite message using message_id
$ curl -i -H "Content-Type:application/json" -X PUT -d '{"message_id":"101"}' http://localhost:2015/messages/todo/api/v1.0/setfavorite
4. Get favorite message (of a user)
$ curl -i http://localhost:2015/messages/todo/api/v1.0/get/favorite/tester4

VOTE MICRO SERVICE:
1. Upvote a post
$ curl -i -H "Content-Type:application/json" -X PUT -d '{"postid":"2"}' http://localhost:2015/votes/todo/api/v1.0/upvote
2. Downvote a post
$ curl -i -H "Content-Type:application/json" -X PUT -d '{"postid":"3"}' http://localhost:2015/votes/todo/api/v1.0/downvote
3. Report the number of upvotes and downvotes for a post
$ curl -i http://localhost:2015/votes/todo/api/v1.0/get/2
4. List the n top-scoring posts to any community
$ curl -i http://localhost:2015/votes/todo/api/v1.0/get/top/3
5. Given a list of post identifiers, return the list sorted by score.
$ curl -i -H "Content-Type:application/json" -X GET -d '{"postids":"2,3,4"}' http://localhost:2015/votes/todo/api/v1.0/sort

# BASIC TEST :
$ python3 basictest.py

# NEGATIVE TEST:
$ python3 negativetest.py

# LOAD TEST (simulating 100 users with bogus data)
$ locust -f loadtest.py --host=http://localhost:2015
When python load testing app Locust is started, open browser and visit this url:
- http://127.0.0.1:8089/
This is a web-interface of our Locust instance. 
- Input number of total users: 100
- Input Hatch rate (users spawned/second): 5
- Press "Start swarming" to start "hatching" users and see results in the table

To stop testing:
- Click "Stop" button at the top right corner of browser.
- Come back terminal, press "Ctrl + C" to stop.

# STRESS TEST (simulating 2000 users with bogus data)
$ locust -f loadtest.py --host=http://localhost:2015
Similar to Loadtest but this time, in a web-interface of our Locust instance(http://127.0.0.1:8089/), we input:
- Input number of total users: 2000
- Input Hatch rate (users spawned/second): 50
- Press "Start swarming" to start "hatching" users and see results in the table
This time, we will see the failure rate is too high because of overload. 

To stop testing:
- Click "Stop" button at the top right corner of browser.
- Come back terminal, press "Ctrl + C" to stop.
