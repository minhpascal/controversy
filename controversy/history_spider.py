# -*- coding: utf-8 -*-
import db
from querier import new_query
print("\t\tthis will take a while...")
map(lambda entry: new_query(entry['Term']), db.histories())
