#!/bin/bash

export FLASK_APP=wsgi.py
export SECRET_KEY='butterlettuce'

flask run
