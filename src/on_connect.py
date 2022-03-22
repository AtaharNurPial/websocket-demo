import json, os
import boto3

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME')
table = dynamodb.Table(table_name)

def connect_db(userId,connectionId):
    table_response = table.put_item(
        TableName = table_name,
        Item={
            'connectionId': connectionId,
            'userId': userId
        }
    )
    print(table_response)
    return table_response

def lambda_handler(event, context):

    print(event)
    connectionId = event['requestContext']['connectionId']
    userId = event['queryStringParameters']['userId']

    try:
        response = connect_db(connectionId,userId)
        return {
            "statusCode": 200,
            "body": json.dumps({
                "result": response,
                "message": "Connected...",
            }),
        }
    except Exception as e:
        print(e)
        return{
            "statusCode": 400,
            "body": json.dumps({
                "message": "Unable to Connect...",
            }),
        }
