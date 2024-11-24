import streamlit as st

NIVEIS_ACESSO = {
    'ADMIN': ['todas'],
    'PROFESSOR': ['alunos', 'aulas', 'avaliacoes'],
    'RECEPCIONISTA': ['alunos', 'matriculas', 'pagamentos'],
}

def verificar_permissao(nivel, pagina):
    if nivel == 'ADMIN':
        return True
    return pagina.lower() in NIVEIS_ACESSO.get(nivel, [])

def requer_permissao(nivel_requerido):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not st.session_state.get('authenticated'):
                st.error("Faça login para continuar")
                return
            
            nivel_usuario = st.session_state['user'].get('nivel')
            if nivel_usuario == 'ADMIN' or nivel_usuario == nivel_requerido:
                return func(*args, **kwargs)
            else:
                st.error("Você não tem permissão para acessar esta página")
        return wrapper
    return decorator

def criar_menu_dinamico():
    nivel = st.session_state['user'].get('nivel')
    
    menu_items = {
        'ADMIN': [
            "Alunos", "Professores", "Aulas", "Matrículas", 
            "Pagamentos", "Modalidades", "Avaliações", "Relatórios", "Usuários"
        ],
        'PROFESSOR': ["Alunos", "Aulas", "Avaliações"],
        'RECEPCIONISTA': ["Alunos", "Matrículas", "Pagamentos"]
    }
    
    return st.sidebar.selectbox(
        "Selecione a Página",
        menu_items.get(nivel, [])
    )