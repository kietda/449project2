# Support Contacts

|        | Team           | Contact Info          	  				| Runbook Review        		|
|--------|----------------|-----------------------------------------|-------------------------------|
|   1	 | Development      | kdang53@csu.fullerton.edu 			| Kiet Dang - 3/15/2020 		|
|   2	 | Testing          | christian.angeles@csu.fullerton.edu 	| Christian Angeles - 3/28/2020 |
|   3	 | Operations       | art2015@csu.fullerton.edu 	  		| Arthur Salazar - 3/29/2020  	|


# Overview

This is the project we’re going to build services for a web application
similar to reddit.

# How to run the services:

The test environment for this project in this course is a Tuffix VM with
Python 3.6.7

Following these steps to install neccessary packages:
1. Install python:
sudo apt-get install python3
2. Install pip3:
sudo apt install python3-pip
3. Install flask:
pip3 install flask

Following these steps to start the services:
1. Open terminal in the project folder
2. Executing a linux command:
	python3 createdb.py
		>> to create new database named "project1.db"
3. Executing a linux command:
	python3 micro1.py
		>> to run microservice 1
4. Open another terminal
4. Executing a linux command:
	python3 micro2.py
		>> to run microservice 2

# How to open the database to test changes
1. Open terminal and execute the linux command to install package "sqlitebrowser"
	sudo apt-get install sqlitebrowser
2. In Tuffix windows, search and open the package named "DB  Browser for SQLite"
3. In the project folder, drag the file named "project1.db" to the window "DB  Browser for SQLite"
4. Check tables in database if neccessary


# Test micro services
1. Install Postman application
    - https://www.postman.com
2. Import the "collections" and "global" variables (basic_test.json, excess_test.json, bogus_neg_test.json and postman_globals.json) to inspect or modify postman requests
3. Install Docker
    - https://docs.docker.com
4. Install Docker Compose
    - https://docs.docker.com/compose/install
5. Open docker-compose.yml with a text editor and change "volume" directory to where source files are located; additional information and configuration in the docker-compose.yml file
6. Run micro services on localhost; docker and postman requests configured to connect to micro services outside of containers
7. Change directory to source files (docker-compose.yml and postman JSON files)
8. Test with no load (postman/newman image should be pulled from docker repository automatically)
    - $ docker-compose up
9. Test with load
    - $ docker-compose up --scale excess_test=<number of containers or "simulated users">
10. Check docker compose logs
    - $ docker-compose logs basic_test
    - $ docker-compose logs bogus_neg_test
11. Save logs to file
    - $ docker-compose logs --no-color basic_test > basic_test_log.txt
    - $ docker-compose logs --no-color bogus_neg_test > bogus_neg_test_log.txt
12. Stop and remove running containers
    - $ docker-compose down

# Deployment and Operations 
This was tested on Tuffix environment
# Installation for foreman, Gunicorn3 and Caddy1

1. install Gunicorn3
$ sudo apt install --yes gunicorn3

2. install foreman 
sudo apt install ruby-foreman

3.installing Caddy1
$ curl https://getcaddy.com | bash -s personal
# Running the Procfile 
Before make sure that both the Procfile and Caddyfile are in the same directory as the project folder

1. Always use this command for foreman to confirm the micro services are recognized
$ foreman check

2a. to run the 1 instances for every microservices (basic test)
sudo foreman start -m posting=3,user=3


4a. Run caddy: ulimit -n 8192 && caddy

2b. to run the three instances for every microservices (including caddy)
$ sudo foreman start -m posting=3,user=3,caddy=1



3b. Two microservices will be accessed by:
http://localhost:2015/posts	(== load balancing, random to http://localhost:5000, http://localhost:5001, http://localhost:5002)
http://localhost:2015/users	(== load balancing, random to http://localhost:5100, http://localhost:5101, http://localhost:5102)

