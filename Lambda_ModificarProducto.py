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

    producto_modificado = event['body']
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_productos')
    
    table.put_item(Item=producto_modificado)
    
    return {
        'statusCode': 200,
        'mensaje': 'Producto modificado exitosamente'
    }
