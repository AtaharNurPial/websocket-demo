import json, os
import boto3

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME')
table = dynamodb.Table(table_name)

def delete_connection(userId,connectionId):
    table_response = table.delete_item(
        TableName = table_name,
        Key={
            'connectionId': connectionId,
            'userId' : userId
        }
    ) 
    print(table_response)
    return table_response

def lambda_handler(event, context):

    print(event)
    userId = event['queryStringParameters']['userId']
    connectionId = event['requestContext']['connectionId']

    try:
        response = delete_connection(connectionId,userId)
        return {
            "statusCode": 200,
            "body": json.dumps({
                "result": response,
                "message": "Disconnected...",
            }),
        }
    except Exception as e:
        return{
            "statusCode": 400,
            "body": json.dumps({
                "message": "Unable to disconnect...",
            }),
        }
