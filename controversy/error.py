# -*- coding: utf-8 -*-
"""
    error.py
    ~~~~~~~
    Proper error handling for RESTful API.
"""

class UsageError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
            
    def to_dict(self):
        rv = {'message' : self.message, 'error' : 1}
        return rv
