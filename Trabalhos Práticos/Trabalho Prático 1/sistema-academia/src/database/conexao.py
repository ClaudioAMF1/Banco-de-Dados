import mysql.connector
import streamlit as st
import pandas as pd

DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'Claudio1472',
    'database': 'academia',
    'port': 3306
}

def iniciar_conexao():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Exception as e:
        return None

def executar_query(query, params=()):
    conn = iniciar_conexao()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            st.error(f"Erro ao executar query: {str(e)}")
            return None
        finally:
            cursor.close()
            conn.close()

def buscar_dados(query, params=()):
    conn = iniciar_conexao()
    if conn:
        try:
            return pd.read_sql(query, conn, params=params)
        except Exception as e:
            st.error(f"Erro ao buscar dados: {str(e)}")
            return pd.DataFrame()
        finally:
            if conn.is_connected():
                conn.close()
    return pd.DataFrame()