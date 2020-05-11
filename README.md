# ompparser-demo

## Deployment using Docker

```bash
docker pull ouankou/ompparser:demo
docker run -p 5000:5000 --name ompparser_demo ouankou/ompparser:demo &
```

## Start Flask server

```bash
# make sure ompparser executable is in the PATH variable
cd flask
python3 server.py
```
