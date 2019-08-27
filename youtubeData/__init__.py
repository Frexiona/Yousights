# initi script to load all configuration and set application parameters

from flask import Flask
from flask_cors import CORS
from flask_restplus import Api
import logging
import logging.config
import yaml
import json
import os
import pymongo


def load_json_file(file_path):
    # load credentials
    with open(file_path) as fpath:
        data = json.load(fpath)
        return data


def create_mongodb_client():
    try:
        mongodb_client = pymongo.MongoClient("mongodb+srv://yousights:dQZ9UbGXMxS2C71R@yousightcluster0-fzaej.mongodb.net/test?retryWrites=true&w=majority")
        return mongodb_client
    except Exception as error:
        logging.error(f"Error while connecting to MongoDB: {error}")
        return False


application_path = os.path.dirname(os.path.abspath(__file__))

# Create logs directory
if not os.path.exists(application_path + "/logs"):
    os.makedirs(application_path + "/logs")

with open(application_path + "/config/logging.yml", "r") as stream:
    try:
        log_conf = yaml.safe_load(stream)
        logging.config.dictConfig(log_conf)
    except yaml.YAMLError as error:
        logging.error(f"Error while loading configuration: {error}")


credentials_file_path = application_path + "/config/credentials.json"
credentials = load_json_file(credentials_file_path)

app = Flask(__name__)
CORS(app)
api = Api(app, version="1.0", title="YouSights API", description="YouSights backend component")
api.namespaces.clear()  # clear default namespace
api = api.namespace("api/v1.0/", description="YouSights API")

# create the shared MongoDB client
shared_mongodb_client = create_mongodb_client()
