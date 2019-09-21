#!/bin/bash

export FLASK_APP=wsgi.py
export FLASK_DEBUG=1
export APP_CONFIG_FILE=config.py
export SECRET_KEY='butterlettuce'

export SQLALCHEMY_DATABASE_URI='sqlite:///chat.sqlite'
export SQLALCHEMY_TRACK_MODIFICATIONS=0

flask run
