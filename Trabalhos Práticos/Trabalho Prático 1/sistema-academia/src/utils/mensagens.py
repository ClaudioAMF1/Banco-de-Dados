import streamlit as st

class Mensagens:
    @staticmethod
    def erro_conflito_horario():
        st.error("Existe conflito de horário com outra aula!")

    @staticmethod
    def erro_capacidade():
        st.error("A turma está com capacidade máxima!")

    @staticmethod
    def erro_matricula():
        st.error("O aluno não possui matrícula ativa!")

    @staticmethod
    def erro_pagamento():
        st.error("Existe pagamento pendente!")

    @staticmethod
    def sucesso_cadastro():
        st.success("Cadastro realizado com sucesso!")

    @staticmethod
    def sucesso_atualizacao():
        st.success("Atualização realizada com sucesso!")

    @staticmethod
    def confirmar_acao(mensagem):
        return st.warning(f"{mensagem}\n\nTem certeza que deseja continuar?")

    @staticmethod
    def erro_conexao():
        st.error("Erro de conexão com o banco de dados. Tente novamente mais tarde.")

    @staticmethod
    def erro_dados_invalidos():
        st.error("Dados inválidos. Verifique as informações e tente novamente.")

    @staticmethod
    def erro_permissao():
        st.error("Você não tem permissão para realizar esta ação.")