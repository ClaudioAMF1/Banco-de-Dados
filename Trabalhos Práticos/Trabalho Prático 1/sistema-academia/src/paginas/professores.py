import streamlit as st
from src.database.conexao import executar_query, buscar_dados
from src.utils.helper import validar_cpf, validar_telefone
import locale

# Configurar formatação de moeda para Real brasileiro
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def formatar_moeda(valor):
    return locale.currency(valor, grouping=True)

def mostrar_pagina():
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
        .status-ativo { background-color: #4CAF50; color: white; }
        .status-inativo { background-color: #FF6B6B; color: white; }
        .professor-info {
            display: flex;
            gap: 1rem;
            align-items: center;
        }
        .professor-avatar {
            width: 64px;
            height: 64px;
            border-radius: 50%;
            background: #6C63FF;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.5rem;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("👨‍🏫 Professores")

    tab1, tab2 = st.tabs(["📋 Lista de Professores", "➕ Novo Professor"])

    with tab1:
        col1, col2, col3 = st.columns([2,1,1])
        with col1:
            pesquisa = st.text_input("🔍", placeholder="Buscar professor...")
        with col2:
            status_filter = st.selectbox(
                "Status",
                ["Todos", "Ativos", "Inativos"]
            )
        with col3:
            ordenar_por = st.selectbox(
                "Ordenar por",
                ["Nome", "Salário"]
            )

        query = """
            SELECT 
                CPF,
                nome,
                telefone,
                especializacao,
                salario,
                status
            FROM PROFESSOR
            WHERE (nome LIKE %s OR CPF LIKE %s)
            AND (status = %s OR %s = 'Todos')
            ORDER BY {} {}
        """.format(
            'nome' if ordenar_por == "Nome" else 'salario',
            'ASC' if ordenar_por == "Nome" else 'DESC'
        )

        params = (
            f"%{pesquisa}%",
            f"%{pesquisa}%",
            'A' if status_filter == "Ativos" else 'I',
            status_filter
        )

        professores = buscar_dados(query, params)

        if professores.empty:
            st.info("🔍 Nenhum professor encontrado")
        else:
            for _, professor in professores.iterrows():
                with st.container():
                    st.markdown(f"""
                        <div class="custom-card">
                            <div class="professor-info">
                                <div class="professor-avatar">
                                    {professor['nome'][0].upper()}
                                </div>
                                <div style="flex-grow: 1;">
                                    <h3 style="margin: 0;">{professor['nome']}</h3>
                                    <p style="margin: 0; color: #666;">
                                        {professor['especializacao'] or 'Especialização não informada'}
                                    </p>
                                </div>
                                <div>
                                    <span class="status-badge status-{'ativo' if professor['status'] == 'A' else 'inativo'}">
                                        {'Ativo' if professor['status'] == 'A' else 'Inativo'}
                                    </span>
                                </div>
                            </div>
                            <div style="margin-top: 1rem;">
                                <p>📞 {professor['telefone'] or 'Não informado'}</p>
                                <p>💰 {formatar_moeda(professor['salario'])}</p>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✏️ Editar", key=f"edit_{professor['CPF']}"):
                            st.session_state['editing_professor'] = professor['CPF']
                            st.session_state['show_edit_form'] = True

                    with col2:
                        if st.button("🗑️ Excluir", key=f"del_{professor['CPF']}"):
                            st.session_state['deleting_professor'] = professor['CPF']
                            st.session_state['show_delete_confirm'] = True

        # Modal de Edição
        if 'show_edit_form' in st.session_state and st.session_state['show_edit_form']:
            professor_edit = buscar_dados(
                "SELECT * FROM PROFESSOR WHERE CPF = %s",
                (st.session_state['editing_professor'],)
            ).iloc[0]

            st.markdown("""
                <div class="custom-card">
                    <h3 style="color: #6C63FF;">✏️ Editar Professor</h3>
                </div>
            """, unsafe_allow_html=True)

            with st.form("edit_form"):
                col1, col2 = st.columns(2)
                with col1:
                    nome = st.text_input("Nome", value=professor_edit['nome'])
                    telefone = st.text_input("Telefone", value=professor_edit['telefone'])
                with col2:
                    especializacao = st.text_input("Especialização", value=professor_edit['especializacao'])
                    salario = st.number_input("Salário", 
                                            min_value=0.0,
                                            value=float(professor_edit['salario']))
                
                status = st.selectbox(
                    "Status",
                    ["Ativo", "Inativo"],
                    index=0 if professor_edit['status'] == 'A' else 1
                )

                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("💾 Salvar", use_container_width=True):
                        if not nome:
                            st.error("Nome é obrigatório!")
                        elif telefone and not validar_telefone(telefone):
                            st.error("Telefone inválido!")
                        elif salario <= 0:
                            st.error("Salário deve ser maior que zero!")
                        else:
                            status_code = 'A' if status == "Ativo" else 'I'
                            executar_query("""
                                UPDATE PROFESSOR 
                                SET nome = %s, telefone = %s, 
                                    especializacao = %s, salario = %s, 
                                    status = %s
                                WHERE CPF = %s
                            """, (nome, telefone, especializacao, salario, 
                                 status_code, st.session_state['editing_professor']))
                            
                            st.success("✅ Professor atualizado com sucesso!")
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
                    <p>Tem certeza que deseja excluir este professor?</p>
                </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                if st.button("✔️ Sim, Excluir", use_container_width=True):
                    executar_query(
                        "DELETE FROM PROFESSOR WHERE CPF = %s",
                        (st.session_state['deleting_professor'],)
                    )
                    st.success("✅ Professor excluído com sucesso!")
                    st.session_state['show_delete_confirm'] = False
                    st.rerun()

            with col2:
                if st.button("❌ Não, Cancelar", use_container_width=True):
                    st.session_state['show_delete_confirm'] = False
                    st.rerun()

    with tab2:
        st.markdown("""
            <div class="custom-card">
                <h3 style="color: #6C63FF;">➕ Novo Professor</h3>
            </div>
        """, unsafe_allow_html=True)

        with st.form("novo_professor"):
            col1, col2 = st.columns(2)
            with col1:
                cpf = st.text_input("CPF (apenas números)", max_chars=11)
                nome = st.text_input("Nome completo")
                telefone = st.text_input("Telefone")
            with col2:
                especializacao = st.text_input("Especialização")
                salario = st.number_input("Salário", min_value=0.0, step=100.0)

            if st.form_submit_button("✅ Cadastrar Professor", use_container_width=True):
                if not validar_cpf(cpf):
                    st.error("CPF inválido!")
                elif not nome:
                    st.error("Nome é obrigatório!")
                elif telefone and not validar_telefone(telefone):
                    st.error("Telefone inválido!")
                elif salario <= 0:
                    st.error("Salário deve ser maior que zero!")
                else:
                    try:
                        executar_query("""
                            INSERT INTO PROFESSOR 
                            (CPF, nome, telefone, especializacao, salario, status)
                            VALUES (%s, %s, %s, %s, %s, 'A')
                        """, (cpf, nome, telefone, especializacao, salario))
                        
                        st.success("✅ Professor cadastrado com sucesso!")
                        st.rerun()
                    except Exception as e:
                        if "Duplicate entry" in str(e):
                            st.error("CPF já cadastrado!")
                        else:
                            st.error(f"Erro ao cadastrar: {str(e)}")

if __name__ == "__main__":
    mostrar_pagina()