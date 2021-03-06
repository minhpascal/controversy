# -*- coding: utf-8 -*-
"""
    db.py
    ~~~~~

    DB functionality.
"""
import pymysql as sql
from config import *
from pymysql import Error
import time

def get_conn():
    return sql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME)


def get_cursor():
    conn = get_conn()
    return conn.cursor(), conn


def get_dict_cursor():
    conn = get_conn()
    return conn.cursor(sql.cursors.DictCursor), conn


def verify_user(username, password):
    cur, _ = get_cursor()
    cur.execute('''
        SELECT *
        FROM Users
        WHERE
        Id = %s AND
        Password = MD5(%s);''', (username, password,))
    return cur.fetchone() is not None


def user_exists(username):
    cur, _ = get_cursor()
    cur.execute('''
        SELECT *
        FROM Users
        WHERE
        Id = %s;''', (username,))
    return cur.fetchone() is not None


def create_user(email, name, password, school):
    cur, _ = get_cursor()
    cur.execute('''
        INSERT INTO
        Users
        (Name, Id, School, Password, Logins)
        VALUES
        (%s, %s, %s, MD5(%s), 0);''', (name, email, school, password,))
    return _.commit()


def dump_user(username):
    """return all rows about user
    """
    cur, _ = get_dict_cursor()
    cur.execute('''
        SELECT *
        FROM Users
        WHERE
        Id = %s;''', (username,))
    return cur.fetchone()


def logged_in(user):
    """increment user's login count
    """
    cur, _ = get_cursor()
    cur.execute('''
        UPDATE Users
        SET Logins = Logins + 1
        WHERE Id = %s''', user)
    return _.commit()


def user_history(username):
    """get query history
    """
    cur, _ = get_dict_cursor()
    cur.execute('''
        SELECT Term, Performed
        FROM Histories
        WHERE
        Originator = %s;''', (username,))
    return cur.fetchall()


def clear_queries(username):
    """clear a user's history.
    Notice this doesn't clear Queries (yes, confusing name)
        since that's anonymous.
    """
    cur, _ = get_cursor()
    cur.execute('''
        DELETE FROM
        Histories
        WHERE
        Originator = %s;''', (username,))
    _.commit()


def drop_account(username):
    """delete someone's account
    """
    clear_queries(username)
    cur, _ = get_cursor()
    cur.execute('''
        DELETE FROM
        Users
        WHERE
        Id = %s;''', (username,))
    _.commit()


def histories():
    """get all queries
    """
    cur, _ = get_dict_cursor()
    cur.execute('''
        SELECT *
        FROM Histories;''')
    return cur.fetchall()


def unique_user_query(keyword, user):
    """checks if user has performed query before
    """
    cur, _ = get_cursor()
    cur.execute('''
        SELECT *
        FROM Histories
        WHERE
        Originator=%s
        AND
        Term=%s;''', (user, keyword,))
    return cur.fetchone() is None


def update_history(keyword, user):
    """updates date for identical query (per user) in Histories table
    """
    cur, _ = get_cursor()
    cur.execute('''
        UPDATE Histories
        SET Performed=Performed
        WHERE
        Originator=%s AND
        Term=%s;''', (user, keyword))
    _.commit()


def append_history(keyword, user):
    """adds new entry in Histories table
    """
    cur, _ = get_cursor()
    cur.execute('''
        INSERT INTO
        Histories (
        Term,
        Originator) VALUES (%s, %s);''', (keyword, user))
    try:
        _.commit()
    except:
        return


def append_queries(keyword, escore):
    """adds new entry (perhaps a duplicate) to Queries table
    Not user-associated. See Histories for user-based history.
    """
    cur, _ = get_cursor()
    cur.execute('''
        INSERT INTO
        Queries (
        Term,
        EntropyScore
        ) VALUES (%s, %s)''', (keyword, str(escore)))
    _.commit()


def keyword_trend(keyword):
    """get scores from past queries
    """
    cur, _ = get_dict_cursor()
    cur.execute('''
        SELECT EntropyScore, Performed
        FROM 
        Queries
        WHERE
        Term = %s''', keyword)
    return cur.fetchall()


def most_controversial():
    """get the terms (to be sorted)
    """
    cur, _ = get_dict_cursor()
    cur.execute('''
        SELECT Term, EntropyScore
        FROM Queries
        ORDER BY EntropyScore DESC''')
    return cur.fetchall()


def add_mturk_read(author, url):
    """add entry to mturk
    """
    cur, _ = get_cursor()
    cur.execute('''
        INSERT INTO
        MturkRead
        (Author, URL)
        VALUES 
        (%s, %s)''', (author, url))
    _.commit()
