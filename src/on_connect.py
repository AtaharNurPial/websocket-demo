import json, os
import boto3

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME')
table = dynamodb.Table(table_name)

# def connect_db(connectionId,userId):
#     table_response = table.put_item(
#         TableName = table_name,
#         Item = {
#             'connectionId': connectionId ,
#             'userId': userId
#         }
#     )
#     print(table_response)
#     return table_response

def connect_db(params):
    table_response = table.put_item(
        TableName = table_name,
        Item = params
    )
    print(table_response)
    return table_response

def lambda_handler(event, context):

    print(event)
    connectionId = event['requestContext']['connectionId']
    userId = event['queryStringParameters']['userId']
    params = {'connectionId': connectionId, 'userId': userId}

    try:
        response = connect_db(params)
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
