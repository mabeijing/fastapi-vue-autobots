#!/bin/bash

source /home/ubuntu/virtualenv/fastapi-vue-autobots/bin/activate

cd /home/ubuntu/projects/fastapi-vue-autobots

uvicorn app.main:app --reload