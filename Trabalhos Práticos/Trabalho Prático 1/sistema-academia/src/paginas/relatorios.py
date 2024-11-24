import streamlit as st
from src.database.conexao import buscar_dados
from datetime import datetime
import locale

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
        .metric-card {
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 8px;
            text-align: center;
            margin: 0.5rem;
        }
        .metric-value {
            font-size: 2rem;
            font-weight: bold;
            color: #2C3E50;
            margin: 0.5rem 0;
        }
        .metric-label {
            color: #666;
            font-size: 1rem;
        }
        .chart-container {
            padding: 1rem;
            background: white;
            border-radius: 12px;
            margin: 1rem 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("📊 Relatórios")

    # Tabs para diferentes tipos de relatórios
    tabs = st.tabs([
        "📈 Financeiro", 
        "👥 Alunos", 
        "🏋️ Modalidades",
        "📅 Aulas"
    ])

    # Relatório Financeiro
    with tabs[0]:
        st.markdown("""
            <div class="custom-card">
                <h3>💰 Relatório Financeiro</h3>
            </div>
        """, unsafe_allow_html=True)

        # Filtro de período
        col1, col2 = st.columns([2,1])
        with col1:
            periodo = st.selectbox(
                "Período",
                ["Últimos 30 dias", "Últimos 90 dias", "Este ano", "Todo período"]
            )
        
        # Métricas financeiras principais
        metricas_query = """
            SELECT 
                COUNT(*) as total_pagamentos,
                SUM(valor) as receita_total,
                AVG(valor) as ticket_medio,
                MAX(valor) as maior_pagamento
            FROM PAGAMENTO 
            WHERE status = 'A'
            {}
        """

        if periodo == "Últimos 30 dias":
            filtro = "AND dataPagamento >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)"
        elif periodo == "Últimos 90 dias":
            filtro = "AND dataPagamento >= DATE_SUB(CURRENT_DATE, INTERVAL 90 DAY)"
        elif periodo == "Este ano":
            filtro = "AND YEAR(dataPagamento) = YEAR(CURRENT_DATE)"
        else:
            filtro = ""

        metricas = buscar_dados(metricas_query.format(filtro))

        if not metricas.empty:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown("""
                    <div class="metric-card">
                        <div class="metric-label">Receita Total</div>
                        <div class="metric-value">{}</div>
                    </div>
                """.format(formatar_moeda(metricas['receita_total'].iloc[0])), unsafe_allow_html=True)

            with col2:
                st.markdown("""
                    <div class="metric-card">
                        <div class="metric-label">Ticket Médio</div>
                        <div class="metric-value">{}</div>
                    </div>
                """.format(formatar_moeda(metricas['ticket_medio'].iloc[0])), unsafe_allow_html=True)

            with col3:
                st.markdown("""
                    <div class="metric-card">
                        <div class="metric-label">Total de Pagamentos</div>
                        <div class="metric-value">{}</div>
                    </div>
                """.format(metricas['total_pagamentos'].iloc[0]), unsafe_allow_html=True)

            with col4:
                st.markdown("""
                    <div class="metric-card">
                        <div class="metric-label">Maior Pagamento</div>
                        <div class="metric-value">{}</div>
                    </div>
                """.format(formatar_moeda(metricas['maior_pagamento'].iloc[0])), unsafe_allow_html=True)

        # Gráfico de receita por forma de pagamento
        receita_forma_pagamento = buscar_dados(f"""
            SELECT 
                formaPagamento,
                COUNT(*) as quantidade,
                SUM(valor) as total
            FROM PAGAMENTO
            WHERE status = 'A' {filtro}
            GROUP BY formaPagamento
        """)

        if not receita_forma_pagamento.empty:
            st.markdown("""
                <div class="chart-container">
                    <h4>Receita por Forma de Pagamento</h4>
                </div>
            """, unsafe_allow_html=True)
            st.bar_chart(receita_forma_pagamento.set_index('formaPagamento')['total'])

    # Relatório de Alunos
    with tabs[1]:
        st.markdown("""
            <div class="custom-card">
                <h3>👥 Relatório de Alunos</h3>
            </div>
        """, unsafe_allow_html=True)

        # Métricas de alunos
        metricas_alunos = buscar_dados("""
            SELECT 
                (SELECT COUNT(*) FROM ALUNO WHERE status = 'A') as alunos_ativos,
                (SELECT COUNT(*) FROM MATRICULA WHERE status = 'A' AND dataFim >= CURRENT_DATE) as matriculas_ativas,
                (SELECT COUNT(*) FROM ALUNO_TURMA WHERE status = 'A') as inscricoes_aulas
        """)

        if not metricas_alunos.empty:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("""
                    <div class="metric-card">
                        <div class="metric-label">Alunos Ativos</div>
                        <div class="metric-value">{}</div>
                    </div>
                """.format(metricas_alunos['alunos_ativos'].iloc[0]), unsafe_allow_html=True)

            with col2:
                st.markdown("""
                    <div class="metric-card">
                        <div class="metric-label">Matrículas Ativas</div>
                        <div class="metric-value">{}</div>
                    </div>
                """.format(metricas_alunos['matriculas_ativas'].iloc[0]), unsafe_allow_html=True)

            with col3:
                st.markdown("""
                    <div class="metric-card">
                        <div class="metric-label">Inscrições em Aulas</div>
                        <div class="metric-value">{}</div>
                    </div>
                """.format(metricas_alunos['inscricoes_aulas'].iloc[0]), unsafe_allow_html=True)

        # Gráfico de alunos por modalidade
        alunos_modalidade = buscar_dados("""
            SELECT 
                m.nome as modalidade,
                COUNT(DISTINCT at.CPF_aluno) as total_alunos
            FROM MODALIDADE m
            LEFT JOIN TURMA t ON m.codModalidade = t.codModalidade
            LEFT JOIN ALUNO_TURMA at ON t.codTurma = at.codTurma
            WHERE m.status = 'A'
            GROUP BY m.codModalidade, m.nome
            ORDER BY total_alunos DESC
        """)

        if not alunos_modalidade.empty:
            st.markdown("""
                <div class="chart-container">
                    <h4>Alunos por Modalidade</h4>
                </div>
            """, unsafe_allow_html=True)
            st.bar_chart(alunos_modalidade.set_index('modalidade')['total_alunos'])

    # Relatório de Modalidades
    with tabs[2]:
        st.markdown("""
            <div class="custom-card">
                <h3>🏋️ Relatório de Modalidades</h3>
            </div>
        """, unsafe_allow_html=True)

        # Métricas de modalidades
        metricas_modalidades = buscar_dados("""
            SELECT 
                (SELECT COUNT(*) FROM MODALIDADE WHERE status = 'A') as modalidades_ativas,
                (SELECT COUNT(*) FROM TURMA WHERE status = 'A') as turmas_ativas,
                (SELECT COUNT(DISTINCT CPF_professor) FROM TURMA WHERE status = 'A') as professores_ativos
        """)

        if not metricas_modalidades.empty:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("""
                    <div class="metric-card">
                        <div class="metric-label">Modalidades Ativas</div>
                        <div class="metric-value">{}</div>
                    </div>
                """.format(metricas_modalidades['modalidades_ativas'].iloc[0]), unsafe_allow_html=True)

            with col2:
                st.markdown("""
                    <div class="metric-card">
                        <div class="metric-label">Turmas Ativas</div>
                        <div class="metric-value">{}</div>
                    </div>
                """.format(metricas_modalidades['turmas_ativas'].iloc[0]), unsafe_allow_html=True)

            with col3:
                st.markdown("""
                    <div class="metric-card">
                        <div class="metric-label">Professores Ativos</div>
                        <div class="metric-value">{}</div>
                    </div>
                """.format(metricas_modalidades['professores_ativos'].iloc[0]), unsafe_allow_html=True)

    # Relatório de Aulas
    with tabs[3]:
        st.markdown("""
            <div class="custom-card">
                <h3>📅 Relatório de Aulas</h3>
            </div>
        """, unsafe_allow_html=True)

        # Ocupação das turmas
        ocupacao_turmas = buscar_dados("""
            SELECT 
                m.nome as modalidade,
                t.diaSemana,
                TIME_FORMAT(t.horario, '%H:%i') as horario,
                p.nome as professor,
                t.capacidade,
                COUNT(at.codAluno_Turma) as alunos_inscritos,
                ROUND((COUNT(at.codAluno_Turma) / t.capacidade) * 100, 1) as ocupacao
            FROM TURMA t
            JOIN MODALIDADE m ON t.codModalidade = m.codModalidade
            JOIN PROFESSOR p ON t.CPF_professor = p.CPF
            LEFT JOIN ALUNO_TURMA at ON t.codTurma = at.codTurma AND at.status = 'A'
            WHERE t.status = 'A'
            GROUP BY t.codTurma
            ORDER BY t.diaSemana, t.horario
        """)

        if not ocupacao_turmas.empty:
            st.markdown("""
                <div class="custom-card">
                    <h4>Ocupação das Turmas</h4>
                </div>
            """, unsafe_allow_html=True)

            for _, turma in ocupacao_turmas.iterrows():
                ocupacao = turma['ocupacao']
                cor = '#4CAF50' if ocupacao < 70 else '#FFA726' if ocupacao < 90 else '#FF6B6B'
                
                st.markdown(f"""
                    <div class="custom-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <h4 style="margin: 0;">{turma['modalidade']}</h4>
                                <p style="margin: 0; color: #666;">
                                    {turma['diaSemana']} às {turma['horario']} - Prof. {turma['professor']}
                                </p>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 1.5rem; font-weight: bold; color: {cor};">
                                    {turma['ocupacao']}%
                                </div>
                                <p style="margin: 0; color: #666;">
                                    {turma['alunos_inscritos']}/{turma['capacidade']} alunos
                                </p>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    mostrar_pagina()