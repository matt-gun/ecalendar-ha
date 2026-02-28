#!/bin/sh
set -e

nginx &
sleep 2
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
