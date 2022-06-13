import json, os, boto3

dynamodb = boto3.resource("dynamodb")
table_name = os.environ.get("TABLE_NAME")
table = dynamodb.Table(table_name)


def delete_connection(connectionId):
    table_response = table.delete_item(
        TableName=table_name,
        Key={
            "connectionId": connectionId,
        },
    )
    print(table_response)
    return table_response


def lambda_handler(event, context):

    print(event)
    connectionId = event["requestContext"]["connectionId"]

    try:
        response = delete_connection(connectionId)
        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "result": response,
                    "message": "Disconnected...",
                }
            ),
        }
    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps(
                {
                    "message": "Some error occurred...",
                }
            ),
        }
