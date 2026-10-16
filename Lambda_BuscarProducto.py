import boto3
import json

def lambda_handler(event, context):
    token = event['headers']['Authorization']
    lambda_client = boto3.client('lambda')    
    payload_string = '{ "token": "' + token +  '" }'
    invoke_response = lambda_client.invoke(FunctionName="ValidarTokenAcceso",
                                           InvocationType='RequestResponse',
                                           Payload=payload_string)
    response = json.loads(invoke_response['Payload'].read())
    if response['statusCode'] == 403:
        return {
            'statusCode' : 403,
            'status' : 'Forbidden - Acceso No Autorizado'
        }       

    body = event['body']
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_productos')
    
    respuesta_db = table.get_item(
        Key={
            'tenant_id': body['tenant_id'],
            'producto_id': body['producto_id']
        }
    )
    
    return {
        'statusCode': 200,
        'producto': respuesta_db.get('Item', {})
    }
