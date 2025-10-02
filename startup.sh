#!/bin/bash
set -e

# Install MS ODBC driver
apt-get update && \
    apt-get install -y curl gnupg apt-transport-https && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/12/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql18 unixodbc-dev

# Then run your app
gunicorn -w 1 -k uvicorn.workers.UvicornWorker app:app --bind=0.0.0.0:8000
