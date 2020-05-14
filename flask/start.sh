#!/bin/bash

cd /home/dev/frontend && serve -s build &
cd /home/dev/flask && python3 server.py
