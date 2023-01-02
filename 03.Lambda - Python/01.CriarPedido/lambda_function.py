import boto3
from datetime import datetime
import json
import requests
import os

from transformar_pedido.solidcon import fazerDeParaPedido
from transformar_pedido.vtex import extrairPedidoSimplificado

secrets_client = boto3.client('secretsmanager')
secret_arn = os.environ['SECRET_ARN']
secret = secrets_client.get_secret_value(SecretId=secret_arn).get('SecretString')

dynamodb = boto3.resource('dynamodb') 

APP_KEY = json.loads(secret).get('AppKey')
APP_TOKEN = json.loads(secret).get('AppToken')

CNPJ_BARRA_SHOP = json.loads(secret).get('CnpjBarraShop')
CNPJ_IPANEMA = json.loads(secret).get('CnpjIpanema')

TABELA = os.environ['TABELA']

URL_SOLIDCON_BARRA_SHOP = json.loads(secret).get('UrlSolidconBarraShop')
URL_SOLIDCON_IPANEMA = json.loads(secret).get('UrlSolidconIpanema')

URL_VTEX = json.loads(secret).get('UrlVtex')

def lambda_handler(event, context):
    try:
        pedidoVtex = (str(event['body']['Orderld']))
        
        pedidoVtexCompleto = obterPedidoVtex(pedidoVtex)

        pedidoVtexSimplificado = extrairPedidoSimplificado(pedidoVtexCompleto)
        
        pedidoSolidcon = fazerDeParaPedido(pedidoVtexCompleto)
        
        respostaSolidcon = gravarPedidoSolidcon(pedidoSolidcon)
        
        gravarPedidoBanco(pedidoVtexSimplificado, pedidoSolidcon, respostaSolidcon)
        
    except Exception as e:
        print("Error: " + str(e))

def obterPedidoVtex(pedidoVtex):
    try:
        url = f'{URL_VTEX}{pedidoVtex}'
        headers = {
            "accept": "application/json",
            "X-VTEX-API-AppKey": APP_KEY,
            "X-VTEX-API-AppToken": APP_TOKEN
        }
        response = requests.get(url, headers=headers)
        return response.json()
    
    except Exception as e:
        print("Error: " + str(e))

def gravarPedidoSolidcon(pedidoSolidcon):
    try:
        pedido = pedidoSolidcon['numero']
        cnpjFilial = pedidoSolidcon['cnpj']
        codEcom = pedidoSolidcon['CodEcom']

        if cnpjFilial == CNPJ_BARRA_SHOP:
            print("Loja Barra Shop")
            url = f'{URL_SOLIDCON_BARRA_SHOP}/pedido/{pedido}/cnpj/{cnpjFilial}/Ecom/{codEcom}/GetPedido'
        
        elif cnpjFilial == CNPJ_IPANEMA:
            print("Loja Ipanema")
            url = f'{URL_SOLIDCON_IPANEMA}/pedido/{pedido}/cnpj/{cnpjFilial}/Ecom/{codEcom}/GetPedido'

        headers = {
            "accept": "application/json"
        }
        response = requests.get(url, headers=headers)
        
        return response.status_code
    
    except Exception as e:
        print("Error: " + str(e))
        
def gravarPedidoBanco(pedidoVtexSimplificado, pedidoSolidcon, respostaSolidcon):
    try:
        tabela = dynamodb.Table(TABELA)
        
        print("Adicionando pedido: ", pedidoVtexSimplificado['orderId'])

        vtex = json.dumps(pedidoVtexSimplificado)
        solidcon = json.dumps(pedidoSolidcon)
    
        tabela.put_item(
            Item={
                'ativo': 1,
                'pedido': pedidoVtexSimplificado['orderId'],
                'data': datetime.utcnow().replace(microsecond=0).isoformat(),
                'inseridoSolidcon': 1 if respostaSolidcon == 200 else 0,
                'vtex': vtex,
                'solidcon': solidcon
            }
        )
    
        print("Pedido: ", pedidoVtexSimplificado['orderId'], " adicionado")

    except Exception as e:
        print("Error: " + str(e))