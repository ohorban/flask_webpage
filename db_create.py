import sqlite3

con = sqlite3.connect('database.db')
cur = con.cursor()

cur.executescript('''
create table users (
    id integer primary key,
    username text not null unique,
    password text not null,
    age integer
);
create table messages (
    id integer primary key,
    sender_id text not null,
    message text not null,
    created_at timestamp not null default current_timestamp
);
insert into users (username, password, age) values ('alex', '12345', 19);
insert into users (username, password, age) values ('jake', '12345', 21);
insert into users (username, password, age) values ('eve', '12345', 16);

insert into messages (sender_id, message) values ('alex', 'I just got in my dream college!');
insert into messages (sender_id, message) values ('jake', 'I love CS');
insert into messages (sender_id, message) values ('eve', 'I used to hate anime but now I love it more than my life');
insert into messages (sender_id, message) values ('alex', 'Guys do you like the social network I created?');
insert into messages (sender_id, message) values ('jake', 'I need to go do homework now!');
''')