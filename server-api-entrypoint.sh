#!/bin/sh

set -e

alembic upgrade head
python -m app.run.server_api.prod
