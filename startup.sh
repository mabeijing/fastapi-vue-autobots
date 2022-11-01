#!/bin/bash

source /home/ubuntu/virtualenv/fastapi-vue-autobots/bin/activate

cd /home/ubuntu/projects/fastapi-vue-autobots || return

uvicorn app.main:app --reload