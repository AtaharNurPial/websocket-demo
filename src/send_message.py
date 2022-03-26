import json, os
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME')
index_name = os.environ.get('INDEX_NAME')
URL = os.environ.get('CONNECTION_URL')
table = dynamodb.Table(table_name)
client = boto3.client('apigatewaymanagementapi',endpoint_url = URL)


def db_response(receiverId):
    response = table.query(
        TableName = table_name,
        IndexName = index_name,
        KeyConditionExpression = Key('userId').eq(receiverId)
    )
    return response

<<<<<<< HEAD
def sendMessage(message,connectionId):
    print('connectionIds List:',connectionId)
    # for connectionId in connectionIds:
    response = client.post_to_connection(
    Data=message,
    ConnectionId=connectionId
    )
    print('receiverConnectionId: ',connectionId)
    return response
=======
def sendMessage(message,connectionIds):
    print('connectionIds',connectionIds)
    responses = []
    for connectionId in connectionIds:
        client.post_to_connection(
        Data=message,
        ConnectionId=connectionId
        )
        print('receiverConnectionId: ',connectionId)
        responses.extend(connectionId)
    return responses
>>>>>>> master

def lambda_handler(event, context):

    print('event: ',event)
    connectionId = event['requestContext']['connectionId']
    body = json.loads(event['body'])
    receiverId = body['receiverId']
    message = body['message']
<<<<<<< HEAD
    # receiverConnectionIds = []
    table_response = db_response(receiverId)
    items = table_response['Items']
    print('Items: ',items)
    if items is not None:
        for item in items:
            receiverConnectionId = item['connectionId']
            # for item in items:
            #     res = [item['connectionId']]
            #     receiverConnectionIds.extend(res)
            # print('receiverConnectionId list: ',receiverConnectionIds)
        connection_response = table.query(
            TableName = table_name,
            KeyConditionExpression = Key('connectionId').eq(connectionId)
        )
        if connection_response['Items'] is not None:
            senderId = connection_response['Items'][0]['userId']
            payload = json.dumps({'Message': message, 'senderId': senderId})
            sendMessage(message=payload,connectionId=receiverConnectionId)            
            # client.post_to_connect(
            #     Data = payload,
            #     ConnectionId = receiverConnectionId
            # )
            return{
                'statusCode': 200,
=======
    try:
        receiverConnectionIds = []
        table_response = db_response(receiverId)
        items = table_response['Items']
        print('Items: ',items)
        if items is not None:
            for item in items:
                res = [item['connectionId']]
                receiverConnectionIds.extend(res)
            print('receiverConnectionId list: ',receiverConnectionIds)
            try:
                connection_response = table.query(
                    TableName = table_name,
                    KeyConditionExpression = Key('connectionId').eq(connectionId)
                )
                if connection_response['Items'] is not None:
                    senderId = connection_response['Items'][0]['userId']
                    payload = json.dumps({'Message': message, 'senderId': senderId})
                    try:
                        sendMessage(message=payload,connectionIds=receiverConnectionIds)
                        return{
                            'statusCode': 200,
                            'body': json.dumps({
                                'result': payload,
                                'message': "Message delivered..."
                            })
                        }
                    except Exception as e:
                        print(e)
                        return{
                            'statusCode': 400,
                            'body': json.dumps({
                            'message': "User is not connected."
                            })
                        }
                else:
                    return{
                        'statusCode': 400,
                        'body': json.dumps({
                            'message': "Message could not be delivered..."
                        })
                    }
            except Exception as e:
                print(e)
                return{
                'statusCode': 400,
>>>>>>> master
                'body': json.dumps({
                'message': "User is not connected."
                })
            }
        else:
            return{
<<<<<<< HEAD
            'statusCode': 400,
            'body': json.dumps({
                'message': "Message could not be delivered..."
            })
        }
            # except Exception as e:
            #     return{
            #         'statusCode': 400,
            #         'body': json.dumps({
            #             'message': "Message could not be delivered..."
            #         })
            #     }
    else:
        return{
=======
>>>>>>> master
                'statusCode': 400,
                'body': json.dumps({
                'message': "User is not connected."
                })
            }
<<<<<<< HEAD
    # except Exception as e:
    #     return{
    #         'statusCode': 400,
    #         'body': json.dumps({
    #         'message': "User is not connected."
    #         })
    #     }





# a_dict = [{'connectionId': 'Pe-h3dHOCYcAc6A=', 'userId': 'mahfuz'}, 
#         {'connectionId': 'Pe-hgd7ACYcAdmg=', 'userId': 'mahfuz'}, 
#         {'connectionId': 'Pe6PJd4BiYcCGmw=', 'userId': 'mahfuz'}, 
#         {'connectionId': 'Pe6PffuYCYcCJKQ=', 'userId': 'mahfuz'}]
# connectionIds = []

# for item in a_dict:
#     res = [item['connectionId']]
#     connectionIds.extend(res)
# print(connectionIds)



=======
    finally:
        return{
                'statusCode': 400,
                'body': json.dumps({
                'message': "User is not connected."
                })
            }
>>>>>>> master
