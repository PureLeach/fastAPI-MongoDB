# !/bin/bash

cd database_service
source .venv/bin/activate
python main.py &
P1=$!
echo $P1 >> ./database_service.pid
