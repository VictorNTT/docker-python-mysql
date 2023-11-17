--DROP database if exists testdb;
--create database testdb;
use testdb;
create table Quote (
    quote VARCHAR(200)
);

insert into Quote values 
    ('Love what you do and you will work every hour!')
    ,('The red fox jumps over the lazy dog')
    ,('Who let the dog out?')
    ,('Oops! I did it again!') ;