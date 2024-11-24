import streamlit as st
from src.database.conexao import executar_query, buscar_dados
import time

def mostrar_pagina():
    # Estilos CSS
    st.markdown("""
        <style>
        .custom-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.05);
            margin: 1rem 0;
            transition: all 0.3s ease;
        }
        .custom-card:hover {
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            transform: translateY(-2px);
        }
        .status-badge {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
            display: inline-block;
        }
        .status-ativo {
            background-color: #4CAF50;
            color: white;
        }
        .status-inativo {
            background-color: #FF6B6B;
            color: white;
        }
        .section-header {
            color: #2C3E50;
            font-weight: 600;
            margin-bottom: 1.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #eee;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("🏋️‍♂️ Modalidades")

    tab1, tab2 = st.tabs(["📋 Lista de Modalidades", "➕ Nova Modalidade"])

    with tab1:
        # Barra de pesquisa e filtros
        col1, col2 = st.columns([3,1])
        with col1:
            pesquisa = st.text_input("🔍", placeholder="Buscar modalidade...")
        with col2:
            status_filter = st.selectbox(
                "Status",
                ["Todas", "Ativas", "Inativas"],
                index=0
            )

        # Buscar modalidades
        query = """
            SELECT 
                codModalidade,
                nome,
                descricao,
                requisitos,
                status
            FROM MODALIDADE
            WHERE (nome LIKE %s OR descricao LIKE %s)
            AND (status = %s OR %s = 'Todas')
            ORDER BY nome
        """
        params = (
            f"%{pesquisa}%", 
            f"%{pesquisa}%",
            'A' if status_filter == "Ativas" else 'I',
            status_filter
        )
        modalidades = buscar_dados(query, params)

        if modalidades.empty:
            st.info("🔍 Nenhuma modalidade encontrada")
        else:
            for _, modalidade in modalidades.iterrows():
                with st.container():
                    st.markdown(f"""
                        <div class="custom-card">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <h3 style="margin: 0;">{modalidade['nome']}</h3>
                                </div>
                                <div>
                                    <span class="status-badge status-{'ativo' if modalidade['status'] == 'A' else 'inativo'}">
                                        {'Ativa' if modalidade['status'] == 'A' else 'Inativa'}
                                    </span>
                                </div>
                            </div>
                            <div style="margin-top: 1rem;">
                                <p><strong>Descrição:</strong> {modalidade['descricao'] or 'Não informada'}</p>
                                <p><strong>Requisitos:</strong> {modalidade['requisitos'] or 'Nenhum requisito específico'}</p>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✏️ Editar", key=f"edit_{modalidade['codModalidade']}"):
                            st.session_state['editing_modalidade'] = modalidade['codModalidade']
                            st.session_state['show_edit_form'] = True

                    with col2:
                        if st.button("🗑️ Excluir", key=f"del_{modalidade['codModalidade']}"):
                            st.session_state['deleting_modalidade'] = modalidade['codModalidade']
                            st.session_state['show_delete_confirm'] = True

        # Modal de Edição
        if 'show_edit_form' in st.session_state and st.session_state['show_edit_form']:
            modalidade_edit = buscar_dados(
                "SELECT * FROM MODALIDADE WHERE codModalidade = %s",
                (st.session_state['editing_modalidade'],)
            ).iloc[0]

            st.markdown("""
                <div class="custom-card">
                    <h3 style="color: #6C63FF;">✏️ Editar Modalidade</h3>
                </div>
            """, unsafe_allow_html=True)

            with st.form("edit_form"):
                nome = st.text_input("Nome", value=modalidade_edit['nome'])
                descricao = st.text_area("Descrição", value=modalidade_edit['descricao'])
                requisitos = st.text_area("Requisitos", value=modalidade_edit['requisitos'])
                status = st.selectbox(
                    "Status",
                    ["Ativa", "Inativa"],
                    index=0 if modalidade_edit['status'] == 'A' else 1
                )

                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("💾 Salvar", use_container_width=True):
                        if not nome:
                            st.error("Nome é obrigatório!")
                        else:
                            status_code = 'A' if status == "Ativa" else 'I'
                            executar_query("""
                                UPDATE MODALIDADE 
                                SET nome = %s, descricao = %s, requisitos = %s, status = %s
                                WHERE codModalidade = %s
                            """, (nome, descricao, requisitos, status_code, 
                                 st.session_state['editing_modalidade']))
                            
                            st.success("✅ Modalidade atualizada com sucesso!")
                            st.session_state['show_edit_form'] = False
                            st.rerun()

                with col2:
                    if st.form_submit_button("❌ Cancelar", use_container_width=True):
                        st.session_state['show_edit_form'] = False
                        st.rerun()

        # Modal de Confirmação de Exclusão
        if 'show_delete_confirm' in st.session_state and st.session_state['show_delete_confirm']:
            st.markdown("""
                <div class="custom-card" style="border: 2px solid #FF6B6B;">
                    <h3 style="color: #FF6B6B;">⚠️ Confirmar Exclusão</h3>
                    <p>Tem certeza que deseja excluir esta modalidade?</p>
                </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                if st.button("✔️ Sim, Excluir", use_container_width=True):
                    executar_query(
                        "DELETE FROM MODALIDADE WHERE codModalidade = %s",
                        (st.session_state['deleting_modalidade'],)
                    )
                    st.success("✅ Modalidade excluída com sucesso!")
                    st.session_state['show_delete_confirm'] = False
                    st.rerun()

            with col2:
                if st.button("❌ Não, Cancelar", use_container_width=True):
                    st.session_state['show_delete_confirm'] = False
                    st.rerun()

    with tab2:
        st.markdown("""
            <div class="custom-card">
                <h3 style="color: #6C63FF;">➕ Nova Modalidade</h3>
            </div>
        """, unsafe_allow_html=True)

        with st.form("nova_modalidade"):
            nome = st.text_input("Nome da Modalidade")
            descricao = st.text_area("Descrição")
            requisitos = st.text_area("Requisitos")

            if st.form_submit_button("✅ Cadastrar Modalidade", use_container_width=True):
                if not nome:
                    st.error("Nome é obrigatório!")
                else:
                    executar_query("""
                        INSERT INTO MODALIDADE (nome, descricao, requisitos, status)
                        VALUES (%s, %s, %s, 'A')
                    """, (nome, descricao, requisitos))
                    
                    st.success("✅ Modalidade cadastrada com sucesso!")
                    st.rerun()

if __name__ == "__main__":
    mostrar_pagina()