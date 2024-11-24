import streamlit as st
from src.database.conexao import executar_query, buscar_dados

def criar_views():
    """Cria todas as views do sistema"""
    
    # View de Alunos Ativos com seus Planos
    executar_query("""
        CREATE OR REPLACE VIEW vw_alunos_ativos AS
        SELECT 
            a.CPF,
            a.nome AS nome_aluno,
            a.telefone,
            m.dataInicio,
            m.dataFim,
            p.nome AS nome_plano,
            p.valor
        FROM ALUNO a
        INNER JOIN MATRICULA m ON a.CPF = m.CPF_aluno
        INNER JOIN PLANO p ON m.codPlano = p.codPlano
        WHERE a.status = 'A' AND m.status = 'A'
    """)

    # View de Turmas com Professores
    executar_query("""
        CREATE OR REPLACE VIEW vw_turmas_detalhes AS
        SELECT 
            t.codTurma,
            m.nome AS modalidade,
            p.nome AS professor,
            t.horario,
            t.diaSemana,
            t.capacidade,
            COUNT(at.CPF_aluno) AS alunos_matriculados
        FROM TURMA t
        INNER JOIN MODALIDADE m ON t.codModalidade = m.codModalidade
        INNER JOIN PROFESSOR p ON t.CPF_professor = p.CPF
        LEFT JOIN ALUNO_TURMA at ON t.codTurma = at.codTurma
        WHERE t.status = 'A'
        GROUP BY t.codTurma
    """)

def consultas_relatorios():
    """Implementa as consultas principais para relatórios"""
    
    # Relatório de Inadimplência
    def get_inadimplentes():
        return buscar_dados("""
            SELECT 
                a.nome AS aluno,
                a.telefone,
                m.dataFim AS vencimento,
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
        """)

    # Relatório de Ocupação das Turmas
    def get_ocupacao_turmas():
        return buscar_dados("""
            SELECT 
                m.nome AS modalidade,
                t.diaSemana,
                t.horario,
                p.nome AS professor,
                t.capacidade AS vagas_totais,
                COUNT(at.CPF_aluno) AS vagas_ocupadas,
                (t.capacidade - COUNT(at.CPF_aluno)) AS vagas_disponiveis
            FROM TURMA t
            INNER JOIN MODALIDADE m ON t.codModalidade = m.codModalidade
            INNER JOIN PROFESSOR p ON t.CPF_professor = p.CPF
            LEFT JOIN ALUNO_TURMA at ON t.codTurma = at.codTurma
            WHERE t.status = 'A'
            GROUP BY t.codTurma
            ORDER BY m.nome, t.diaSemana, t.horario
        """)

    # Busca de Alunos por Modalidade
    def get_alunos_por_modalidade():
        return buscar_dados("""
            SELECT 
                m.nome AS modalidade,
                a.nome AS aluno,
                a.telefone,
                at.dataInscricao
            FROM ALUNO_TURMA at
            INNER JOIN TURMA t ON at.codTurma = t.codTurma
            INNER JOIN MODALIDADE m ON t.codModalidade = m.codModalidade
            INNER JOIN ALUNO a ON at.CPF_aluno = a.CPF
            WHERE at.status = 'A'
            ORDER BY m.nome, a.nome
        """)

    # Faturamento por Período e Forma de Pagamento
    def get_faturamento(periodo_inicio=None, periodo_fim=None):
        query = """
            SELECT 
                DATE_FORMAT(dataPagamento, '%Y-%m') AS mes,
                formaPagamento,
                COUNT(*) AS quantidade,
                SUM(valor) AS total
            FROM PAGAMENTO
            WHERE status = 'A'
        """
        
        params = []
        if periodo_inicio and periodo_fim:
            query += " AND dataPagamento BETWEEN %s AND %s"
            params.extend([periodo_inicio, periodo_fim])
            
        query += " GROUP BY DATE_FORMAT(dataPagamento, '%Y-%m'), formaPagamento ORDER BY mes, formaPagamento"
        
        return buscar_dados(query, tuple(params))

    # Evolução das Avaliações Físicas
    def get_evolucao_avaliacoes():
        return buscar_dados("""
            SELECT 
                a.nome AS aluno,
                av.data,
                av.peso,
                av.altura,
                av.percentualGordura,
                p.nome AS professor
            FROM AVALIACAO av
            INNER JOIN ALUNO a ON av.CPF_aluno = a.CPF
            INNER JOIN PROFESSOR p ON av.CPF_professor = p.CPF
            ORDER BY a.nome, av.data
        """)

    # Histórico de Frequência nas Modalidades
    def get_frequencia_modalidades():
        return buscar_dados("""
            SELECT 
                a.nome AS aluno,
                m.nome AS modalidade,
                COUNT(at.codAluno_Turma) AS total_frequencia
            FROM ALUNO a
            INNER JOIN ALUNO_TURMA at ON a.CPF = at.CPF_aluno
            INNER JOIN TURMA t ON at.codTurma = t.codTurma
            INNER JOIN MODALIDADE m ON t.codModalidade = m.codModalidade
            WHERE at.status = 'A'
            GROUP BY a.CPF, m.codModalidade
            ORDER BY a.nome, m.nome
        """)

    # Análise de Desempenho dos Professores
    def get_desempenho_professores():
        return buscar_dados("""
            SELECT 
                p.nome AS professor,
                m.nome AS modalidade,
                COUNT(DISTINCT at.CPF_aluno) AS total_alunos,
                COUNT(DISTINCT t.codTurma) AS total_turmas
            FROM PROFESSOR p
            INNER JOIN TURMA t ON p.CPF = t.CPF_professor
            INNER JOIN MODALIDADE m ON t.codModalidade = m.codModalidade
            LEFT JOIN ALUNO_TURMA at ON t.codTurma = at.codTurma
            WHERE t.status = 'A'
            GROUP BY p.CPF, m.codModalidade
        """)

    # Análise de Renovações de Matrícula
    def get_renovacoes_matricula():
        return buscar_dados("""
            SELECT 
                a.nome AS aluno,
                p.nome AS plano,
                COUNT(*) AS total_renovacoes,
                MAX(m.dataInicio) AS ultima_matricula
            FROM ALUNO a
            INNER JOIN MATRICULA m ON a.CPF = m.CPF_aluno
            INNER JOIN PLANO p ON m.codPlano = p.codPlano
            GROUP BY a.CPF, p.codPlano
            HAVING COUNT(*) > 1
            ORDER BY total_renovacoes DESC
        """)

    # Análise de Ocupação da Academia por Horário
    def get_ocupacao_horarios():
        return buscar_dados("""
            SELECT 
                t.diaSemana,
                t.horario,
                COUNT(DISTINCT t.codTurma) as total_turmas,
                SUM(t.capacidade) as capacidade_total,
                COUNT(DISTINCT at.CPF_aluno) as total_alunos,
                ROUND((COUNT(DISTINCT at.CPF_aluno) / SUM(t.capacidade)) * 100, 2) as taxa_ocupacao
            FROM TURMA t
            LEFT JOIN ALUNO_TURMA at ON t.codTurma = at.codTurma
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

    return {
        'inadimplentes': get_inadimplentes,
        'ocupacao_turmas': get_ocupacao_turmas,
        'alunos_por_modalidade': get_alunos_por_modalidade,
        'faturamento': get_faturamento,
        'evolucao_avaliacoes': get_evolucao_avaliacoes,
        'frequencia_modalidades': get_frequencia_modalidades,
        'desempenho_professores': get_desempenho_professores,
        'renovacoes_matricula': get_renovacoes_matricula,
        'ocupacao_horarios': get_ocupacao_horarios
    }

criar_views()

consultas = consultas_relatorios()