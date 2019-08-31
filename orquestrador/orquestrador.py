# -*- coding: utf-8 -*-
import json
from flask import jsonify
from pymongo import MongoClient  # Para acessar o MongoDB
from bson.objectid import ObjectId
import urllib.parse  # (OPCIONAL) Para criar texto de URI

from biblioteca_respostas.status_internos import StatusInternos


class Orquestrador(object):
    def __init__(self):
        print("\n[Orquestrador] instanciado com sucesso!\n")

        # Carregando com paramêtros de acesso para desenvolvedor
        usuario_banco = urllib.parse.quote_plus('dev_connect')
        senha_banco = urllib.parse.quote_plus('rgPuzhTgc8HAHFlV')

        # Criando conexão com o MongoDB
        conexao_servidor = MongoClient(
            'mongodb+srv://%s:%s@cluster0-hygoa.gcp.mongodb.net/?retryWrites=true' % (usuario_banco, senha_banco))

        # Instanciando um gerenciador do banco de dados TCC
        self.conexao_bd = conexao_servidor.TCC

    # ----------------------------------------------------------------------
    # Orquestrador: Pessoa
    # ----------------------------------------------------------------------
    def cadastrar_pessoa(self, pessoa):
        if self.verificar_cpf(pessoa["cpf"]):
            raise StatusInternos('SI-1', {'cpf': str(pessoa["cpf"])})
        if self.verificar_email(pessoa["email"]):
            raise StatusInternos('SI-2', {'email': str(pessoa["email"])})

        try:
            colecao_pessoas = self.conexao_bd.Pessoas
        except:
            raise StatusInternos('SI-4')

        try:
            # Chamada de função para inserir documento de cadastro
            pessoa_id = colecao_pessoas.insert_one(pessoa)

            # Chama função de cadastro do Blockchain
            print("\n[Orquestrador] pessoa cadastrada com sucesso!\n")
            print("id:" + str(pessoa_id.inserted_id))

            return(str(pessoa_id.inserted_id))
        except:
            raise StatusInternos('SI-3', {'pessoa': pessoa})
    
    def adicionar_dados_pessoa(self, segredo, dados_novos):
        try:
            if(self.conexao_bd.Pessoas.find({"_id": ObjectId(segredo)}).limit(1).count() > 0):

                print("\n[Orquestrador] Dados novos:\n" + str(dados_novos))

                try:
                    self.conexao_bd.Pessoas.update(
                        {"_id": ObjectId(segredo)}, {"$set":  dados_novos})
                        
                except Exception as e:
                    print(e)
                    raise Exception(StatusInternos(
                        "SI-8", {"colecao": "Pessoas", "momento": "adicionar dados novos", "dados novos": dados_novos, "segredo": segredo}))

            else:
                raise Exception(StatusInternos(
                    "SI-8", {"colecao": "Pessoas", "momento": "adicionar dados novos", "dados novos": dados_novos, "segredo": segredo}))

        except Exception as e:
            print(e)
            raise Exception(StatusInternos(
                "SI-4", {"colecao": "Pessoas", "momento": "adicionar dados novos", "dados novos": dados_novos}))

    def editar_dados_pessoa(self, segredo, dados):

        try:
            if(self.conexao_bd.Pessoas.find({"_id": ObjectId(segredo)}).limit(1).count() > 0):

                print("\n[Orquestrador] Dados novos:\n" + str(dados))

                try:
                    self.conexao_bd.Pessoas.update(
                        {"_id": ObjectId(segredo)}, {"$set":  dados})

                except Exception as e:
                    print(e)
                    raise Exception(StatusInternos(
                        "SI-8", {"colecao": "Pessoas", "momento": "editar dados novos", "dados novos": dados, "segredo": segredo}))

            else:
                raise Exception(StatusInternos(
                    "SI-8", {"colecao": "Pessoas", "momento": "editar dados novos", "dados novos": dados, "segredo": segredo}))

        except Exception as e:
            print(e)
            raise Exception(StatusInternos(
                "SI-4", {"colecao": "Pessoas", "momento": "editar dados novos", "dados novos": dados}))

    def excluir_pessoa(self, pessoa_id_usuario):
            # simulando retorno OK
        return True
    
    
    
    def excluir_dados_pessoa(self, segredo, dados):
        
        try:
            if (self.conexao_bd.Pessoas.find({"_id": ObjectId(segredo)}).limit(1).count() > 0):

                print("\n[Orquestrador] Exclusão de dados:\n" + str(dados))

                try:
                    self.conexao_bd.Pessoas.update(
                    {"_id": ObjectId(segredo)}, {"$unset": dados}), False, True

                except Exception as e:
                    print(e)
                    raise Exception(StatusInternos(
                    "SI-8", {"colecao": "Pessoas", "momento": "Excluir dados", "dados excluídos": dados,
                         "segredo": segredo}))

            else:
                raise Exception(StatusInternos(
                "SI-8", {"colecao": "Pessoas", "momento": "Excluir dados", "dados excluídos": dados,
                     "segredo": segredo}))

        except Exception as e:
            print(e)
            raise Exception(StatusInternos(
                "SI-4", {"colecao": "Pessoas", "momento": "Excluir dados", "dados excluídos": dados}))
            
            
    

    def login_pessoa(self, valor_login, senha, tipo):
        # Login por cpf
        if(tipo == '0'):
            metodo_login = "cpf"
        # Login por e-mail
        elif(tipo == '1'):
            metodo_login = "email"
        # Login com identificador errado
        else:
            print("[Orquestrador.ERRO] Método de login não foi identificado.")
            raise StatusInternos(
                'SI-7', {"metodo_login": tipo, metodo_login: valor_login, 'senha': senha})

        try:
            if(self.conexao_bd.Pessoas.find({"$and": [{metodo_login: valor_login}, {"senha": senha}]}).limit(1).count() > 0):
                print("[Orquestrador] " + metodo_login + ": '" + valor_login +
                      "' encontrado na coleção de Pessoas, exibindo documento retornado:")

                dados_pessoa = self.conexao_bd.Pessoas.find(
                    {"$and": [{metodo_login: valor_login}, {"senha": senha}]})

                print(str({
                    "segredo": str(dados_pessoa[0]['_id']),
                    "usuario_nome": str(dados_pessoa[0]['nome_completo'])
                }))

                return {
                    'segredo': str(dados_pessoa[0]['_id']),
                    'nome_usuario': str(dados_pessoa[0]['nome_completo'])
                }

            else:
                print("[Orquestrador] " + metodo_login + ": '" +
                      valor_login + "' não encontrado na coleção de Pessoas.")
                raise StatusInternos
        except Exception as e:
            print(e)
            raise StatusInternos('SI-6')

    def verificar_id_usuario(self, pessoa_id_usuario):
        try:
            if(self.conexao_bd.Pessoas.find({"_id": ObjectId(pessoa_id_usuario)},{"_id":0}).limit(1).count() > 0):
                print("[Orquestrador] id pessoa '" + str(pessoa_id_usuario) +
                      "' encontrado na coleção de Pessoas, exibindo documento retornado:\n")

                dados_pessoa = self.conexao_bd.Pessoas.find(
                    {"_id": ObjectId(pessoa_id_usuario)})

                print(str(dados_pessoa[0]))

                return dados_pessoa[0]
            else:
                print("[Orquestrador] id pessoa '" + str(pessoa_id_usuario) +
                      "' não encontrado na coleção de Pessoas\n")

                return None
        except Exception as e:
            print("[Orquestrador.ERRO] erro durante a execução do comando de seleção")
            raise(e)

        # raise Exception(CodigoStatusHttp(500).retorno())

    def verificar_cpf(self, pessoa_cpf):
        if(self.conexao_bd.Pessoas.find({"cpf": pessoa_cpf}).limit(1).count() > 0):
            return True
        else:
            return False

    def verificar_email(self, pessoa_email):
        if(self.conexao_bd.Pessoas.find({"email": pessoa_email}).limit(1).count() > 0):
            return True
        else:
            return False
    
    def verificar_metodo_login_existente(self, pessoa_cpf, pessoa_email):
        if(self.conexao_bd.Pessoas.find({"$or": [{"cpf": pessoa_cpf}, {"email": pessoa_email}]}).limit(1).count() > 0):
            return True
        else:
            return False

    # ----------------------------------------------------------------------
    # Orquestrador: Empresa
    # ----------------------------------------------------------------------
    def cadastrar_empresa(self, empresa):
        if self.verificar_cnpj(empresa["cnpj"]):
            raise StatusInternos("SI-9", {'cnpj': str(empresa["cnpj"])})
        else:
            try:
                colecao_empresas = self.conexao_bd.Empresas
            except:
                raise StatusInternos('SI-4')

            try:
                empresa_id = colecao_empresas.insert_one(empresa)

                print("\n[Orquestrador] empresa cadastrada com sucesso!\n")
                print("id:" + str(empresa_id.inserted_id))

                return(str(empresa_id.inserted_id))

            except:
                raise StatusInternos('SI-10', {'empresa': empresa})

    def verificar_id_empresa(self, empresa_id_usuario):
        try:
            if(self.conexao_bd.Empresas.find({"_id": ObjectId(empresa_id_usuario)}).limit(1).count() > 0):
                print("[Orquestrador] id empresa '" + str(empresa_id_usuario) +
                      "' encontrado na coleção de Pessoas, exibindo documento retornado:\n")

                dados_empresa = self.conexao_bd.Empresas.find(
                    {"_id": ObjectId(empresa_id_usuario)})

                print(str(dados_empresa[0]))
                return dados_empresa[0]
            else:
                print("[Orquestrador] id empresa '" + str(empresa_id_usuario) +
                      "' não encontrado na coleção de Empresas\n")

                return None
        except Exception as e:
            print("[Orquestrador.ERRO] erro durante a execução do comando de seleção")
            raise(e)

    def verificar_cnpj(self, empresa_cnpj):
        if(self.conexao_bd.Empresas.find({"cnpj": empresa_cnpj}).limit(1).count() > 0):
            return True
        else:
            return False

    def verificar_empresa(self, id_empresa):
        if(self.conexao_bd.Empresas.find({"_id": ObjectId(id_empresa)}).limit(1).count() > 0):
            print('empresa encontrado!!')
            return True
        else:
            return False

    # ----------------------------------------------------------------------
    # Orquestrador: Projeto
    # ----------------------------------------------------------------------        
    def cadastrar_projeto(self, projeto):
        
        if self.verificar_empresa(projeto["id_empresa"]):
            try:
                colecao_projetos = self.conexao_bd.Projetos
            except:
                raise StatusInternos('SI-4')

            try:
                projeto_id = colecao_projetos.insert_one(projeto)
                
                print("\n[Orquestrador] projeto cadastrado com sucesso!\n")
                print("id:" + str(projeto_id.inserted_id))

                return(str(projeto_id.inserted_id))
            
            except:
                raise StatusInternos('SI-12', {'projeto': projeto})
        
        else:
            print("[Orquestrador] empresa não cadastrada na coleção Empresas")
            raise StatusInternos('SI-13')

    def verificar_id_projeto(self, id_projeto):
        try:
            if(self.conexao_bd.Projetos.find({"_id": ObjectId(id_projeto)}).limit(1).count() > 0):
            
                print("[Orquestrador] id projeto '" + str(id_projeto) + "' encontrado na coleção de Projetos, exibindo documento retornado:\n")
            
                dados_projeto = self.conexao_bd.Projetos.find({ "_id": ObjectId(id_projeto)})
            
                print(str(dados_projeto[0]))
                return dados_projeto[0]

            else:
                print("[Orquestrador] id projeto '" + str(id_projeto) + "' não encontrado na coleção de ProjetoPessoa\n")
                
            return None
        
        except Exception as e:
            print("[Orquestrador.ERRO] erro durante a execução do comando de seleção")
            raise(e)
    
