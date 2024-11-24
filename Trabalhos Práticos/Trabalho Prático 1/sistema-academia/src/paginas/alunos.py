import streamlit as st
from src.database.conexao import executar_query, buscar_dados
from src.utils.helper import validar_cpf, validar_email, validar_telefone
import time

def mostrar_pagina():
    # Estilos CSS modernos e clean
    st.markdown("""
        <style>
        /* Cores e variáveis */
        :root {
            --primary-color: #6C63FF;
            --danger-color: #FF6B6B;
            --success-color: #4CAF50;
            --warning-color: #FFA726;
            --background-light: #F8F9FA;
        }

        /* Cards */
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

        /* Botões */
        .custom-button {
            padding: 8px 16px;
            border-radius: 8px;
            border: none;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
            margin: 0 5px;
        }
        .edit-button {
            background-color: var(--warning-color);
            color: white;
        }
        .delete-button {
            background-color: var(--danger-color);
            color: white;
        }
        
        /* Status Badge */
        .status-badge {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
            display: inline-block;
        }
        .status-ativo {
            background-color: var(--success-color);
            color: white;
        }
        .status-inativo {
            background-color: var(--danger-color);
            color: white;
        }

        /* Headers */
        .section-header {
            color: #2C3E50;
            font-weight: 600;
            margin-bottom: 1.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #eee;
        }

        /* Formulários */
        .stTextInput > div > div {
            border-radius: 8px;
        }
        .stTextInput input {
            font-size: 1rem;
            padding: 0.5rem;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
        }
        .stTabs [data-baseweb="tab"] {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
        
        /* Animações */
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        .animate-slide-in {
            animation: slideIn 0.3s ease forwards;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("🏋️ Sistema Academia")
    st.header("Gestão de Alunos")

    # Tabs com ícones e design moderno
    tabs = st.tabs(["📋 Lista de Alunos", "➕ Novo Aluno"])

    with tabs[0]:  # Lista de Alunos
        # Barra de pesquisa e filtros em layout clean
        col1, col2, col3 = st.columns([2,1,1])
        with col1:
            pesquisa = st.text_input("🔍", placeholder="Buscar por nome ou CPF...")
        with col2:
            status_filter = st.selectbox(
                "Status",
                ["Todos", "Ativos", "Inativos"],
                index=0
            )
        with col3:
            st.metric("Total de Alunos", 
                     buscar_dados("SELECT COUNT(*) as total FROM ALUNO WHERE status = 'A'").iloc[0]['total'])

        # Lista de alunos com design moderno
        alunos = buscar_dados("""
            SELECT 
                CPF,
                nome as Nome,
                email as Email,
                telefone as Telefone,
                status as Status
            FROM ALUNO
            WHERE (nome LIKE %s OR CPF LIKE %s)
            AND (status = %s OR %s = 'Todos')
            ORDER BY nome
        """, (f"%{pesquisa}%", f"%{pesquisa}%", 
              'A' if status_filter == "Ativos" else 'I', 
              status_filter))

        if alunos.empty:
            st.info("🔍 Nenhum aluno encontrado")
        else:
            for idx, aluno in alunos.iterrows():
                with st.container():
                    st.markdown(f"""
                        <div class="custom-card animate-slide-in" id="aluno-{aluno['CPF']}">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <h3 style="margin: 0;">{aluno['Nome']}</h3>
                                    <p style="color: #666; margin: 5px 0;">CPF: {aluno['CPF']}</p>
                                </div>
                                <div>
                                    <span class="status-badge status-{'ativo' if aluno['Status'] == 'A' else 'inativo'}">
                                        {'Ativo' if aluno['Status'] == 'A' else 'Inativo'}
                                    </span>
                                </div>
                            </div>
                            <div style="margin-top: 1rem;">
                                <p>📧 {aluno['Email'] or 'Não informado'}</p>
                                <p>📱 {aluno['Telefone'] or 'Não informado'}</p>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                
                col1, col2 = st.columns([1,1])
                with col1:
                    if st.button("✏️ Editar", key=f"edit_{aluno['CPF']}"):
                        st.session_state['editing_aluno'] = aluno['CPF']
                        st.session_state['show_edit_form'] = True
                        # Rolagem automática para o formulário de edição
                        st.markdown(f"""
                            <script>
                                document.getElementById('edit-form').scrollIntoView({{
                                    behavior: 'smooth'
                                }});
                            </script>
                        """, unsafe_allow_html=True)
                
                with col2:
                    if st.button("🗑️ Excluir", key=f"del_{aluno['CPF']}"):
                        st.session_state['deleting_aluno'] = aluno['CPF']
                        st.session_state['show_delete_confirm'] = True
                        # Rolagem automática para confirmação
                        st.markdown(f"""
                            <script>
                                document.getElementById('delete-confirm').scrollIntoView({{
                                    behavior: 'smooth'
                                }});
                            </script>
                        """, unsafe_allow_html=True)

    # Modal de Edição com novo design
    if 'show_edit_form' in st.session_state and st.session_state['show_edit_form']:
        st.markdown("""
            <div class="custom-card animate-slide-in" id="edit-form">
                <h3 style="color: var(--primary-color); margin-bottom: 1.5rem;">
                    ✏️ Editar Aluno
                </h3>
            </div>
        """, unsafe_allow_html=True)
        
        aluno_edit = buscar_dados(
            "SELECT * FROM ALUNO WHERE CPF = %s",
            (st.session_state['editing_aluno'],)
        ).iloc[0]
        
        with st.form("edit_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                nome = st.text_input("Nome", 
                                   value=aluno_edit['nome'],
                                   placeholder="Nome completo")
                email = st.text_input("Email", 
                                    value=aluno_edit['email'],
                                    placeholder="email@exemplo.com")
            
            with col2:
                telefone = st.text_input("Telefone", 
                                       value=aluno_edit['telefone'],
                                       placeholder="(11) 99999-9999")
                status = st.selectbox("Status",
                                    ["Ativo", "Inativo"],
                                    index=0 if aluno_edit['status'] == 'A' else 1)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([2,1,1])
            with col1:
                submit = st.form_submit_button("💾 Salvar Alterações", 
                                             use_container_width=True,
                                             type="primary")
            with col2:
                if st.form_submit_button("❌ Cancelar", 
                                       use_container_width=True):
                    st.session_state['show_edit_form'] = False
                    st.rerun()
            
            if submit:
                if not nome:
                    st.error("Nome é obrigatório!")
                elif email and not validar_email(email):
                    st.error("Email inválido!")
                elif telefone and not validar_telefone(telefone):
                    st.error("Telefone inválido!")
                else:
                    status_code = 'A' if status == "Ativo" else 'I'
                    executar_query("""
                        UPDATE ALUNO 
                        SET nome = %s, 
                            email = %s, 
                            telefone = %s, 
                            status = %s
                        WHERE CPF = %s
                    """, (nome, email, telefone, status_code, 
                          st.session_state['editing_aluno']))
                    
                    st.session_state['show_edit_form'] = False
                    st.success("✅ Aluno atualizado com sucesso!")
                    time.sleep(1)
                    st.rerun()

    # Modal de Confirmação de Exclusão com novo design
    if 'show_delete_confirm' in st.session_state and st.session_state['show_delete_confirm']:
        st.markdown("""
            <div class="custom-card animate-slide-in" id="delete-confirm" 
                 style="border: 2px solid var(--danger-color);">
                <h3 style="color: var(--danger-color);">
                    ⚠️ Confirmar Exclusão
                </h3>
                <p>Tem certeza que deseja excluir este aluno? Esta ação não pode ser desfeita.</p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✔️ Sim, Excluir",
                        type="primary",
                        use_container_width=True):
                executar_query(
                    "DELETE FROM ALUNO WHERE CPF = %s",
                    (st.session_state['deleting_aluno'],)
                )
                st.session_state['show_delete_confirm'] = False
                st.success("✅ Aluno excluído com sucesso!")
                time.sleep(1)
                st.rerun()
        
        with col2:
            if st.button("❌ Não, Cancelar",
                        use_container_width=True):
                st.session_state['show_delete_confirm'] = False
                st.rerun()

    # Formulário de Novo Aluno com novo design
    with tabs[1]:
        st.markdown("""
            <div class="custom-card">
                <h3 style="color: var(--primary-color);">
                    ➕ Cadastrar Novo Aluno
                </h3>
                <p style="color: #666;">
                    Preencha os dados do novo aluno abaixo
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("new_aluno_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                cpf = st.text_input("CPF (apenas números)", 
                                  max_chars=11,
                                  placeholder="12345678900")
                nome = st.text_input("Nome completo",
                                   placeholder="Nome do aluno")
            
            with col2:
                email = st.text_input("Email",
                                    placeholder="email@exemplo.com")
                telefone = st.text_input("Telefone",
                                       placeholder="11999999999")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col1, col2 = st.columns([2,1])
            with col1:
                submit = st.form_submit_button("✅ Cadastrar Aluno",
                                             use_container_width=True,
                                             type="primary")
            
            if submit:
                if not validar_cpf(cpf):
                    st.error("CPF inválido!")
                elif not nome:
                    st.error("Nome é obrigatório!")
                elif email and not validar_email(email):
                    st.error("Email inválido!")
                elif telefone and not validar_telefone(telefone):
                    st.error("Telefone inválido!")
                else:
                    try:
                        executar_query("""
                            INSERT INTO ALUNO (CPF, nome, email, telefone, status)
                            VALUES (%s, %s, %s, %s, 'A')
                        """, (cpf, nome, email, telefone))
                        
                        st.success("✅ Aluno cadastrado com sucesso!")
                        time.sleep(1)
                        st.rerun()
                    except Exception as e:
                        if "Duplicate entry" in str(e):
                            st.error("CPF já cadastrado!")
                        else:
                            st.error(f"Erro ao cadastrar: {str(e)}")

if __name__ == "__main__":
    mostrar_pagina()