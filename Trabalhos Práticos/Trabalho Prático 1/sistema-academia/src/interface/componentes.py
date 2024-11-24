import streamlit as st

class Card:
    @staticmethod
    def info(titulo, valor, descricao=None):
        st.markdown(f"""
            <div class="metric-card">
                <h3>{titulo}</h3>
                <h2>{valor}</h2>
                {f'<p>{descricao}</p>' if descricao else ''}
            </div>
        """, unsafe_allow_html=True)

class Tabela:
    @staticmethod
    def com_acoes(df, acoes, key_col):
        for index, row in df.iterrows():
            col1, *data_cols, col2 = st.columns([1] + [2]*len(df.columns) + [1])
            
            with col1:
                st.write(f"#{index+1}")
            
            for i, col in enumerate(df.columns):
                with data_cols[i]:
                    st.write(row[col])
            
            with col2:
                for acao, func in acoes.items():
                    if st.button(acao, key=f"{acao}_{row[key_col]}"):
                        func(row[key_col])

class Form:
    @staticmethod
    def confirmar_acao(titulo, mensagem, acao_confirmacao):
        with st.form(f"confirmar_{titulo.lower()}"):
            st.write(f"### {titulo}")
            st.write(mensagem)
            
            if st.form_submit_button("Confirmar"):
                acao_confirmacao()

class Dashboard:
    @staticmethod
    def mostrar_metricas(metricas):
        cols = st.columns(len(metricas))
        for col, (titulo, valor, descricao) in zip(cols, metricas):
            with col:
                Card.info(titulo, valor, descricao)