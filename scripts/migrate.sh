#!/bin/bash

alembic revision --autogenerate -m "generate changes"
alembic upgrade head