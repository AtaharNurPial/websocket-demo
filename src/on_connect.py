import json, os
import boto3

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME')
table = dynamodb.Table(table_name)

def connect_db(connectionId):
    table_response = table.put_item(
        TableName = table_name,
        Item=connectionId
    )
    print(table_response)
    return table_response

def lambda_handler(event, context):

    print(event)
    connectionId = json.loads(event['requestContext']['connectionId'])

    try:
        response = connect_db(connectionId)
        return {
            "statusCode": 200,
            "body": json.dumps({
                "result": response,
                "message": "Connected...",
            }),
        }
    except Exception as e:
        return{
            "statusCode": 400,
            "body": json.dumps({
                "message": "Unable to Connect...",
            }),
        }
