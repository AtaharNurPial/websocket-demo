import json, os
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME')
index_name = os.environ.get('INDEX_NAME')
# URL = os.environ.get('CONNECTION_URL')
table = dynamodb.Table(table_name)
URL = 'https://azuk465590.execute-api.us-east-2.amazonaws.com/Prod/@connections'
client = boto3.client('apigatewaymanagementapi',endpoint_url = URL)
print(URL)

def table_response(userId):
    table_response = table.query(
    TableName = table_name,
    IndexName = index_name,
    KeyConditionExpression=Key('userId').eq(userId)
    )
    items = table_response['Items']
    print(items)
    return items

def sendMessage(connectionId, message):
    response = client.post_to_connection(
    Data=message,
    ConnectionId=connectionId
    )
    return response

def lambda_handler(event, context):

    print(event)
    connectionId = event['requestContext']['connectionId']
    body = json.loads(event['body'])
    userId = event['queryStringParameters']['userId']
    message = body['message']
    response = table_response(userId)
    print(response)
    try:
        result = sendMessage(connectionId,message)
        return {
            "statusCode": 200,
            "body": json.dumps({
            "message": "message sent...",
            "result": result
            }),
        }
    except Exception as e:
        print(e)
        return{
            "statusCode": 400,
             "body": json.dumps({
            "message": "unable to send message..."
            }),
        }
