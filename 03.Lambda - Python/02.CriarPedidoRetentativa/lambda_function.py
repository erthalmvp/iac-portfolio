import boto3
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime
import json
import requests
import os

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
        pedidoPendente = verificarPedidoPendente()
        
        respostaSolidcon = gravarPedidoSolidcon(pedidoPendente)
        
        atualizarPedidoBanco(pedidoPendente, respostaSolidcon)
        
    except Exception as e:
        print("Error: " + str(e))

def verificarPedidoPendente():
    try:
        tabela = dynamodb.Table(TABELA)

        print("Procurando pedido...")

        resposta = tabela.query(KeyConditionExpression=Key('ativo').eq(1), FilterExpression=Attr('inseridoSolidcon').eq(0))

        itens = resposta['Items']

        if len(itens) > 0:
            pedidos = []
            for item in itens:
                ativo = item['ativo']
                pedido = item['pedido']
                inseridoSolidcon = item['inseridoSolidcon']
                vtex = item['vtex']
                solidcon = item['solidcon']

                print("Pedido encontrado: ", pedido)
                print("Status: ", "Ativo" if ativo == 1 else "Inativo")
                print("Inserido na Solidcon: ", "Não" if inseridoSolidcon == 0 else "Sim")

                pedidos.extend(ativo, pedido, inseridoSolidcon, vtex, solidcon)

            return pedidos

        elif len(itens) == 0:
            print("Nenhum pedido encontrado.")
            return None

    except Exception as e:
        print("Error: " + str(e))

def gravarPedidoSolidcon(pedidoPendente):
    try:
        if pedidoPendente is None:
            print ("Não existem dados a serem gravados na Solidcon.")
            return requests.codes['continue']

        else:
            pedido = pedidoPendente[1]
            cnpjFilial = pedidoPendente['solidcon']['cnpj']
            codEcom = pedidoPendente['solidcon']['CodEcom']

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

def atualizarPedidoBanco(pedidoPendente, respostaSolidcon):
    try:
        if pedidoPendente is None and respostaSolidcon == 100:
            print ("Não existem dados a serem atualizados no banco.")
            return requests.codes['continue']

        else:
            tabela = dynamodb.Table(TABELA)
            
            print("Atualizando pedido: ", pedidoPendente['pedido'], "...")

            tabela.update_item(
                Key={
                    'ativo': pedidoPendente['ativo'],
                    'pedido': pedidoPendente['pedido']
                },
                UpdateExpression='SET inseridoSolidcon = :inserido',
                ConditionExpression="inseridoSolidcon = :naoInserido",
                ExpressionAttributeValues={
                    ':inserido': '1',
                    ':naoInserido': '0'
                }
            )
        
            print("Pedido: ", pedidoPendente['pedido'], " atualizado.")

    except Exception as e:
        print("Error: " + str(e))