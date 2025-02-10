#!/bin/sh
ACCESS_TOKEN=`curl -X POST "http://127.0.0.1:8000/token" \
     -d "username=user1&password=password1" \
     -H "Content-Type: application/x-www-form-urlencoded" | jq -r '.access_token'`
echo $ACCESS_TOKEN
curl -X GET "http://127.0.0.1:8000/task/"$1 -H "Authorization: Bearer $ACCESS_TOKEN"   -H "Content-Type: application/json" 
#-d '{ "task_id": "fb024782-d62c-43c9-aac7-2f64486ba1a9" }'
