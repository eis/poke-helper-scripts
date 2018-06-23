from __future__ import print_function

import boto3
import json

print('Loading function')


def handler(event, context):
    '''Provide an event that contains the following keys:

      - operation: one of the operations in the operations dict below
      - tableName: required for operations that interact with DynamoDB
      - payload: a parameter to pass to the operation being performed
    '''
    print("Received event: " + json.dumps(event, indent=2))

    body = json.loads(event['body'])

    if not 'operation' in body:
        raise ValueError('operation not found in body')
    operation = body['operation']

    if 'tableName' in event:
        dynamo = boto3.resource('dynamodb').Table(event['tableName'])

    operations = {
        'create': lambda x: dynamo.put_item(**x),
        'read': lambda x: dynamo.get_item(**x),
        'update': lambda x: dynamo.update_item(**x),
        'delete': lambda x: dynamo.delete_item(**x),
        'list': lambda x: dynamo.scan(**x),
        'echo': lambda x: x,
        'ping': lambda x: 'pong'
    }

    print("Parsed operation: " + operation)  
    print("Using payload: " + json.dumps(body['payload']))

    if operation in operations:
        return {
            'statusCode': 200,
            'body': json.dumps(body['payload'])
        }
        # return operations[operation](json.dumps(body['payload']))
    else:
        raise ValueError('Unrecognized operation "{}"'.format(operation))
