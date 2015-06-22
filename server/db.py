# -*- coding: utf-8 -*-
"""
    db.py
    ~~~~~

    db functionality.

    :copyright: (c) 2015 |contributors|.
    :license: BSD, see LICENSE for more details.
"""
import pymysql as sql
from config import *
from pymysql import Error


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


def create_user(form):
    cur, _ = get_cursor()
    cur.execute('''
        INSERT INTO
        Users
        (Name, Id, School, Password)
        VALUES
        (%s, %s, %s, MD5(%s));''', (form['Name'], form['Id'], form['School'], form['Password'],))
    return _.commit()


def dump_user(username):
    """
    return all rows about user
    """
    cur, _ = get_dict_cursor()
    cur.execute('''
        SELECT *
        FROM Users
        WHERE
        Id = %s;''', (username,))
    return cur.fetchone()


def user_history(username):
    """
    get query history
    """
    cur, _ = get_dict_cursor()
    cur.execute('''
        SELECT Term, Performed
        FROM Histories
        WHERE
        Originator = %s;''', (username,))
    return cur.fetchall()


def histories():
    """
    get all queries
    """
    cur, _ = get_dict_cursor()
    cur.execute('''
        SELECT *
        FROM Histories''')
    return cur.fetchall()


def unique_user_query(keyword, user):
    """
    checks if user has performed query before
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


def update_history(keyword, date, user):
    """
    updates date for identical query (per user) in Histories table
    """
    cur, _ = get_cursor()
    cur.execute('''
        UPDATE Histories
        SET
        Performed=%s
        WHERE
        Originator=%s
        AND
        Term=%s;''', (date, user, keyword,))
    _.commit()


def append_history(keyword, date, user):
    """
    adds new entry in Histories table
    """
    cur, _ = get_cursor()
    cur.execute('''
        INSERT INTO
        Histories (
        Term,
        Originator,
        Performed) VALUES (%s, %s, %s);''', (keyword, user, date,))

    try:
        _.commit()
    except:
        return
