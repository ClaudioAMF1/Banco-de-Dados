import streamlit as st
from src.database.conexao import buscar_dados
from datetime import datetime
import locale
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
        .view-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.05);
            margin: 1rem 0;
            transition: all 0.3s ease;
        }
        .view-card:hover {
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        }
        .metric-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin: 1rem 0;
        }
        .metric-item {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 8px;
            text-align: center;
        }
        .metric-value {
            font-size: 1.5rem;
            font-weight: bold;
            color: #2C3E50;
        }
        .metric-label {
            color: #666;
            font-size: 0.9rem;
        }
        .tab-content {
            padding: 1rem;
            background: white;
            border-radius: 0 0 12px 12px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("📊 Views do Sistema")

    # Abas para diferentes views
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Alunos Ativos",
        "Turmas",
        "Inadimplentes",
        "Ocupação",
        "Professores",
        "Renovações"
    ])

    with tab1:
        st.header("Alunos Ativos")
        alunos_ativos = buscar_dados("""
            SELECT 
                a.nome AS nome_aluno,
                a.telefone,
                DATE_FORMAT(m.dataInicio, '%d/%m/%Y') as data_inicio,
                DATE_FORMAT(m.dataFim, '%d/%m/%Y') as data_fim,
                p.nome AS plano,
                p.valor
            FROM ALUNO a
            INNER JOIN MATRICULA m ON a.CPF = m.CPF_aluno
            INNER JOIN PLANO p ON m.codPlano = p.codPlano
            WHERE a.status = 'A' AND m.status = 'A'
            AND m.dataFim >= CURRENT_DATE
            ORDER BY a.nome
        """)

        if not alunos_ativos.empty:
            # Métricas
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total de Alunos Ativos", len(alunos_ativos))
            with col2:
                valor_medio = alunos_ativos['valor'].mean()
                st.metric("Ticket Médio", formatar_moeda(valor_medio))
            with col3:
                receita_total = alunos_ativos['valor'].sum()
                st.metric("Receita Total", formatar_moeda(receita_total))

            # Gráfico de distribuição por plano
            planos_dist = alunos_ativos.groupby('plano').size().reset_index(name='count')
            fig = px.pie(planos_dist, values='count', names='plano', title='Distribuição por Plano')
            st.plotly_chart(fig, use_container_width=True)

            # Tabela de alunos
            st.dataframe(alunos_ativos, use_container_width=True)

            # Botão de download
            csv = alunos_ativos.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Download CSV",
                csv,
                "alunos_ativos.csv",
                "text/csv",
                key='download-csv-alunos'
            )

    with tab2:
        st.header("Turmas e Ocupação")
        turmas = buscar_dados("""
            SELECT 
                m.nome AS modalidade,
                t.diaSemana,
                TIME_FORMAT(t.horario, '%H:%i') as horario,
                p.nome AS professor,
                t.capacidade,
                COUNT(at.codAluno_Turma) as alunos_inscritos,
                ROUND((COUNT(at.codAluno_Turma) / t.capacidade * 100), 1) as taxa_ocupacao
            FROM TURMA t
            INNER JOIN MODALIDADE m ON t.codModalidade = m.codModalidade
            INNER JOIN PROFESSOR p ON t.CPF_professor = p.CPF
            LEFT JOIN ALUNO_TURMA at ON t.codTurma = at.codTurma AND at.status = 'A'
            WHERE t.status = 'A'
            GROUP BY t.codTurma
            ORDER BY t.diaSemana, t.horario
        """)

        if not turmas.empty:
            # Métricas
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total de Turmas", len(turmas))
            with col2:
                ocupacao_media = turmas['taxa_ocupacao'].mean()
                st.metric("Ocupação Média", f"{ocupacao_media:.1f}%")
            with col3:
                turmas_lotadas = len(turmas[turmas['taxa_ocupacao'] >= 90])
                st.metric("Turmas Lotadas", turmas_lotadas)

            # Heatmap de ocupação
            pivot = pd.pivot_table(
                turmas, 
                values='alunos_inscritos', 
                index='diaSemana',
                columns='horario',
                fill_value=0
            )

            fig = go.Figure(data=go.Heatmap(
                z=pivot.values,
                x=pivot.columns,
                y=pivot.index,
                colorscale='Blues'
            ))
            fig.update_layout(
                title='Mapa de Calor - Ocupação por Horário',
                xaxis_title='Horário',
                yaxis_title='Dia da Semana'
            )
            st.plotly_chart(fig, use_container_width=True)

            # Tabela de turmas
            st.dataframe(turmas, use_container_width=True)

            # Download
            csv = turmas.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Download CSV",
                csv,
                "turmas.csv",
                "text/csv",
                key='download-csv-turmas'
            )

    with tab3:
        st.header("Inadimplentes")
        inadimplentes = buscar_dados("""
            SELECT 
                a.nome AS aluno,
                a.telefone,
                DATE_FORMAT(m.dataFim, '%d/%m/%Y') as vencimento,
                p.valor,
                DATEDIFF(CURRENT_DATE, m.dataFim) AS dias_atraso
            FROM MATRICULA m
            INNER JOIN ALUNO a ON m.CPF_aluno = a.CPF
            INNER JOIN PLANO p ON m.codPlano = p.codPlano
            WHERE m.dataFim < CURRENT_DATE
            AND m.status = 'A'
            AND NOT EXISTS (
                SELECT 1 FROM PAGAMENTO pg 
                WHERE pg.codMatricula = m.codMatricula 
                AND pg.dataPagamento > m.dataFim
            )
            ORDER BY dias_atraso DESC
        """)

        if not inadimplentes.empty:
            # Métricas
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Inadimplentes", len(inadimplentes))
            with col2:
                valor_total = inadimplentes['valor'].sum()
                st.metric("Valor Total em Atraso", formatar_moeda(valor_total))
            with col3:
                media_atraso = inadimplentes['dias_atraso'].mean()
                st.metric("Média de Dias em Atraso", f"{media_atraso:.0f}")

            # Gráfico de distribuição de atraso
            fig = px.histogram(
                inadimplentes, 
                x='dias_atraso',
                title='Distribuição dos Dias em Atraso',
                nbins=20
            )
            st.plotly_chart(fig, use_container_width=True)

            # Tabela
            st.dataframe(inadimplentes, use_container_width=True)

            # Download
            csv = inadimplentes.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Download CSV",
                csv,
                "inadimplentes.csv",
                "text/csv",
                key='download-csv-inadimplentes'
            )

    with tab4:
        st.header("Ocupação da Academia")
        ocupacao = buscar_dados("""
            SELECT 
                t.diaSemana,
                TIME_FORMAT(t.horario, '%H:%i') as horario,
                COUNT(DISTINCT t.codTurma) as total_turmas,
                SUM(t.capacidade) as capacidade_total,
                COUNT(DISTINCT at.CPF_aluno) as total_alunos,
                ROUND((COUNT(DISTINCT at.CPF_aluno) / SUM(t.capacidade)) * 100, 2) as taxa_ocupacao
            FROM TURMA t
            LEFT JOIN ALUNO_TURMA at ON t.codTurma = at.codTurma AND at.status = 'A'
            WHERE t.status = 'A'
            GROUP BY t.diaSemana, t.horario
            ORDER BY 
                CASE 
                    WHEN t.diaSemana = 'Segunda' THEN 1
                    WHEN t.diaSemana = 'Terça' THEN 2
                    WHEN t.diaSemana = 'Quarta' THEN 3
                    WHEN t.diaSemana = 'Quinta' THEN 4
                    WHEN t.diaSemana = 'Sexta' THEN 5
                    WHEN t.diaSemana = 'Sábado' THEN 6
                    ELSE 7
                END,
                t.horario
        """)

        if not ocupacao.empty:
            # Métricas
            col1, col2, col3 = st.columns(3)
            with col1:
                ocupacao_media = ocupacao['taxa_ocupacao'].mean()
                st.metric("Ocupação Média", f"{ocupacao_media:.1f}%")
            with col2:
                total_capacidade = ocupacao['capacidade_total'].sum()
                st.metric("Capacidade Total", total_capacidade)
            with col3:
                total_alunos = ocupacao['total_alunos'].sum()
                st.metric("Total de Alunos", total_alunos)

            # Heatmap de ocupação
            pivot = pd.pivot_table(
                ocupacao, 
                values='taxa_ocupacao', 
                index='diaSemana',
                columns='horario',
                fill_value=0
            )

            fig = go.Figure(data=go.Heatmap(
                z=pivot.values,
                x=pivot.columns,
                y=pivot.index,
                colorscale='RdYlGn'
            ))
            fig.update_layout(
                title='Taxa de Ocupação por Horário',
                xaxis_title='Horário',
                yaxis_title='Dia da Semana'
            )
            st.plotly_chart(fig, use_container_width=True)

            # Tabela
            st.dataframe(ocupacao, use_container_width=True)

            # Download
            csv = ocupacao.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Download CSV",
                csv,
                "ocupacao.csv",
                "text/csv",
                key='download-csv-ocupacao'
            )

    # Continue com as outras tabs...


    with tab5:
        st.header("Desempenho dos Professores")
        professores = buscar_dados("""
            SELECT 
                p.nome AS professor,
                m.nome AS modalidade,
                COUNT(DISTINCT at.CPF_aluno) AS total_alunos,
                COUNT(DISTINCT t.codTurma) AS total_turmas,
                ROUND(AVG(t.capacidade), 0) as media_capacidade,
                ROUND((COUNT(DISTINCT at.CPF_aluno) / SUM(t.capacidade) * 100), 1) as taxa_ocupacao
            FROM PROFESSOR p
            INNER JOIN TURMA t ON p.CPF = t.CPF_professor
            INNER JOIN MODALIDADE m ON t.codModalidade = m.codModalidade
            LEFT JOIN ALUNO_TURMA at ON t.codTurma = at.codTurma AND at.status = 'A'
            WHERE t.status = 'A' AND p.status = 'A'
            GROUP BY p.CPF, m.codModalidade
            ORDER BY total_alunos DESC
        """)

        if not professores.empty:
            # Métricas
            col1, col2, col3 = st.columns(3)
            with col1:
                total_profs = len(professores['professor'].unique())
                st.metric("Total de Professores", total_profs)
            with col2:
                media_alunos = professores['total_alunos'].mean()
                st.metric("Média de Alunos/Professor", f"{media_alunos:.0f}")
            with col3:
                ocupacao_media = professores['taxa_ocupacao'].mean()
                st.metric("Taxa Média de Ocupação", f"{ocupacao_media:.1f}%")

            # Gráfico de barras empilhadas por modalidade
            fig = px.bar(
                professores,
                x='professor',
                y='total_alunos',
                color='modalidade',
                title='Alunos por Professor e Modalidade',
                labels={'professor': 'Professor', 'total_alunos': 'Total de Alunos', 'modalidade': 'Modalidade'}
            )
            st.plotly_chart(fig, use_container_width=True)

            # Gráfico de ocupação
            fig2 = px.scatter(
                professores,
                x='total_turmas',
                y='taxa_ocupacao',
                size='total_alunos',
                color='modalidade',
                hover_data=['professor'],
                title='Análise de Ocupação por Professor'
            )
            st.plotly_chart(fig2, use_container_width=True)

            # Tabela detalhada
            st.dataframe(professores, use_container_width=True)

            # Download
            csv = professores.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Download CSV",
                csv,
                "desempenho_professores.csv",
                "text/csv",
                key='download-csv-professores'
            )

    with tab6:
        st.header("Histórico de Renovações")
        renovacoes = buscar_dados("""
            SELECT 
                a.nome AS aluno,
                p.nome AS plano,
                COUNT(*) AS total_renovacoes,
                MIN(DATE_FORMAT(m.dataInicio, '%d/%m/%Y')) as primeira_matricula,
                MAX(DATE_FORMAT(m.dataInicio, '%d/%m/%Y')) as ultima_matricula,
                SUM(p.valor) as valor_total
            FROM ALUNO a
            INNER JOIN MATRICULA m ON a.CPF = m.CPF_aluno
            INNER JOIN PLANO p ON m.codPlano = p.codPlano
            GROUP BY a.CPF, p.codPlano
            HAVING COUNT(*) > 1
            ORDER BY total_renovacoes DESC, valor_total DESC
        """)

        if not renovacoes.empty:
            # Métricas
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total de Renovações", renovacoes['total_renovacoes'].sum())
            with col2:
                media_renovacoes = renovacoes['total_renovacoes'].mean()
                st.metric("Média de Renovações", f"{media_renovacoes:.1f}")
            with col3:
                valor_total = renovacoes['valor_total'].sum()
                st.metric("Valor Total", formatar_moeda(valor_total))

            # Gráfico de distribuição de renovações
            fig = px.histogram(
                renovacoes,
                x='total_renovacoes',
                title='Distribuição do Número de Renovações',
                labels={'total_renovacoes': 'Número de Renovações', 'count': 'Quantidade de Alunos'}
            )
            st.plotly_chart(fig, use_container_width=True)

            # Gráfico de valor total por plano
            fig2 = px.pie(
                renovacoes,
                values='valor_total',
                names='plano',
                title='Distribuição do Valor Total por Plano'
            )
            st.plotly_chart(fig2, use_container_width=True)

            # Top 5 alunos mais fiéis
            st.subheader("Top 5 Alunos com Mais Renovações")
            top_5 = renovacoes.nlargest(5, 'total_renovacoes')
            
            for _, aluno in top_5.iterrows():
                st.markdown(f"""
                    <div class="view-card">
                        <h4>{aluno['aluno']}</h4>
                        <div class="metric-grid">
                            <div class="metric-item">
                                <div class="metric-value">{aluno['total_renovacoes']}</div>
                                <div class="metric-label">Renovações</div>
                            </div>
                            <div class="metric-item">
                                <div class="metric-value">{formatar_moeda(aluno['valor_total'])}</div>
                                <div class="metric-label">Valor Total</div>
                            </div>
                            <div class="metric-item">
                                <div class="metric-value">{aluno['plano']}</div>
                                <div class="metric-label">Plano Atual</div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            # Tabela completa
            st.subheader("Todos os Alunos com Renovações")
            st.dataframe(renovacoes, use_container_width=True)

            # Download
            csv = renovacoes.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Download CSV",
                csv,
                "renovacoes_matricula.csv",
                "text/csv",
                key='download-csv-renovacoes'
            )

    st.markdown("---")
    st.subheader("📈 Estatísticas Gerais do Sistema")

    stats = buscar_dados("""
        SELECT
            (SELECT COUNT(*) FROM ALUNO WHERE status = 'A') as total_alunos,
            (SELECT COUNT(*) FROM PROFESSOR WHERE status = 'A') as total_professores,
            (SELECT COUNT(*) FROM MODALIDADE WHERE status = 'A') as total_modalidades,
            (SELECT COUNT(*) FROM TURMA WHERE status = 'A') as total_turmas,
            (SELECT COUNT(*) FROM MATRICULA WHERE status = 'A' AND dataFim >= CURRENT_DATE) as matriculas_ativas,
            (SELECT SUM(valor) FROM PAGAMENTO WHERE status = 'A' AND MONTH(dataPagamento) = MONTH(CURRENT_DATE)) as faturamento_mes
    """)

    if not stats.empty:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
                <div class="view-card">
                    <h4>👥 Pessoas</h4>
                    <div class="metric-grid">
                        <div class="metric-item">
                            <div class="metric-value">{}</div>
                            <div class="metric-label">Alunos</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-value">{}</div>
                            <div class="metric-label">Professores</div>
                        </div>
                    </div>
                </div>
            """.format(
                stats['total_alunos'].iloc[0],
                stats['total_professores'].iloc[0]
            ), unsafe_allow_html=True)

        with col2:
            st.markdown("""
                <div class="view-card">
                    <h4>🏋️‍♂️ Atividades</h4>
                    <div class="metric-grid">
                        <div class="metric-item">
                            <div class="metric-value">{}</div>
                            <div class="metric-label">Modalidades</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-value">{}</div>
                            <div class="metric-label">Turmas</div>
                        </div>
                    </div>
                </div>
            """.format(
                stats['total_modalidades'].iloc[0],
                stats['total_turmas'].iloc[0]
            ), unsafe_allow_html=True)

        with col3:
            st.markdown("""
                <div class="view-card">
                    <h4>💰 Financeiro</h4>
                    <div class="metric-grid">
                        <div class="metric-item">
                            <div class="metric-value">{}</div>
                            <div class="metric-label">Matrículas Ativas</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-value">{}</div>
                            <div class="metric-label">Faturamento do Mês</div>
                        </div>
                    </div>
                </div>
            """.format(
                stats['matriculas_ativas'].iloc[0],
                formatar_moeda(stats['faturamento_mes'].iloc[0])
            ), unsafe_allow_html=True)

if __name__ == "__main__":
    mostrar_pagina()
