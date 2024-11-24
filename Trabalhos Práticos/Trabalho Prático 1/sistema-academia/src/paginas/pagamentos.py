import streamlit as st
from src.database.conexao import executar_query, buscar_dados
from datetime import datetime, timedelta
import locale
import pandas as pd

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
        .payment-badge {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
            display: inline-block;
        }
        .payment-dinheiro { background-color: #4CAF50; color: white; }
        .payment-cartao { background-color: #2196F3; color: white; }
        .payment-pix { background-color: #9C27B0; color: white; }
        .summary-card {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 8px;
            margin: 0.5rem 0;
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
        </style>
    """, unsafe_allow_html=True)

    st.title("💰 Pagamentos")

    tabs = st.tabs(["📊 Histórico de Pagamentos", "➕ Novo Pagamento"])

    with tabs[0]:
        # Filtros
        col1, col2, col3 = st.columns([2,1,1])
        with col1:
            pesquisa = st.text_input("🔍", placeholder="Buscar por nome do aluno...")
        with col2:
            periodo = st.selectbox(
                "Período",
                ["Últimos 30 dias", "Últimos 90 dias", "Este ano", "Todos"]
            )
        with col3:
            forma_pagamento = st.selectbox(
                "Forma de Pagamento",
                ["Todas", "Dinheiro", "Cartão Débito", "Cartão Crédito", "PIX"]
            )

        # Construir query com base nos filtros
        query = """
            SELECT 
                p.codPagamento,
                a.nome as aluno,
                pl.nome as plano,
                p.dataPagamento,
                p.valor,
                p.formaPagamento,
                p.status
            FROM PAGAMENTO p
            JOIN MATRICULA m ON p.codMatricula = m.codMatricula
            JOIN ALUNO a ON m.CPF_aluno = a.CPF
            JOIN PLANO pl ON m.codPlano = pl.codPlano
            WHERE p.status = 'A'
            AND (a.nome LIKE %s OR %s = '')
            AND (p.formaPagamento = %s OR %s = 'Todas')
        """

        # Adicionar filtro de período
        if periodo == "Últimos 30 dias":
            query += " AND p.dataPagamento >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)"
        elif periodo == "Últimos 90 dias":
            query += " AND p.dataPagamento >= DATE_SUB(CURRENT_DATE, INTERVAL 90 DAY)"
        elif periodo == "Este ano":
            query += " AND YEAR(p.dataPagamento) = YEAR(CURRENT_DATE)"

        query += " ORDER BY p.dataPagamento DESC"

        params = (f"%{pesquisa}%", pesquisa, forma_pagamento, forma_pagamento)
        pagamentos = buscar_dados(query, params)

        if not pagamentos.empty:
            # Resumo financeiro
            total_periodo = pagamentos['valor'].sum()
            media_pagamento = pagamentos['valor'].mean()
            total_pagamentos = len(pagamentos)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                    <div class="summary-card">
                        <div class="metric-value">{formatar_moeda(total_periodo)}</div>
                        <div class="metric-label">Total no período</div>
                    </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                    <div class="summary-card">
                        <div class="metric-value">{formatar_moeda(media_pagamento)}</div>
                        <div class="metric-label">Média por pagamento</div>
                    </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                    <div class="summary-card">
                        <div class="metric-value">{total_pagamentos}</div>
                        <div class="metric-label">Total de pagamentos</div>
                    </div>
                """, unsafe_allow_html=True)

            # Lista de pagamentos
            for _, pagamento in pagamentos.iterrows():
                data_pagamento = pagamento['dataPagamento'].strftime('%d/%m/%Y') if isinstance(pagamento['dataPagamento'], datetime) else pagamento['dataPagamento']
                
                payment_class = {
                    'Dinheiro': 'payment-dinheiro',
                    'PIX': 'payment-pix'
                }.get(pagamento['formaPagamento'], 'payment-cartao')

                st.markdown(f"""
                    <div class="custom-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <h3 style="margin: 0;">{pagamento['aluno']}</h3>
                                <p style="margin: 0; color: #666;">{pagamento['plano']}</p>
                            </div>
                            <div>
                                <span class="payment-badge {payment_class}">
                                    {pagamento['formaPagamento']}
                                </span>
                            </div>
                        </div>
                        <div style="margin-top: 1rem; display: flex; justify-content: space-between;">
                            <div>
                                <p>📅 Data: {data_pagamento}</p>
                            </div>
                            <div>
                                <p class="metric-value">{formatar_moeda(pagamento['valor'])}</p>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

        else:
            st.info("🔍 Nenhum pagamento encontrado para os filtros selecionados")

    with tabs[1]:
        st.markdown("""
            <div class="custom-card">
                <h3 style="color: #6C63FF;">➕ Registrar Pagamento</h3>
            </div>
        """, unsafe_allow_html=True)

        with st.form("novo_pagamento"):
            # Buscar matrículas ativas
            matriculas = buscar_dados("""
                SELECT 
                    m.codMatricula,
                    a.nome as aluno,
                    pl.nome as plano,
                    pl.valor,
                    DATE_FORMAT(m.dataFim, '%d/%m/%Y') as vencimento,
                    CONCAT(a.nome, ' - ', pl.nome, ' (Venc.: ', 
                           DATE_FORMAT(m.dataFim, '%d/%m/%Y'), 
                           ' - ', pl.valor, ')') as descricao
                FROM MATRICULA m
                JOIN ALUNO a ON m.CPF_aluno = a.CPF
                JOIN PLANO pl ON m.codPlano = pl.codPlano
                WHERE m.status = 'A'
                AND m.dataFim >= CURRENT_DATE
                ORDER BY a.nome
            """)

            if matriculas.empty:
                st.warning("Não há matrículas ativas para registrar pagamento")
                st.stop()

            # Seleção da matrícula
            matricula_selecionada = st.selectbox(
                "Matrícula",
                options=matriculas['descricao'].astype(str).tolist(),
                placeholder="Selecione a matrícula"
            )

            if matricula_selecionada:
                matricula_info = matriculas[
                    matriculas['descricao'] == matricula_selecionada
                ].iloc[0]
                
                st.markdown(f"""
                    <div class="info-box">
                        <h4>{matricula_info['aluno']}</h4>
                        <p>Plano: {matricula_info['plano']}</p>
                        <p>Vencimento: {matricula_info['vencimento']}</p>
                        <p class="preco-destaque">{formatar_moeda(float(matricula_info['valor']))}</p>
                    </div>
                """, unsafe_allow_html=True)

                col1, col2 = st.columns(2)
                with col1:
                    data_pagamento = st.date_input(
                        "Data do Pagamento",
                        value=datetime.now().date(),
                        max_value=datetime.now().date()
                    )
                
                with col2:
                    forma_pagamento = st.selectbox(
                        "Forma de Pagamento",
                        ["Dinheiro", "Cartão Débito", "Cartão Crédito", "PIX"]
                    )

                # Verificar pagamentos existentes
                pagamentos_existentes = buscar_dados("""
                    SELECT 
                        DATE_FORMAT(dataPagamento, '%d/%m/%Y') as data,
                        valor,
                        formaPagamento
                    FROM PAGAMENTO
                    WHERE codMatricula = %s
                    AND status = 'A'
                    ORDER BY dataPagamento DESC
                """, (int(matricula_info['codMatricula']),))

                if not pagamentos_existentes.empty:
                    st.markdown("""
                        <div style="margin: 1rem 0;">
                            <h4>Histórico de Pagamentos</h4>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    for _, pag in pagamentos_existentes.iterrows():
                        st.markdown(f"""
                            <div style="padding: 0.5rem; background: #f8f9fa; border-radius: 4px; margin-bottom: 0.5rem;">
                                📅 {pag['data']} - {formatar_moeda(pag['valor'])} ({pag['formaPagamento']})
                            </div>
                        """, unsafe_allow_html=True)

            if st.form_submit_button("💰 Confirmar Pagamento", use_container_width=True):
                if not matricula_selecionada:
                    st.error("Por favor, selecione uma matrícula!")
                else:
                    try:
                        # Verificar se já existe pagamento na mesma data
                        pagamento_existente = buscar_dados("""
                            SELECT 1 FROM PAGAMENTO
                            WHERE codMatricula = %s
                            AND DATE(dataPagamento) = %s
                            AND status = 'A'
                        """, (int(matricula_info['codMatricula']), data_pagamento))

                        if not pagamento_existente.empty:
                            st.error("Já existe um pagamento registrado nesta data!")
                            st.stop()

                        # Registrar pagamento
                        query_pagamento = """
                            INSERT INTO PAGAMENTO 
                            (codMatricula, dataPagamento, valor, formaPagamento, status)
                            VALUES (%s, %s, %s, %s, 'A')
                        """
                        executar_query(
                            query_pagamento,
                            (int(matricula_info['codMatricula']),
                             data_pagamento,
                             float(matricula_info['valor']),
                             forma_pagamento)
                        )

                        st.success(f"""
                            ✅ Pagamento registrado com sucesso!
                            
                            📝 Detalhes:
                            - Aluno: {matricula_info['aluno']}
                            - Plano: {matricula_info['plano']}
                            - Valor: {formatar_moeda(float(matricula_info['valor']))}
                            - Data: {data_pagamento.strftime('%d/%m/%Y')}
                            - Forma: {forma_pagamento}
                        """)
                        time.sleep(2)
                        st.rerun()

                    except Exception as e:
                        st.error(f"Erro ao registrar pagamento: {str(e)}")

        # Gráficos e estatísticas
        if not matriculas.empty:
            st.markdown("""
                <div style="margin-top: 2rem;">
                    <h3>📊 Estatísticas de Pagamentos</h3>
                </div>
            """, unsafe_allow_html=True)

            # Estatísticas gerais
            stats = buscar_dados("""
                SELECT 
                    COUNT(*) as total_pagamentos,
                    SUM(valor) as valor_total,
                    AVG(valor) as valor_medio,
                    formaPagamento
                FROM PAGAMENTO
                WHERE status = 'A'
                AND dataPagamento >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)
                GROUP BY formaPagamento
            """)

            if not stats.empty:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Gráfico de pizza por forma de pagamento
                    dados_pizza = {
                        'Forma': stats['formaPagamento'],
                        'Valor': stats['valor_total']
                    }
                    st.write("Distribuição por Forma de Pagamento (Últimos 30 dias)")
                    st.bar_chart(dados_pizza, x='Forma')

                with col2:
                    # Tabela de resumo
                    st.write("Resumo por Forma de Pagamento")
                    resumo = pd.DataFrame({
                        'Forma': stats['formaPagamento'],
                        'Total de Pagamentos': stats['total_pagamentos'],
                        'Valor Total': stats['valor_total'].apply(formatar_moeda),
                        'Valor Médio': stats['valor_medio'].apply(formatar_moeda)
                    })
                    st.dataframe(resumo, hide_index=True)

if __name__ == "__main__":
    mostrar_pagina()