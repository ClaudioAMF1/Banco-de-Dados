import streamlit as st
import mysql.connector
import hashlib
from src.database.conexao import executar_query, buscar_dados

def criar_tabela_usuarios():
    query = """
    CREATE TABLE IF NOT EXISTS USUARIO (
        id INT AUTO_INCREMENT,
        username VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        nivel VARCHAR(20) NOT NULL,
        status CHAR(1) DEFAULT 'A',
        PRIMARY KEY (id)
    )
    """
    executar_query(query)

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def login():
    st.title("Login")
    
    with st.form("login_form"):
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        submitted = st.form_submit_button("Entrar")
        
        if submitted:
            query = """
            SELECT id, username, nivel 
            FROM USUARIO 
            WHERE username = %s AND password = %s AND status = 'A'
            """
            users_df = buscar_dados(query, (username, hash_senha(password)))
            
            if not users_df.empty:
                st.session_state['authenticated'] = True
                st.session_state['user'] = {
                    'id': users_df['id'].iloc[0],
                    'username': users_df['username'].iloc[0],
                    'nivel': users_df['nivel'].iloc[0]
                }
                st.success("Login realizado com sucesso!")
                st.rerun()
            else:
                st.error("Usuário ou senha inválidos")

def check_auth():
    return st.session_state.get('authenticated', False)

def logout():
    if st.sidebar.button("Sair"):
        st.session_state['authenticated'] = False
        st.session_state['user'] = None
        st.rerun()