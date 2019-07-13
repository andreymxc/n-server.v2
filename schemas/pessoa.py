# -*- coding: utf-8 -*-
## ----------------------------------------------------------
## Definição do schema de validação do Json a ser recebido pela requisição HTTP
## ----------------------------------------------------------
schemaCadastro = {
    "title": "Pessoa",
    "type": "object",
    "required": ["nome_completo", "cpf", "data_nasc", "genero", "email", "senha"],
    "properties": {
        "nome_completo": {
            "type": "string", "pattern": "^[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ ]+$"
        },
        "cpf": {
            "type": "string", "minLength": 11, "maxLength": 11
        },
        "rg:": {
            "type": "object",
            "properties": {
                "emissor":{
                    "type": "string", "minLength": 3, "maxLength": 3
                },
                "numero": {
                    "type": "string", "maxLength": 14
                }
            }
        },
        "data_nasc": {
            "type": "string", "format": "date-time"
        },
        "genero": {
            "type": "string", "pattern": "^[M|F|D]$"
        },
        "email": {
            "type": "string", "format": "email"
        },
        "senha": {
            "type": "string", "minLength": 8 #Adicionar criptografia
        }
    }
}