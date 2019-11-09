#!/bin/bash

export FLASK_APP=wsgi.py
export SECRET_KEY='butterlettuce'
export FLASK_DEBUG=1

python -m flask run #--host=0.0.0.0 --port=80
