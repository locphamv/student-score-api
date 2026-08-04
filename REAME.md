# Student Score API

A simple student score management API built with FastAPI.

## Current endpoints

- `GET /`
- `GET /health`
- `GET /students`
- `GET /students/{student_id}`

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
fastapi dev main.py
