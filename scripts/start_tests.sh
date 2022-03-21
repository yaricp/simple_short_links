#!/usr/bin/env bash

set -e
set -x

env PYTHONPATH=:/app; pytest /app/tests "${@}"

# --cov=app --cov-report=term-missing