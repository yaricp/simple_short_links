#!/bin/bash

uvicorn --port 80 --host 0.0.0.0 main:app --reload