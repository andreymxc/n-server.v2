# -*- coding: utf-8 -*-
## ----------------------------------------------------------
## Importa��o dos m�dulos padr�es
## ----------------------------------------------------------
from flask_json_schema import JsonSchema, JsonValidationError
from flask import Flask, Blueprint, request, jsonify
from bson.objectid import ObjectId
from datetime import datetime, timedelta


import pymongo
import dns

## ----------------------------------------------------------
## Importa��o do orquestrador da conex�o com BD
## ----------------------------------------------------------
from orquestrador.orquestrador import Orquestrador 
## ----------------------------------------------------------
## Importa��o dos Objetos de tratamento de erros
## ----------------------------------------------------------
from biblioteca_respostas.status_internos import StatusInternos
from biblioteca_respostas.respostas_api import RespostasAPI
## ----------------------------------------------------------
## Importa��o dos schemas referentes a Externos
## ----------------------------------------------------------

orq = Orquestrador()

## ----------------------------------------------------------
## Defini��o do Blueprint
## ----------------------------------------------------------
blueprint_externos = Blueprint("Externos",__name__)

## ----------------------------------------------------------
## Defini��o do Subapp e Schema
## ----------------------------------------------------------
app = Flask("Externos")
schema = JsonSchema(app)

## ----------------------------------------------------------
## Rotas dos servi�os para o APP
## ----------------------------------------------------------
##
## @pessoa_blue.route: A rota do endpoint
## @schema.validate: O schema a ser validado durante a requisi��o
## ----------------------------------------------------------


@blueprint_externos.route("/gera_token", methods=['POST'])
def Gerar_Token():
      try:  
            token_request = request.json  
            segredo = token_request['segredo']
            retorno = orq.verificar_id_projeto_externos(segredo)
            if retorno :
                id_projeto = token_request['segredo']
                token = orq.gera_hash(id_projeto)
                vencimento = datetime.now() + timedelta(minutes=5)      
                orq.armazenar_tokens(id_projeto, token, vencimento)
                return RespostasAPI('Consulta realizada com sucesso',
                                    {
                                        'token': str(token),                                        
                                    }
                                    ).JSON 
            else:
                raise StatusInternos('SI-21', {'projeto': projeto})
      except StatusInternos as e:
            return e.errors
      try:
          orq.verifica_token(token)
      except StatusInternos as e:
            return e.errors




