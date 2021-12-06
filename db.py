import sqlite3
import hashlib
conn = sqlite3.connect('data.db')
c = conn.cursor()

def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT UNIQUE,password TEXT,keyword text)')


def add_userdata(username,password,keyword):
	c.execute('INSERT INTO userstable(username,password,keyword) VALUES (?,?,?)',(username,password,keyword))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data

def search_user(username,keyword):
	c.execute('SELECT * FROM userstable WHERE username =? AND keyword = ?',(username,keyword))
	data = c.fetchall()
	return data
def change_password(username,new_password):
	c.execute('UPDATE userstable SET password ="{}" WHERE username="{}"'.format(new_password,username))
	conn.commit()
def drop():
	c.execute("DROP TABLE userstable")
	conn.commit()


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data

def create_table():
	c.execute('CREATE TABLE IF NOT EXISTS blogtable(author TEXT,title TEXT,article TEXT,postdate,DATE)')
	c.execute('CREATE TABLE IF NOT EXISTS commenttable(username TEXT,title TEXT,comment TEXT,postdate,DATE)')
	c.execute('CREATE TABLE IF NOT EXISTS rating(rate NUMBER,title TEXT,num_exp NUMBER)')

def fetch_rating(title):
	c.execute('SELECT * FROM rating WHERE title =?',(title,))
	data = c.fetchall()
	return data

def update_rating_at(title,rating,num_exp):
	c.execute('UPDATE rating SET rate ="{}", num_exp ="{}" WHERE title="{}"'.format(rating,num_exp,title))
	conn.commit()

def insert_rating(title,rating):
	c.execute('INSERT INTO rating(rate,title,num_exp) VALUES (?,?,?)',(rating,title,1))
	conn.commit()


def add_data(author,title,article,postdate):
	c.execute('INSERT INTO blogtable(author,title,article,postdate) VALUES (?,?,?,?)',(author,title,article,postdate))
	conn.commit()

def add_commment(username,title,comment,postdate):
	c.execute('INSERT INTO commenttable(username,title,comment,postdate) VALUES (?,?,?,?)',(username,title,comment,postdate))
	conn.commit()

def fetch_comments(title):
	c.execute('SELECT * FROM commenttable WHERE title=?',(title,))
	data = c.fetchall()
	return data

def view_all_notes():
	c.execute('SELECT * FROM blogtable')
	data = c.fetchall()
	# for row in data:
	# 	print(row)
	return data

def view_all_titles():
	c.execute('SELECT DISTINCT title FROM blogtable')
	data = c.fetchall()
	# for row in data:
	# 	print(row)
	return data

def view_all_titles_by_author(author):
	c.execute('SELECT DISTINCT title FROM blogtable WHERE author="{}"'.format(author))
	data = c.fetchall()
	# for row in data:
	# 	print(row)
	return data

def get_single_blog(title):
	c.execute('SELECT * FROM blogtable WHERE title="{}"'.format(title))
	data = c.fetchall()
	return data

def get_blog_by_title(title):
	c.execute('SELECT * FROM blogtable WHERE title="{}"'.format(title))
	data = c.fetchall()
	return data

def get_blog_by_author(author):
	c.execute('SELECT * FROM blogtable WHERE author="{}"'.format(author))
	data = c.fetchall()
	return data
 

def get_blog_by_msg(article):
	c.execute("SELECT * FROM blogtable WHERE article like '%{}%'".format(article))
	data = c.fetchall()
	return data

def edit_blog_author(author,new_author):
	c.execute('UPDATE blogtable SET author ="{}" WHERE author="{}"'.format(new_author,author))
	conn.commit()
	data = c.fetchall()
	return data

def edit_blog_title(title,new_title):
	c.execute('UPDATE blogtable SET title ="{}" WHERE title="{}"'.format(new_title,title
		))
	conn.commit()
	data = c.fetchall()
	return data


def edit_blog_article(article,new_article):
	c.execute('UPDATE blogtable SET title ="{}" WHERE title="{}"'.format(new_article,article
		))
	conn.commit()
	data = c.fetchall()
	return data

def delete_data(title):
	c.execute('DELETE FROM blogtable WHERE title="{}"'.format(title))
	conn.commit()

def delete_user(user):
	c.execute('DELETE FROM userstable WHERE username="{}"'.format(user))
	conn.commit()
