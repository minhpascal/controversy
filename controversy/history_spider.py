# -*- coding: utf-8 -*-
import db
from querier import new_query

map(lambda entry: new_query(entry['Term']), db.histories())
