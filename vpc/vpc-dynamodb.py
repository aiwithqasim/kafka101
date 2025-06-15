import boto3
import json
client_dynamo=boto3.resource('dynamodb',region_name='us-east-1')
table=client_dynamo.Table("dynamodb-my-mpc-ec2-vpc-endpoint")
records=""

with open('./data-vpc-dynamodb.json','r') as datafile:
    records=json.load(datafile)

count=0
for i in records:
    i['roll_no']=str(count)
    print(i)
    i['X']=str(i['X'])
    i['Y']=str(i['Y'])
    response=table.put_item(Item=i)
    count+=1