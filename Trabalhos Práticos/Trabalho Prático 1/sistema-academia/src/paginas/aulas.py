import streamlit as st
from src.database.conexao import executar_query, buscar_dados
from datetime import datetime, timedelta

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
        .turma-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .capacity-badge {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
        }
        .capacity-ok { background-color: #4CAF50; color: white; }
        .capacity-warning { background-color: #FFA726; color: white; }
        .capacity-full { background-color: #FF6B6B; color: white; }
        .dia-semana-tag {
            background: #6C63FF;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.85rem;
            margin-right: 8px;
        }
        .professor-tag {
            background: #F1F3F4;
            color: #444;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.85rem;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("📅 Turmas e Aulas")

    tab1, tab2 = st.tabs(["📋 Turmas", "➕ Nova Turma"])

    with tab1:
        # Filtros
        col1, col2, col3 = st.columns(3)
        with col1:
            modalidade_filter = st.selectbox(
                "Modalidade",
                ["Todas"] + buscar_dados(
                    "SELECT nome FROM MODALIDADE WHERE status = 'A'"
                )['nome'].tolist()
            )
        with col2:
            dia_filter = st.selectbox(
                "Dia da Semana",
                ["Todos", "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]
            )
        with col3:
            professor_filter = st.selectbox(
                "Professor",
                ["Todos"] + buscar_dados(
                    "SELECT nome FROM PROFESSOR WHERE status = 'A'"
                )['nome'].tolist()
            )

        # Query de turmas
        query = """
            SELECT 
                t.codTurma,
                m.nome as modalidade,
                t.diaSemana,
                TIME_FORMAT(t.horario, '%H:%i') as horario,
                p.nome as professor,
                t.capacidade,
                COUNT(at.codAluno_Turma) as alunos_inscritos
            FROM TURMA t
            JOIN MODALIDADE m ON t.codModalidade = m.codModalidade
            JOIN PROFESSOR p ON t.CPF_professor = p.CPF
            LEFT JOIN ALUNO_TURMA at ON t.codTurma = at.codTurma AND at.status = 'A'
            WHERE t.status = 'A'
            AND (%s = 'Todas' OR m.nome = %s)
            AND (%s = 'Todos' OR t.diaSemana = %s)
            AND (%s = 'Todos' OR p.nome = %s)
            GROUP BY t.codTurma
            ORDER BY FIELD(t.diaSemana, 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado'),
                     t.horario
        """
        params = (
            modalidade_filter, modalidade_filter,
            dia_filter, dia_filter,
            professor_filter, professor_filter
        )

        turmas = buscar_dados(query, params)

        if turmas.empty:
            st.info("🔍 Nenhuma turma encontrada")
        else:
            for _, turma in turmas.iterrows():
                with st.container():
                    ocupacao = (turma['alunos_inscritos'] / turma['capacidade']) * 100
                    if ocupacao < 70:
                        capacity_class = "capacity-ok"
                        capacity_text = "Vagas disponíveis"
                    elif ocupacao < 90:
                        capacity_class = "capacity-warning"
                        capacity_text = "Poucas vagas"
                    else:
                        capacity_class = "capacity-full"
                        capacity_text = "Turma cheia"

                    st.markdown(f"""
                        <div class="custom-card">
                            <div class="turma-header">
                                <h3 style="margin: 0;">{turma['modalidade']}</h3>
                                <span class="capacity-badge {capacity_class}">
                                    {turma['alunos_inscritos']}/{turma['capacidade']} • {capacity_text}
                                </span>
                            </div>
                            <div style="margin: 1rem 0;">
                                <span class="dia-semana-tag">{turma['diaSemana']} {turma['horario']}</span>
                                <span class="professor-tag">Prof. {turma['professor']}</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("✏️ Editar", key=f"edit_{turma['codTurma']}"):
                            st.session_state['editing_turma'] = turma['codTurma']
                            st.session_state['show_edit_form'] = True
                    
                    with col2:
                        if st.button("👥 Alunos", key=f"alunos_{turma['codTurma']}"):
                            st.session_state['viewing_alunos'] = turma['codTurma']
                            st.session_state['show_alunos'] = True

                    with col3:
                        if st.button("🗑️ Excluir", key=f"del_{turma['codTurma']}"):
                            st.session_state['deleting_turma'] = turma['codTurma']
                            st.session_state['show_delete_confirm'] = True

        # Modal de Visualização de Alunos
        if 'show_alunos' in st.session_state and st.session_state['show_alunos']:
            alunos_turma = buscar_dados("""
                SELECT 
                    a.nome,
                    a.telefone,
                    DATE_FORMAT(at.dataInscricao, '%d/%m/%Y') as data_inscricao
                FROM ALUNO_TURMA at
                JOIN ALUNO a ON at.CPF_aluno = a.CPF
                WHERE at.codTurma = %s AND at.status = 'A'
                ORDER BY a.nome
            """, (st.session_state['viewing_alunos'],))

            st.markdown("""
                <div class="custom-card">
                    <h3>👥 Alunos da Turma</h3>
                </div>
            """, unsafe_allow_html=True)

            if alunos_turma.empty:
                st.info("Nenhum aluno inscrito nesta turma")
            else:
                st.dataframe(alunos_turma, hide_index=True)

            if st.button("Fechar"):
                st.session_state['show_alunos'] = False
                st.rerun()

        # Modal de Edição
        if 'show_edit_form' in st.session_state and st.session_state['show_edit_form']:
            turma_edit = buscar_dados("""
                SELECT t.*, m.nome as modalidade, p.nome as professor
                FROM TURMA t
                JOIN MODALIDADE m ON t.codModalidade = m.codModalidade
                JOIN PROFESSOR p ON t.CPF_professor = p.CPF
                WHERE t.codTurma = %s
            """, (st.session_state['editing_turma'],)).iloc[0]

            st.markdown("""
                <div class="custom-card">
                    <h3 style="color: #6C63FF;">✏️ Editar Turma</h3>
                </div>
            """, unsafe_allow_html=True)

            with st.form("edit_turma"):
                modalidades = buscar_dados(
                    "SELECT codModalidade, nome FROM MODALIDADE WHERE status = 'A'"
                )
                professores = buscar_dados(
                    "SELECT CPF, nome FROM PROFESSOR WHERE status = 'A'"
                )

                col1, col2 = st.columns(2)
                with col1:
                    modalidade = st.selectbox(
                        "Modalidade",
                        options=modalidades['nome'].tolist(),
                        index=modalidades[modalidades['nome'] == turma_edit['modalidade']].index[0]
                    )
                    horario = st.time_input("Horário", value=datetime.strptime(turma_edit['horario'], '%H:%M').time())
                
                with col2:
                    professor = st.selectbox(
                        "Professor",
                        options=professores['nome'].tolist(),
                        index=professores[professores['nome'] == turma_edit['professor']].index[0]
                    )
                    dia_semana = st.selectbox(
                        "Dia da Semana",
                        options=["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"],
                        index=["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"].index(turma_edit['diaSemana'])
                    )

                capacidade = st.number_input(
                    "Capacidade",
                    min_value=1,
                    value=int(turma_edit['capacidade'])
                )

                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("💾 Salvar", use_container_width=True):
                        modalidade_id = modalidades[modalidades['nome'] == modalidade]['codModalidade'].iloc[0]
                        professor_cpf = professores[professores['nome'] == professor]['CPF'].iloc[0]

                        executar_query("""
                            UPDATE TURMA 
                            SET codModalidade = %s,
                                CPF_professor = %s,
                                horario = %s,
                                diaSemana = %s,
                                capacidade = %s
                            WHERE codTurma = %s
                        """, (modalidade_id, professor_cpf, horario, dia_semana, 
                              capacidade, st.session_state['editing_turma']))
                        
                        st.success("✅ Turma atualizada com sucesso!")
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
                    <p>Tem certeza que deseja excluir esta turma?</p>
                    <p style="color: #666;">Todos os alunos serão desvinculados da turma.</p>
                </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                if st.button("✔️ Sim, Excluir", use_container_width=True):
                    # Primeiro desvincula os alunos
                    executar_query(
                        "UPDATE ALUNO_TURMA SET status = 'I' WHERE codTurma = %s",
                        (st.session_state['deleting_turma'],)
                    )
                    # Depois inativa a turma
                    executar_query(
                        "UPDATE TURMA SET status = 'I' WHERE codTurma = %s",
                        (st.session_state['deleting_turma'],)
                    )
                    
                    st.success("✅ Turma excluída com sucesso!")
                    st.session_state['show_delete_confirm'] = False
                    st.rerun()

            with col2:
                if st.button("❌ Não, Cancelar", use_container_width=True):
                    st.session_state['show_delete_confirm'] = False
                    st.rerun()

    with tab2:
        st.markdown("""
            <div class="custom-card">
                <h3 style="color: #6C63FF;">➕ Nova Turma</h3>
            </div>
        """, unsafe_allow_html=True)

        with st.form("nova_turma"):
            modalidades = buscar_dados(
                "SELECT codModalidade, nome FROM MODALIDADE WHERE status = 'A'"
            )
            professores = buscar_dados(
                "SELECT CPF, nome FROM PROFESSOR WHERE status = 'A'"
            )

            col1, col2 = st.columns(2)
            with col1:
                modalidade = st.selectbox("Modalidade", options=modalidades['nome'].tolist())
                horario = st.time_input("Horário")
            
            with col2:
                professor = st.selectbox("Professor", options=professores['nome'].tolist())
                dia_semana = st.selectbox(
                    "Dia da Semana",
                    options=["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]
                )

            capacidade = st.number_input("Capacidade", min_value=1, value=20)

            if st.form_submit_button("✅ Criar Turma", use_container_width=True):
                modalidade_id = modalidades[modalidades['nome'] == modalidade]['codModalidade'].iloc[0]
                professor_cpf = professores[professores['nome'] == professor]['CPF'].iloc[0]

                executar_query("""
                    INSERT INTO TURMA 
                    (codModalidade, CPF_professor, horario, diaSemana, capacidade, status)
                    VALUES (%s, %s, %s, %s, %s, 'A')
                """, (modalidade_id, professor_cpf, horario, dia_semana, capacidade))
                
                st.success("✅ Turma criada com sucesso!")
                st.rerun()

if __name__ == "__main__":
    mostrar_pagina()