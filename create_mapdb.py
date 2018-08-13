# -*- coding: utf-8 -*-
"""
Created on Sun May 14 14:33:15 2017

@author: ek028m
"""

import sqlite3
import csv

conn = sqlite3.connect('map.db')
c = conn.cursor()

# Once created, no need to run again.
def create_tables():
     c.execute('CREATE TABLE IF NOT EXISTS nodes(id INTEGER PRIMARY KEY NOT NULL, lat REAL, lon REAL, user TEXT, uid INTEGER, version INTEGER, changeset INTEGER, timestamp TEXT)')
     c.execute('CREATE TABLE IF NOT EXISTS nodes_tags(id INTEGER, key TEXT, value TEXT, type TEXT, FOREIGN KEY (id) REFERENCES nodes(id))')
     c.execute('CREATE TABLE IF NOT EXISTS ways(id INTEGER PRIMARY KEY NOT NULL, user TEXT, uid INTEGER, version TEXT, changeset INTEGER, timestamp TEXT)')
     c.execute('CREATE TABLE IF NOT EXISTS ways_tags(id INTEGER NOT NULL, key TEXT NOT NULL, value TEXT NOT NULL, type TEXT, FOREIGN KEY (id) REFERENCES ways(id))')
     c.execute('CREATE TABLE IF NOT EXISTS ways_nodes(id INTEGER NOT NULL,node_id INTEGER NOT NULL, position INTEGER NOT NULL, FOREIGN KEY (id) REFERENCES ways(id), FOREIGN KEY (node_id) REFERENCES nodes(id))')
     
create_tables()
conn.commit()

    
def insert_nodes():
    with open('new_nodes.csv','r') as fin:
        # csv.DictReader uses first line in file for column headings by default
        dr = csv.DictReader(fin) # comma is default delimiter
        to_db = [(i['id'].decode('utf-8'), i['lat'].decode('utf-8'),i['lon'].decode('utf-8'), i['user'].decode('utf-8'), i['uid'].decode('utf-8'), i['version'].decode('utf-8'), i['changeset'].decode('utf-8'), i['timestamp'].decode('utf-8')) for i in dr]
    
    # insert the data
    c.executemany('INSERT INTO nodes(id, lat, lon, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?);', to_db)
    # commit the changes
    conn.commit()

def insert_nodes_tags():
    with open('new_nodes_tags.csv','r') as fin:
        dr = csv.DictReader(fin) 
        to_db = [(i['id'].decode('utf-8'), i['key'].decode('utf-8'),i['value'].decode('utf-8'), i['type'].decode('utf-8')) for i in dr]
        #for i in dr:
            #if i['id']:
                #to_db = [(i['id'].decode('utf-8'), i['key'].decode('utf-8'),i['value'].decode('utf-8'), i['type'].decode('utf-8'))]
    
    c.executemany('INSERT INTO nodes_tags(id, key, value, type) VALUES (?, ?, ?, ?);', to_db)
    conn.commit()
    
def insert_ways():
    with open('new_ways.csv','r') as fin:
        dr = csv.DictReader(fin) 
        to_db = [(i['id'].decode('utf-8'), i['user'].decode('utf-8'),i['uid'].decode('utf-8'), i['version'].decode('utf-8'), i['changeset'].decode('utf-8'), i['timestamp'].decode('utf-8')) for i in dr]
    
    c.executemany('INSERT INTO ways(id, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?);', to_db)
    conn.commit()
    
def insert_ways_tags():
    with open('new_ways_tags.csv','r') as fin:
        dr = csv.DictReader(fin) 
        to_db = [(i['id'].decode('utf-8'), i['key'].decode('utf-8'),i['value'].decode('utf-8'), i['type'].decode('utf-8')) for i in dr]
    
    c.executemany('INSERT INTO ways_tags(id, key, value, type) VALUES (?, ?, ?, ?);', to_db)
    conn.commit()
    
def insert_ways_nodes():
    with open('new_ways_nodes.csv','r') as fin:
        dr = csv.DictReader(fin) 
        to_db = [(i['id'].decode('utf-8'), i['node_id'].decode('utf-8'),i['position'].decode('utf-8')) for i in dr]
    
    c.executemany('INSERT INTO ways_nodes(id, node_id, position) VALUES (?, ?, ?);', to_db)
    conn.commit()

insert_nodes()
insert_nodes_tags()
insert_ways()
insert_ways_tags()
insert_ways_nodes()

conn.close()