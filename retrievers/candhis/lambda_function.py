from waves_candhis_retriever import get_candhis_data
import boto3
from decimal import Decimal
import json

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    extracts = get_candhis_data('Y2FtcD0wNjQwMg==')
    print(extracts[0])
    table = dynamodb.Table('surfcheck-candhis')
    for e in extracts:
        item = json.loads(json.dumps(e.to_dict()), parse_float=Decimal)
        item['id'] = f"{item['campaign_id']}@{item['dt']}"
        table.put_item(Item=item)