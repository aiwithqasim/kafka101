import boto3
import json
from decimal import Decimal

client_dynamo = boto3.resource('dynamodb', region_name='us-east-1')
table = client_dynamo.Table("dynamodb-my-mpc-ec2-vpc-endpoint")

with open('./data-vpc-dynamodb.json', 'r') as datafile:
    records = json.load(datafile)

for item in records:
    item['X'] = Decimal(str(item['X']))
    item['Y'] = Decimal(str(item['Y']))

    try:
        table.put_item(Item=item)
        print(f"Inserted: {item}")
    except Exception as e:
        print(f"Error inserting {item}: {e}")

print(f"Done. {len(records)} items processed.")