#!/bin/sh
ACCESS_TOKEN=`curl -X POST "http://127.0.0.1:8000/token" \
     -d "username=user&password=password" \
     -H "Content-Type: application/x-www-form-urlencoded" | jq -r '.access_token'`
echo $ACCESS_TOKEN
curl -X POST http://localhost:8000/create-instances/ \
   -H "Content-Type: application/json" \
   -H "Authorization: Bearer $ACCESS_TOKEN" \
   -d '{
       "instance_type": "t2.micro",
       "ami_id": "ami-02d3fd86e6a2f5122",
       "key_name": "NEW_KCR",
       "security_group_ids": ["sg-09ac434d5bead2ab1"],
       "namespace": "testCluster",
       "min_count": 2,
       "max_count": 2
   }'
