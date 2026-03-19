#!/bin/sh

set -e

alembic upgrade head
python -m app.run.app_api.prod
