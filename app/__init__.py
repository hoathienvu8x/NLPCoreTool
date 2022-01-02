# -*- coding: utf-8 -*-

import os
from flask import Flask

engine = Flask(__name__)

ABSPATH = os.path.dirname(os.path.dirname(__file__))
DATA_FOLDER = os.path.join(ABSPATH,"data")

engine.config['SECRET_KEY'] = ''
engine.config["JSON_AS_ASCII"] = False
engine.config["JSONIFY_PRETTYPRINT_REGULAR"] = False

engine.config["DEBUG"] = False
engine.config["ENV"] = "production"
engine.config["PORT"] = 7500

from .views import *
