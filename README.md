Test task "REST API with FastAPI and MongoDB"
---------------------

## Problem statement:
```
Service (DatabaseService) should serve for CRUD (Create, Read, Update, Delete) operations related to files to be received from user and stored (can be in GridFS, can be on disk) on server. For each uploaded file should be created a document in MongoDB with brief information about file (who uploaded the file, when he did it, what he uploaded, etc). User IDs can be specified randomly, Auth subsystem implementation is not required.
```

## Building

1) Rename the example.env file, which is located in the database_service\core path to back.env

2) Use Docker Compose to build an image
```
docker-compose build
```

3) Run docker compose up to start the application
```
docker-compose up
```

4) Go to http://localhost:8000/docs to view and use the endpoints