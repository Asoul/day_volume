#!/bin/bash
cd /home/asoul/day_volume/
/usr/bin/python crawl.py
/usr/bin/git add .
/usr/bin/git commit -m "daily update"
/usr/bin/git push
