#!/bin/bash
cd /mnt/data/xtrt/projects/python/api_mea/ && source /mnt/data/xtrt/projects/python/api_mea/venv/bin/activate && uvicorn main:app  --reload --host 192.168.50.228 --port 8077
