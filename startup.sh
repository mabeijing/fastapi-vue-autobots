#!/bin/bash

source /home/ubuntu/virtualenv/fastapi-vue-autobots-3.11.0/bin/activate

cd /home/ubuntu/projects/fastapi-vue-autobots || return

uvicorn app.main:app --reload