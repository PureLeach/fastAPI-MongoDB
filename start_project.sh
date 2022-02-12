# !/bin/bash

source .venv/bin/activate
cd database_service
python main.py &
P1=$!
echo $P1 >> ./database_service.pid
