import streamlit as st

def mostrar_pagina():
    # CSS personalizado para a página inicial
    st.markdown("""
        <style>
        .hero-section {
            text-align: center;
            padding: 4rem 2rem;
            background: linear-gradient(135deg, #6C63FF 0%, #4CAF50 100%);
            border-radius: 20px;
            color: white;
            margin-bottom: 2rem;
        }
        .feature-card {
            background: white;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05);
            margin: 1rem 0;
            transition: all 0.3s ease;
            text-align: center;
            height: 100%;
        }
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 25px rgba(0,0,0,0.1);
        }
        .feature-icon {
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }
        .stats-card {
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            margin: 0.5rem;
            transition: all 0.3s ease;
        }
        .stats-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .stats-value {
            font-size: 2.5rem;
            font-weight: bold;
            background: linear-gradient(135deg, #6C63FF 0%, #4CAF50 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0.5rem 0;
        }
        .stats-label {
            color: #666;
            font-size: 1.1rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # Hero Section
    st.markdown("""
        <div class="hero-section">
            <h1 style="font-size: 3.5rem; margin-bottom: 1rem;">💪 Academia Fitness</h1>
            <p style="font-size: 1.4rem; margin-bottom: 2rem;">
                Transformando vidas através da saúde e do bem-estar
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Features Section
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">🏋️‍♂️</div>
                <h3>Equipamentos Premium</h3>
                <p>Aparelhos de última geração para maximizar seus resultados</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">👥</div>
                <h3>Professores Especializados</h3>
                <p>Equipe com formação superior e especializações</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">📱</div>
                <h3>Sistema Integrado</h3>
                <p>Gestão digital completa para melhor atendê-lo</p>
            </div>
        """, unsafe_allow_html=True)

    # Stats Section
    st.markdown("<h2 style='text-align: center; margin: 3rem 0;'>Nossos Números</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class="stats-card">
                <div class="stats-value">500+</div>
                <div class="stats-label">Alunos Ativos</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="stats-card">
                <div class="stats-value">20+</div>
                <div class="stats-label">Modalidades</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="stats-card">
                <div class="stats-value">30+</div>
                <div class="stats-label">Professores</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div class="stats-card">
                <div class="stats-value">98%</div>
                <div class="stats-label">Satisfação</div>
            </div>
        """, unsafe_allow_html=True)

    # Horários
    st.markdown("<h2 style='text-align: center; margin: 3rem 0;'>Horário de Funcionamento</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="feature-card">
                <h3>Segunda a Sexta</h3>
                <p style="font-size: 1.4rem; color: #6C63FF;">06:00 - 22:00</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="feature-card">
                <h3>Sábados</h3>
                <p style="font-size: 1.4rem; color: #6C63FF;">08:00 - 18:00</p>
            </div>
        """, unsafe_allow_html=True)