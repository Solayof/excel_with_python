#!/usr/bin/python3
"initialzing db"
from backup.engine.storage import Dbstorage


storage = Dbstorage()
storage.init()