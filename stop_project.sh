# !/bin/bash

cd database_service
kill $(cat database_service.pid)
rm database_service.pid
