#!/bin/bash
systemctl stop api_mea.service && kill -9 $(sudo lsof -t -i:8077)
