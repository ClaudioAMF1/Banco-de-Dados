import streamlit as st
from src.paginas import (
    alunos, 
    aulas, 
    matriculas, 
    pagamentos,  
    modalidades, 
    professores, 
    relatorios,
    views,
    home
)
from src.database.conexao import iniciar_conexao

# Configuração da página
st.set_page_config(
    page_title="Academia Fitness",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Verificar conexão apenas na primeira execução
if 'sistema_iniciado' not in st.session_state:
    conexao = iniciar_conexao()
    if conexao:
        st.session_state['sistema_iniciado'] = True
        conexao.close()
    else:
        st.error("❌ Erro ao conectar ao banco de dados")
        st.stop()

# Função de Login
def login():
    st.markdown("""
        <style>
        .login-container {
            max-width: 400px;
            margin: 2rem auto;
            padding: 2rem;
            background: white;
            border-radius: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }
        .login-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        .login-header h1 {
            color: #2C3E50;
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }
        .login-header p {
            color: #666;
            font-size: 1.1rem;
        }
        .login-form {
            margin-top: 2rem;
        }
        .login-form input {
            width: 100%;
            padding: 0.75rem 1rem;
            margin-bottom: 1rem;
            border: 1px solid #ddd;
            border-radius: 10px;
            font-size: 1rem;
        }
        .login-button {
            background: linear-gradient(135deg, #6C63FF 0%, #4CAF50 100%);
            color: white;
            padding: 0.75rem;
            border: none;
            border-radius: 10px;
            width: 100%;
            font-size: 1.1rem;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .login-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .login-footer {
            text-align: center;
            margin-top: 2rem;
            color: #666;
            font-size: 0.9rem;
        }
        .hero-gradient {
            background: linear-gradient(135deg, #6C63FF 0%, #4CAF50 100%);
            padding: 4rem 2rem;
            text-align: center;
            color: white;
            border-radius: 20px;
            margin-bottom: 2rem;
        }
        .hero-title {
            font-size: 3rem;
            font-weight: bold;
            margin-bottom: 1rem;
        }
        .hero-subtitle {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        .error-message {
            background-color: #FFF5F5;
            color: #DC2626;
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            margin: 1rem 0;
            border: 1px solid #FCA5A5;
        }
        .stButton button {
            background: linear-gradient(135deg, #6C63FF 0%, #4CAF50 100%);
            color: white;
            font-weight: bold;
            border-radius: 10px;
            padding: 0.75rem 2rem;
            border: none;
            transition: all 0.3s ease;
        }
        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        </style>
    """, unsafe_allow_html=True)

    # Hero Section
    st.markdown("""
        <div class="hero-gradient">
            <div class="hero-title">🏋️‍♂️ Academia Fitness</div>
            <div class="hero-subtitle">Sistema de Gestão</div>
        </div>
    """, unsafe_allow_html=True)

    # Login Container
    st.markdown("""
        <div class="login-container">
            <div class="login-header">
                <h1>👋 Bem-vindo</h1>
                <p>Faça login para continuar</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Login Form
    with st.form("login_form"):
        username = st.text_input("Usuário", placeholder="Digite seu usuário")
        password = st.text_input("Senha", type="password", placeholder="Digite sua senha")
        
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            submitted = st.form_submit_button("ENTRAR", use_container_width=True)
            if submitted:
                if username == "admin" and password == "admin":
                    st.session_state['authenticated'] = True
                    st.session_state['username'] = username
                    st.rerun()
                else:
                    st.markdown("""
                        <div class="error-message">
                            ❌ Usuário ou senha incorretos!
                        </div>
                    """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
        <div class="login-footer">
            <p>© 2024 Academia Fitness. Todos os direitos reservados.</p>
            <p style="margin-top: 0.5rem;">
                Desenvolvido com ❤️ por Claudio Meireles
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Features
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div style="text-align: center; padding: 1rem;">
                <h3 style="color: #2C3E50;">🔒 Seguro</h3>
                <p style="color: #666;">Sistema protegido e confiável</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style="text-align: center; padding: 1rem;">
                <h3 style="color: #2C3E50;">⚡ Rápido</h3>
                <p style="color: #666;">Acesso instantâneo aos dados</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div style="text-align: center; padding: 1rem;">
                <h3 style="color: #2C3E50;">📱 Responsivo</h3>
                <p style="color: #666;">Acesse de qualquer dispositivo</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Estilo CSS personalizado
st.markdown("""
    <style>
        /* Layout Geral */
        .main {
            padding: 2rem;
        }
        
        /* Cards */
        .stButton button {
            width: 100%;
            border-radius: 20px;
            padding: 0.5rem 1rem;
            transition: all 0.3s ease;
        }
        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        /* Campos de Seleção */
        .stSelectbox {
            margin-bottom: 1rem;
        }
        .stSelectbox > div > div {
            border-radius: 8px;
        }
        
        /* Header */
        .stHeader {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 2rem;
        }
        
        /* Sidebar */
        .sidebar .decoration {
            padding: 1rem;
            margin-top: 2rem;
            border-top: 1px solid rgba(255,255,255,0.1);
        }
        
        /* Métricas e Cards */
        .metric-card {
            background-color: #ffffff;
            padding: 1.5rem;
            border-radius: 1rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            margin-bottom: 1rem;
            transition: all 0.3s ease;
        }
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.12);
        }
        
        /* Feedback Messages */
        .stSuccess {
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        }
        .stError {
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        }
        
        /* Forms */
        .stForm {
            background: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.05);
        }
        
        /* Tables */
        .stDataFrame {
            border-radius: 8px;
            overflow: hidden;
        }
        .stDataFrame table {
            border-collapse: separate;
            border-spacing: 0;
        }
        
        /* Navigation */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
            margin-bottom: 1rem;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 1rem 2rem;
            font-weight: 500;
        }

        /* User Info */
        .user-info {
            background: rgba(255,255,255,0.1);
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
        }
        
        /* Logout Button */
        .logout-button {
            background: rgba(255,255,255,0.1);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 10px;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
            border: 1px solid rgba(255,255,255,0.2);
        }
        .logout-button:hover {
            background: rgba(255,255,255,0.2);
        }
    </style>
""", unsafe_allow_html=True)

# Verificar autenticação
if 'authenticated' not in st.session_state:
    login()
else:
    # Menu lateral
    with st.sidebar:
        st.title("Menu Principal")
        
        # Menu de navegação
        pagina = st.selectbox(
            "Selecione a Página",
            [
                "Home",
                "Alunos",
                "Professores",
                "Modalidades",
                "Aulas",
                "Matrículas",
                "Pagamentos",
                "Views",
                "Relatórios"
            ]
        )
        
        st.markdown("---")
        
        # Informações do usuário
        st.markdown(f"""
            <div class="user-info">
                <p style="margin:0">👤 Usuário: {st.session_state['username']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Botão de Logout estilizado
        if st.button("🚪 Sair", key="logout"):
            del st.session_state['authenticated']
            del st.session_state['username']
            st.rerun()
        
        # Informações do sistema
        with st.expander("ℹ️ Informações do Sistema"):
            st.markdown("""
                - **Versão**: 1.0.0
                - **Desenvolvido por**: Claudio Meireles
                - **Contato**: cmeireles756@gmail.com
            """)

    # Título principal e breadcrumb (apenas se não estiver na Home)
    if pagina != "Home":
        st.title("Sistema de Gestão - Academia")
        st.markdown(f"""
            <div style='color: #666; margin-bottom: 1rem;'>
                🏠 Home / {pagina}
            </div>
        """, unsafe_allow_html=True)

    # Roteamento de páginas
    try:
        if pagina == "Home":
            home.mostrar_pagina()
        elif pagina == "Alunos":
            alunos.mostrar_pagina()
        elif pagina == "Professores":
            professores.mostrar_pagina()
        elif pagina == "Modalidades":
            modalidades.mostrar_pagina()
        elif pagina == "Aulas":
            aulas.mostrar_pagina()
        elif pagina == "Matrículas":
            matriculas.mostrar_pagina()
        elif pagina == "Pagamentos":
            pagamentos.mostrar_pagina()
        elif pagina == "Views":
            views.mostrar_pagina()
        elif pagina == "Relatórios":
            relatorios.mostrar_pagina()
    except Exception as e:
        st.error(f"""
            ❌ Erro ao carregar a página: {str(e)}
            
            Por favor, tente novamente ou contate o suporte.
        """)

    # Rodapé
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
        <div class='decoration'>
            <p style='text-align: center; color: rgba(255,255,255,0.5);'>
                Academia Fitness © 2024<br>
                Todos os direitos reservados
            </p>
        </div>
    """, unsafe_allow_html=True)