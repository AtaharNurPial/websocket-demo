import json, os
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME')
# index_name = os.environ.get('INDEX_NAME')
# URL = os.environ.get('CONNECTION_URL')
table = dynamodb.Table(table_name)


def sendMessage(message,connectionId):
    URL = 'https://azuk465590.execute-api.us-east-2.amazonaws.com/Prod'
    client = boto3.client('apigatewaymanagementapi',endpoint_url = URL)
    response = client.post_to_connection(
    Data=message,
    ConnectionId=connectionId
    )
    return response

def lambda_handler(event, context):

    print(event)
    connectionId = event['requestContext']['connectionId']
    body = json.loads(event['body'])
    receiverId = body['receiverId']
    message = body['message']
    table_response = table.scan(
        TableName = table_name,
        FilterExpression = Key('userId').eq(receiverId)
    )
    if table_response['Items'] is not None:
        receiverConnectionId = table_response['Items'][0]['connectionId']
        connection_response = table.scan(
            TableName = table_name,
            FilterExpression = Key('connectionId').eq(connectionId)
        )
        if connection_response['Items'] is not None:
            senderId = connection_response['Items'][0]['userId']
            payload = json.dumps({'Message': message, 'senderId': senderId})
            sendMessage(message=payload,connectionId=receiverConnectionId)
            return{
                'statusCode': 200,
                'body': json.dumps({
                    'result': payload,
                    'message': "Message delivered..."
                })
            }
        else:
            return{
                'statusCode': 200,
                'body': json.dumps({
                    'message': "Message could not be delivered..."
                })
            }
    else:
        return{
            'statusCode': 200,
            'body': json.dumps({
            'message': "User is not connected."
            })
        }
    # print(table_response)
    # try:
    #     result = sendMessage(connectionId,message)
    #     return {
    #         "statusCode": 200,
    #         "body": json.dumps({
    #         "message": "message sent...",
    #         "result": result
    #         }),
    #     }
    # except Exception as e:
    #     print(e)
    #     return{
    #         "statusCode": 400,
    #          "body": json.dumps({
    #         "message": "unable to send message..."
    #         }),
    #     }
