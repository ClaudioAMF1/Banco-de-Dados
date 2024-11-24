import streamlit as st
from src.database.conexao import executar_query, buscar_dados
from datetime import datetime, timedelta
import locale
import time

# Configurar formatação de moeda para Real brasileiro
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except:
    locale.setlocale(locale.LC_ALL, '')

def formatar_moeda(valor):
    if isinstance(valor, str):
        valor = float(valor)
    return locale.currency(valor, grouping=True, symbol='R$')

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
        .status-ativa { background-color: #4CAF50; color: white; }
        .status-vencida { background-color: #FF6B6B; color: white; }
        .plano-info {
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
            transition: all 0.2s ease;
        }
        .plano-info.selected {
            border-color: #6C63FF;
            background: #f8f9ff;
        }
        .preco-destaque {
            font-size: 1.5rem;
            font-weight: bold;
            color: #6C63FF;
            margin: 0.5rem 0;
        }
        .info-box {
            background-color: #f8f9fa;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("💳 Matrículas")
    
    tabs = st.tabs(["📋 Matrículas Ativas", "➕ Nova Matrícula"])
    
    with tabs[0]:
        # Filtros
        col1, col2 = st.columns([2,1])
        with col1:
            pesquisa = st.text_input("🔍", placeholder="Buscar por nome do aluno...")
        with col2:
            situacao = st.selectbox(
                "Situação",
                ["Todas", "Ativas", "Vencidas"]
            )

        # Consulta de matrículas
        query = """
            SELECT 
                m.codMatricula,
                a.nome as aluno,
                p.nome as plano,
                m.dataInicio,
                m.dataFim,
                p.valor,
                CASE 
                    WHEN m.dataFim >= CURRENT_DATE THEN 'Ativa'
                    ELSE 'Vencida'
                END as situacao
            FROM MATRICULA m
            JOIN ALUNO a ON m.CPF_aluno = a.CPF
            JOIN PLANO p ON m.codPlano = p.codPlano
            WHERE m.status = 'A'
            AND (a.nome LIKE %s OR %s = '')
            AND (
                %s = 'Todas' 
                OR (%s = 'Ativas' AND m.dataFim >= CURRENT_DATE)
                OR (%s = 'Vencidas' AND m.dataFim < CURRENT_DATE)
            )
            ORDER BY 
                CASE WHEN m.dataFim >= CURRENT_DATE THEN 0 ELSE 1 END,
                m.dataFim DESC
        """
        params = (f"%{pesquisa}%", pesquisa, situacao, situacao, situacao)
        
        matriculas = buscar_dados(query, params)

        if matriculas.empty:
            st.info("🔍 Nenhuma matrícula encontrada")
        else:
            for _, matricula in matriculas.iterrows():
                with st.container():
                    data_inicio = matricula['dataInicio'].strftime('%d/%m/%Y') if isinstance(matricula['dataInicio'], datetime) else matricula['dataInicio']
                    data_fim = matricula['dataFim'].strftime('%d/%m/%Y') if isinstance(matricula['dataFim'], datetime) else matricula['dataFim']
                    
                    st.markdown(f"""
                        <div class="custom-card">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <h3 style="margin: 0;">{matricula['aluno']}</h3>
                                    <p style="margin: 0; color: #666;">{matricula['plano']}</p>
                                </div>
                                <div>
                                    <span class="status-badge status-{'ativa' if matricula['situacao'] == 'Ativa' else 'vencida'}">
                                        {matricula['situacao']}
                                    </span>
                                </div>
                            </div>
                            <div style="margin-top: 1rem; display: flex; justify-content: space-between;">
                                <div>
                                    <p>📅 Início: {data_inicio}</p>
                                    <p>📅 Fim: {data_fim}</p>
                                </div>
                                <div>
                                    <p class="preco-destaque">{formatar_moeda(matricula['valor'])}</p>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                    with st.form(key=f"matricula_form_{matricula['codMatricula']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button("🔄 Renovar", use_container_width=True):
                                st.session_state['renovando_matricula'] = int(matricula['codMatricula'])
                                st.session_state['show_renew_form'] = True
                                st.rerun()
                        with col2:
                            if st.form_submit_button("❌ Cancelar", use_container_width=True):
                                st.session_state['cancelando_matricula'] = int(matricula['codMatricula'])
                                st.session_state['show_cancel_confirm'] = True
                                st.rerun()

                                # Modal de Renovação
        if 'show_renew_form' in st.session_state and st.session_state['show_renew_form']:
            matricula_atual = buscar_dados("""
                SELECT m.*, p.nome as plano, p.valor, a.nome as aluno
                FROM MATRICULA m
                JOIN PLANO p ON m.codPlano = p.codPlano
                JOIN ALUNO a ON m.CPF_aluno = a.CPF
                WHERE m.codMatricula = %s
            """, (st.session_state['renovando_matricula'],)).iloc[0]

            st.markdown("""
                <div class="custom-card">
                    <h3 style="color: #6C63FF;">🔄 Renovar Matrícula</h3>
                </div>
            """, unsafe_allow_html=True)

            with st.form("renovar_matricula"):
                st.info(f"Renovando matrícula de: {matricula_atual['aluno']}")

                planos = buscar_dados("SELECT * FROM PLANO WHERE status = 'A'")
                planos_opcoes = planos['nome'].astype(str).tolist()
                plano_atual_index = planos_opcoes.index(str(matricula_atual['plano']))

                plano = st.selectbox(
                    "Plano",
                    options=planos_opcoes,
                    index=plano_atual_index
                )

                data_inicio = st.date_input(
                    "Data de Início",
                    value=matricula_atual['dataFim'] + timedelta(days=1),
                    min_value=datetime.now().date()
                )

                plano_selecionado = planos[planos['nome'] == plano].iloc[0]
                data_fim = data_inicio + timedelta(days=30 * int(plano_selecionado['duracao']))
                st.info(f"Data de término: {data_fim.strftime('%d/%m/%Y')}")

                forma_pagamento = st.selectbox(
                    "Forma de Pagamento",
                    ["Dinheiro", "Cartão Débito", "Cartão Crédito", "PIX"]
                )

                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("✅ Confirmar Renovação", use_container_width=True):
                        try:
                            # Inativa a matrícula atual
                            executar_query(
                                "UPDATE MATRICULA SET status = 'I' WHERE codMatricula = %s",
                                (st.session_state['renovando_matricula'],)
                            )

                            # Cria nova matrícula
                            query_matricula = """
                                INSERT INTO MATRICULA 
                                (CPF_aluno, codPlano, dataInicio, dataFim, status)
                                VALUES (%s, %s, %s, %s, 'A')
                            """
                            nova_matricula = executar_query(
                                query_matricula,
                                (matricula_atual['CPF_aluno'], plano_selecionado['codPlano'],
                                 data_inicio, data_fim)
                            )

                            # Registra pagamento
                            if nova_matricula:
                                query_pagamento = """
                                    INSERT INTO PAGAMENTO 
                                    (codMatricula, dataPagamento, valor, formaPagamento, status)
                                    VALUES (%s, %s, %s, %s, 'A')
                                """
                                executar_query(
                                    query_pagamento,
                                    (nova_matricula, datetime.now().date(),
                                     plano_selecionado['valor'], forma_pagamento)
                                )

                                st.success("✅ Matrícula renovada com sucesso!")
                                st.session_state['show_renew_form'] = False
                                st.rerun()
                        except Exception as e:
                            st.error(f"Erro ao renovar matrícula: {str(e)}")

                with col2:
                    if st.form_submit_button("❌ Cancelar", use_container_width=True):
                        st.session_state['show_renew_form'] = False
                        st.rerun()

        # Modal de Cancelamento
        if 'show_cancel_confirm' in st.session_state and st.session_state['show_cancel_confirm']:
            with st.form("confirmar_cancelamento"):
                st.markdown("""
                    <div class="custom-card" style="border: 2px solid #FF6B6B;">
                        <h3 style="color: #FF6B6B;">⚠️ Confirmar Cancelamento</h3>
                        <p>Tem certeza que deseja cancelar esta matrícula?</p>
                        <p style="color: #666;">Esta ação não pode ser desfeita.</p>
                    </div>
                """, unsafe_allow_html=True)

                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("✔️ Sim, Cancelar Matrícula", use_container_width=True):
                        executar_query(
                            "UPDATE MATRICULA SET status = 'I' WHERE codMatricula = %s",
                            (st.session_state['cancelando_matricula'],)
                        )
                        st.success("✅ Matrícula cancelada com sucesso!")
                        st.session_state['show_cancel_confirm'] = False
                        st.rerun()

                with col2:
                    if st.form_submit_button("❌ Não, Manter Matrícula", use_container_width=True):
                        st.session_state['show_cancel_confirm'] = False
                        st.rerun()

    with tabs[1]:
        st.markdown("""
            <div class="custom-card">
                <h3 style="color: #6C63FF;">➕ Nova Matrícula</h3>
            </div>
        """, unsafe_allow_html=True)

        with st.form("nova_matricula"):
            alunos = buscar_dados("""
                SELECT a.CPF, a.nome
                FROM ALUNO a
                WHERE a.status = 'A'
                AND NOT EXISTS (
                    SELECT 1 FROM MATRICULA m
                    WHERE m.CPF_aluno = a.CPF
                    AND m.status = 'A'
                    AND m.dataFim >= CURRENT_DATE
                )
                ORDER BY a.nome
            """)

            planos = buscar_dados("SELECT * FROM PLANO WHERE status = 'A' ORDER BY valor")

            if alunos.empty:
                st.warning("Não há alunos disponíveis para nova matrícula")
                st.stop()

            # Seleção do aluno e data
            col1, col2 = st.columns(2)
            with col1:
                aluno = st.selectbox(
                    "Aluno",
                    options=alunos['nome'].astype(str).tolist(),
                    placeholder="Selecione o aluno"
                )

            with col2:
                data_inicio = st.date_input(
                    "Data de Início",
                    value=datetime.now().date(),
                    min_value=datetime.now().date()
                )

            # Seleção do plano
            st.markdown("<h4>Selecione o Plano</h4>", unsafe_allow_html=True)
            
            plano_escolhido = st.radio(
                "Plano",
                options=[f"{p['nome']} - {formatar_moeda(float(p['valor']))}/mês" for _, p in planos.iterrows()],
                horizontal=True,
                label_visibility="collapsed"
            )

            if plano_escolhido:
                plano_nome = plano_escolhido.split(" - ")[0]
                plano_info = planos[planos['nome'] == plano_nome].iloc[0]
                
                st.markdown(f"""
                    <div class="info-box">
                        <h4>{plano_info['nome']}</h4>
                        <p class="preco-destaque">{formatar_moeda(float(plano_info['valor']))}/mês</p>
                        <p>Duração: {int(plano_info['duracao'])} {'meses' if int(plano_info['duracao']) > 1 else 'mês'}</p>
                        <p>{plano_info['descricao'] or ''}</p>
                    </div>
                """, unsafe_allow_html=True)

            forma_pagamento = st.selectbox(
                "Forma de Pagamento",
                ["Dinheiro", "Cartão Débito", "Cartão Crédito", "PIX"]
            )

            if st.form_submit_button("✅ Confirmar Matrícula", use_container_width=True):
                if not aluno:
                    st.error("Por favor, selecione um aluno!")
                elif not plano_escolhido:
                    st.error("Por favor, selecione um plano!")
                else:
                    try:
                        aluno_cpf = alunos[alunos['nome'] == aluno]['CPF'].iloc[0]
                        plano_nome = plano_escolhido.split(" - ")[0]
                        plano_info = planos[planos['nome'] == plano_nome].iloc[0]
                        
                        # Calcular data fim
                        data_fim = data_inicio + timedelta(days=30 * int(plano_info['duracao']))
                        
                        # Criar matrícula
                        query_matricula = """
                            INSERT INTO MATRICULA 
                            (CPF_aluno, codPlano, dataInicio, dataFim, status)
                            VALUES (%s, %s, %s, %s, 'A')
                        """
                        matricula_id = executar_query(
                            query_matricula,
                            (aluno_cpf, int(plano_info['codPlano']), data_inicio, data_fim)
                        )

                        if matricula_id:
                            # Registrar pagamento
                            query_pagamento = """
                                INSERT INTO PAGAMENTO 
                                (codMatricula, dataPagamento, valor, formaPagamento, status)
                                VALUES (%s, %s, %s, %s, 'A')
                            """
                            executar_query(
                                query_pagamento,
                                (matricula_id, datetime.now().date(),
                                 float(plano_info['valor']), forma_pagamento)
                            )

                            st.success(f"""
                                ✅ Matrícula realizada com sucesso!
                                
                                📝 Detalhes:
                                - Aluno: {aluno}
                                - Plano: {plano_info['nome']}
                                - Valor: {formatar_moeda(float(plano_info['valor']))}
                                - Início: {data_inicio.strftime('%d/%m/%Y')}
                                - Fim: {data_fim.strftime('%d/%m/%Y')}
                                
                                💰 Pagamento registrado automaticamente.
                            """)
                            time.sleep(2)
                            st.rerun()

                    except Exception as e:
                        st.error(f"Erro ao realizar matrícula: {str(e)}")

if __name__ == "__main__":
    mostrar_pagina()