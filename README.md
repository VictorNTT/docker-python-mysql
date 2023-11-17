# General 
Demonstrate docker, docker-compose, Alpin Linux, Python Flask, MySQL, Redis in-memomory cache.

# Date 
Oct 24, 2023

# Build and run 
$ docker-compose up --build

Then access http://localhost:8000/ to see data from:
(a) MySQL 'world' database (comes in with the installation of MySQL) on the host machine (outside of a docker container); or
(b) MYSQL 'testdb' database created on deploying 'mysql' container, running within a docker container

