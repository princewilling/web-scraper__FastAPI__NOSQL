import pathlib
import os

from dotenv import load_dotenv

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

import config


settings = config.get_settings()

ASTRA_DB_CLIENT_ID = settings.db_client_id
ASTRA_DB_CLIENT_SECRET = settings.db_client_secret 

BASE_DIR = pathlib.Path(__file__).resolve().parent
CLUSTER_BUNDLE = BASE_DIR / "ignored" / 'connect.zip'

def get_cluster():
    cloud_config= {
            'secure_connect_bundle': CLUSTER_BUNDLE
    }
    auth_provider = PlainTextAuthProvider(ASTRA_DB_CLIENT_ID, ASTRA_DB_CLIENT_SECRET)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    return cluster


def get_session():
    cluster = get_cluster()
    session = cluster.connect()
    return session 

session = get_session()
row = session.execute("select release_version from system.local").one()
if row:
      print(row[0])
else:
      print("An error occurred.")
      