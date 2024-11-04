-- 1. View para informações completas dos alunos ativos com seus planos
CREATE VIEW vw_alunos_ativos AS
SELECT 
    a.id_aluno,
    a.nome,
    a.email,
    a.telefone,
    m.id_matricula,
    p.nome as plano,
    m.data_inicio,
    m.data_fim,
    m.status as status_matricula,
    CASE 
        WHEN m.data_fim < CURDATE() THEN 'Vencida'
        WHEN m.data_fim = CURDATE() THEN 'Vence hoje'
        ELSE 'Em dia'
    END as situacao
FROM Aluno a
INNER JOIN Matricula m ON a.id_aluno = m.id_aluno
INNER JOIN Plano p ON m.id_plano = p.id_plano
WHERE a.status = 'ativo';

-- 2. View para relatório de frequência mensal dos alunos
CREATE VIEW vw_frequencia_mensal AS
SELECT 
    a.id_aluno,
    a.nome,
    DATE_FORMAT(p.data, '%Y-%m') as mes,
    COUNT(*) as dias_presentes,
    SEC_TO_TIME(AVG(TIME_TO_SEC(TIMEDIFF(p.hora_saida, p.hora_entrada)))) as tempo_medio
FROM Aluno a
INNER JOIN Presenca p ON a.id_aluno = p.id_aluno
GROUP BY a.id_aluno, a.nome, DATE_FORMAT(p.data, '%Y-%m')
ORDER BY mes DESC, nome;

-- 3. View para análise de evolução física dos alunos
CREATE VIEW vw_evolucao_fisica AS
SELECT 
    a.id_aluno,
    a.nome,
    af.data_avaliacao,
    af.peso,
    af.altura,
    af.imc,
    af.percentual_gordura,
    LAG(af.peso) OVER (PARTITION BY a.id_aluno ORDER BY af.data_avaliacao) as peso_anterior,
    ROUND(af.peso - LAG(af.peso) OVER (PARTITION BY a.id_aluno ORDER BY af.data_avaliacao), 2) as variacao_peso
FROM Aluno a
INNER JOIN Avaliacao_Fisica af ON a.id_aluno = af.id_aluno
ORDER BY a.nome, af.data_avaliacao;

-- 4. View para relatório financeiro de mensalidades
CREATE VIEW vw_relatorio_financeiro AS
SELECT 
    DATE_FORMAT(p.data_pagamento, '%Y-%m') as mes,
    COUNT(DISTINCT p.id_pagamento) as total_pagamentos,
    SUM(p.valor) as valor_total,
    AVG(p.valor) as ticket_medio,
    COUNT(CASE WHEN p.status = 'confirmado' THEN 1 END) as pagamentos_confirmados,
    COUNT(CASE WHEN p.status = 'pendente' THEN 1 END) as pagamentos_pendentes
FROM Pagamento p
GROUP BY DATE_FORMAT(p.data_pagamento, '%Y-%m')
ORDER BY mes DESC;

-- 5. View para análise de vendas de produtos
CREATE VIEW vw_analise_vendas AS
SELECT 
    p.categoria,
    p.nome as produto,
    COUNT(iv.id_item) as quantidade_vendida,
    SUM(iv.quantidade) as unidades_vendidas,
    SUM(iv.subtotal) as valor_total,
    AVG(iv.valor_unitario) as preco_medio
FROM Produto p
LEFT JOIN Item_Venda iv ON p.id_produto = iv.id_produto
LEFT JOIN Venda v ON iv.id_venda = v.id_venda
WHERE v.status = 'finalizada'
GROUP BY p.categoria, p.nome
ORDER BY valor_total DESC;

-- Consultas úteis para o sistema

-- 1. Consulta para verificar alunos com matrículas a vencer nos próximos 30 dias
SELECT 
    a.nome,
    a.email,
    a.telefone,
    m.data_fim,
    DATEDIFF(m.data_fim, CURDATE()) as dias_restantes,
    p.nome as plano
FROM Aluno a
INNER JOIN Matricula m ON a.id_aluno = m.id_aluno
INNER JOIN Plano p ON m.id_plano = p.id_plano
WHERE 
    m.status = 'ativa' 
    AND m.data_fim BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY)
ORDER BY m.data_fim;

-- 2. Consulta para verificar treinos que precisam ser atualizados
SELECT 
    a.nome as aluno,
    f.nome as instrutor,
    t.data_criacao,
    t.data_validade,
    DATEDIFF(t.data_validade, CURDATE()) as dias_para_vencer
FROM Treino t
INNER JOIN Aluno a ON t.id_aluno = a.id_aluno
INNER JOIN Funcionario f ON t.id_funcionario = f.id_funcionario
WHERE 
    t.status = 'ativo'
    AND t.data_validade BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 15 DAY)
ORDER BY t.data_validade;

-- 3. Consulta para analisar frequência dos alunos na última semana
SELECT 
    a.nome,
    COUNT(p.id_presenca) as dias_presentes,
    GROUP_CONCAT(DISTINCT DATE_FORMAT(p.data, '%d/%m/%Y') ORDER BY p.data) as dias
FROM Aluno a
LEFT JOIN Presenca p ON a.id_aluno = p.id_aluno
WHERE 
    p.data BETWEEN DATE_SUB(CURDATE(), INTERVAL 7 DAY) AND CURDATE()
    AND a.status = 'ativo'
GROUP BY a.id_aluno, a.nome
ORDER BY dias_presentes DESC;

-- 4. Consulta para relatório de desempenho dos funcionários (vendas e alunos atendidos)
SELECT 
    f.nome,
    f.cargo,
    COUNT(DISTINCT t.id_aluno) as alunos_atendidos,
    COUNT(DISTINCT v.id_venda) as vendas_realizadas,
    COALESCE(SUM(v.valor_total), 0) as valor_total_vendas
FROM Funcionario f
LEFT JOIN Treino t ON f.id_funcionario = t.id_funcionario
LEFT JOIN Venda v ON f.id_funcionario = v.id_funcionario
WHERE f.status = 'ativo'
GROUP BY f.id_funcionario, f.nome, f.cargo
ORDER BY alunos_atendidos DESC;

-- 5. Consulta para análise de exercícios mais utilizados nos treinos
SELECT 
    e.nome as exercicio,
    e.grupo_muscular,
    COUNT(ft.id_ficha) as total_utilizacoes,
    AVG(ft.series) as media_series,
    AVG(ft.repeticoes) as media_repeticoes,
    AVG(ft.carga) as media_carga
FROM Exercicio e
LEFT JOIN Ficha_Treino ft ON e.id_exercicio = ft.id_exercicio
GROUP BY e.id_exercicio, e.nome, e.grupo_muscular
ORDER BY total_utilizacoes DESC;

-- 6. Consulta para verificar produtos com estoque baixo
SELECT 
    nome,
    categoria,
    estoque,
    preco_venda,
    CASE 
        WHEN estoque = 0 THEN 'Esgotado'
        WHEN estoque < 10 THEN 'Crítico'
        WHEN estoque < 20 THEN 'Baixo'
        ELSE 'Normal'
    END as situacao_estoque
FROM Produto
WHERE estoque < 20
ORDER BY estoque;

-- 7. Procedure para gerar relatório de inadimplência
DELIMITER //
CREATE PROCEDURE sp_relatorio_inadimplencia()
BEGIN
    SELECT 
        a.nome,
        a.email,
        a.telefone,
        m.data_fim,
        p.valor as valor_plano,
        DATEDIFF(CURDATE(), m.data_fim) as dias_atraso
    FROM Aluno a
    INNER JOIN Matricula m ON a.id_aluno = m.id_aluno
    INNER JOIN Plano p ON m.id_plano = p.id_plano
    LEFT JOIN Pagamento pag ON m.id_matricula = pag.id_matricula
    WHERE 
        m.data_fim < CURDATE()
        AND (pag.status = 'pendente' OR pag.status IS NULL)
    ORDER BY dias_atraso DESC;
END //
DELIMITER ;

-- 8. Procedure para atualizar status das matrículas
DELIMITER //
CREATE PROCEDURE sp_atualizar_status_matriculas()
BEGIN
    UPDATE Matricula
    SET status = 'vencida'
    WHERE 
        data_fim < CURDATE()
        AND status = 'ativa';
        
    UPDATE Matricula
    SET status = 'ativa'
    WHERE 
        data_fim >= CURDATE()
        AND status = 'pendente'
        AND id_matricula IN (
            SELECT id_matricula 
            FROM Pagamento 
            WHERE status = 'confirmado'
        );
END //
DELIMITER ;

-- 9. Trigger para atualizar estoque após venda
DELIMITER //
CREATE TRIGGER trg_atualiza_estoque AFTER INSERT ON Item_Venda
FOR EACH ROW
BEGIN
    UPDATE Produto
    SET estoque = estoque - NEW.quantidade
    WHERE id_produto = NEW.id_produto;
END //
DELIMITER ;

-- 10. Trigger para calcular IMC automaticamente
DELIMITER //
CREATE TRIGGER trg_calcula_imc BEFORE INSERT ON Avaliacao_Fisica
FOR EACH ROW
BEGIN
    SET NEW.imc = ROUND(NEW.peso / (NEW.altura * NEW.altura), 2);
END //
DELIMITER ;
