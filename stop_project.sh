# !/bin/bash

cd database_service/core
kill $(cat database_service.pid)
rm database_service.pid
