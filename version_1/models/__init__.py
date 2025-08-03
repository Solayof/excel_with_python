#!/usr/bin/python3
"initialzing db"
from models.engine.storage import Dbstorage


storage = Dbstorage()
storage.init()