import streamlit as st
from src.database.conexao import executar_query, buscar_dados
from datetime import datetime

def mostrar_pagina():
    st.header("Avaliações Físicas")
    
    tab1, tab2 = st.tabs(["Visualizar Avaliações", "Nova Avaliação"])
    
    with tab1:
        avaliacoes_df = buscar_dados("""
            SELECT 
                a.nome as Aluno,
                DATE_FORMAT(av.data, '%d/%m/%Y') as Data,
                av.peso as Peso,
                av.altura as Altura,
                av.percentualGordura as 'Percentual de Gordura',
                p.nome as Professor,
                av.observacoes as Observações
            FROM AVALIACAO av
            JOIN ALUNO a ON av.CPF_aluno = a.CPF
            JOIN PROFESSOR p ON av.CPF_professor = p.CPF
            ORDER BY av.data DESC, a.nome
        """)
        
        if not avaliacoes_df.empty:
            st.dataframe(avaliacoes_df, hide_index=True)
    
    with tab2:
        with st.form("avaliacao_form"):
            alunos = buscar_dados("""
                SELECT CPF, nome 
                FROM ALUNO 
                WHERE status = 'A'
                ORDER BY nome
            """)
            
            professores = buscar_dados("""
                SELECT CPF, nome 
                FROM PROFESSOR 
                WHERE status = 'A'
                ORDER BY nome
            """)
            
            aluno = st.selectbox(
                "Selecione o Aluno",
                options=alunos['nome'].tolist() if not alunos.empty else []
            )
            
            professor = st.selectbox(
                "Selecione o Professor",
                options=professores['nome'].tolist() if not professores.empty else []
            )
            
            peso = st.number_input("Peso (kg)", min_value=0.0, max_value=300.0, step=0.1)
            altura = st.number_input("Altura (m)", min_value=0.0, max_value=3.0, step=0.01)
            gordura = st.number_input("Percentual de Gordura", min_value=0.0, max_value=100.0, step=0.1)
            observacoes = st.text_area("Observações")
            
            if st.form_submit_button("Registrar Avaliação"):
                if aluno and professor and peso > 0 and altura > 0:
                    aluno_cpf = str(alunos[alunos['nome'] == aluno]['CPF'].iloc[0])
                    professor_cpf = str(professores[professores['nome'] == professor]['CPF'].iloc[0])
                    
                    query = """
                    INSERT INTO AVALIACAO 
                    (CPF_aluno, CPF_professor, data, peso, altura, 
                     percentualGordura, observacoes)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    executar_query(
                        query, 
                        (aluno_cpf, professor_cpf, datetime.now().date(), 
                         peso, altura, gordura, observacoes)
                    )