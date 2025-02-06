#!/bin/sh
ACCESS_TOKEN=`curl -X POST "http://127.0.0.1:8000/token" \
     -d "username=user1&password=password1" \
     -H "Content-Type: application/x-www-form-urlencoded" | jq -r '.access_token'`
echo $ACCESS_TOKEN
curl -X POST "http://127.0.0.1:8000/tasks/" -H "Authorization: Bearer $ACCESS_TOKEN"   -H "Content-Type: application/json" -d '{"message": "Hello, Celery!"}'
