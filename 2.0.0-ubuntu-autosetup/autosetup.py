#!/bin/evn python

from http.client import HTTPConnection
from json import dumps
from os import environ
from sys import exit
from time import sleep


CONFIG = {
    "action": "enable_cluster",
    "bind_address": "0.0.0.0",
    "port": "5984",
    "username": environ.get("COUCHDB_USER", "admin"),
    "password": environ.get("COUCHDB_PASSWORD", "password")
}

while True:
    try:
        connection = HTTPConnection("localhost:5984")
        connection.request("GET", "/_membership")
        break
    except:
        sleep(0.5)
response = connection.getresponse()
if response.status == 401:
    # CouchDB already configured
    exit()
response.read()

connection = HTTPConnection("localhost:5984")
connection.request("POST", "/_cluster_setup", body=dumps(CONFIG), headers={"Content-Type": "application/json"})
connection.getresponse()
connection.close()
