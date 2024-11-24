from datetime import datetime, timedelta
from src.database.conexao import buscar_dados

def validar_conflito_horario(aluno_cpf, turma_id):
    """Verifica se há conflito de horário para o aluno"""
    query = """
        SELECT t1.diaSemana, t1.horario
        FROM TURMA t1
        JOIN ALUNO_TURMA at1 ON t1.codTurma = at1.codTurma
        WHERE at1.CPF_aluno = %s AND at1.status = 'A'
        AND EXISTS (
            SELECT 1 FROM TURMA t2
            WHERE t2.codTurma = %s
            AND t2.diaSemana = t1.diaSemana
            AND ABS(TIME_TO_SEC(TIMEDIFF(t2.horario, t1.horario))) < 3600
        )
    """
    conflitos = buscar_dados(query, (aluno_cpf, turma_id))
    return not conflitos.empty

def validar_capacidade_turma(turma_id):
    """Verifica se a turma ainda tem vagas"""
    query = """
        SELECT t.capacidade, COUNT(at.codAluno_Turma) as inscritos
        FROM TURMA t
        LEFT JOIN ALUNO_TURMA at ON t.codTurma = at.codTurma AND at.status = 'A'
        WHERE t.codTurma = %s
        GROUP BY t.codTurma, t.capacidade
    """
    capacidade = buscar_dados(query, (turma_id,))
    if not capacidade.empty:
        return int(capacidade['inscritos'].iloc[0]) < int(capacidade['capacidade'].iloc[0])
    return False

def validar_matricula_ativa(aluno_cpf):
    """Verifica se o aluno tem matrícula ativa"""
    query = """
        SELECT 1 FROM MATRICULA
        WHERE CPF_aluno = %s
        AND status = 'A'
        AND dataFim >= CURRENT_DATE
    """
    matricula = buscar_dados(query, (aluno_cpf,))
    return not matricula.empty

def validar_pagamento_pendente(matricula_id):
    """Verifica se há pagamento pendente"""
    query = """
        SELECT 1 FROM PAGAMENTO
        WHERE codMatricula = %s
        AND status = 'A'
        AND dataPagamento >= CURRENT_DATE - INTERVAL 30 DAY
    """
    pagamento = buscar_dados(query, (matricula_id,))
    return not pagamento.empty