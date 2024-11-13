/* Criação do Banco de Dados */
CREATE DATABASE academia;

/* Seleciona o Banco de Dados */
USE academia;

/* Tabela ENDERECO */
CREATE TABLE ENDERECO (
   codEndereco INT AUTO_INCREMENT,
   rua VARCHAR(100) NOT NULL,
   numero VARCHAR(10) NOT NULL,
   complemento VARCHAR(50),
   bairro VARCHAR(50) NOT NULL,
   cidade VARCHAR(50) NOT NULL,
   estado CHAR(2) NOT NULL,
   CEP CHAR(8) NOT NULL,
   CONSTRAINT pk_endereco PRIMARY KEY (codEndereco),
   CONSTRAINT chk_cep CHECK (CEP REGEXP '^[0-9]{8}$'),
   CONSTRAINT chk_estado CHECK (estado REGEXP '^[A-Z]{2}$')
) COMMENT 'Tabela de endereços dos alunos';

/* Tabela ALUNO */
CREATE TABLE ALUNO (
   CPF CHAR(11),
   nome VARCHAR(100) NOT NULL,
   email VARCHAR(100),
   telefone CHAR(11),
   codEndereco INT,
   status CHAR(1) DEFAULT 'A',
   CONSTRAINT pk_aluno PRIMARY KEY (CPF),
   CONSTRAINT fk_aluno_endereco FOREIGN KEY (codEndereco) 
       REFERENCES ENDERECO (codEndereco)
       ON DELETE RESTRICT
       ON UPDATE CASCADE,
   CONSTRAINT chk_cpf_aluno CHECK (CPF REGEXP '^[0-9]{11}$'),
   CONSTRAINT chk_email CHECK (email REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
   CONSTRAINT chk_telefone CHECK (telefone REGEXP '^[0-9]{11}$'),
   CONSTRAINT chk_status_aluno CHECK (status IN ('A','I'))
) COMMENT 'Tabela de cadastro de alunos';

/* Tabela PROFESSOR */
CREATE TABLE PROFESSOR (
   CPF CHAR(11),
   nome VARCHAR(100) NOT NULL,
   telefone CHAR(11),
   especializacao VARCHAR(100),
   salario DECIMAL(10,2),
   status CHAR(1) DEFAULT 'A',
   CONSTRAINT pk_professor PRIMARY KEY (CPF),
   CONSTRAINT chk_cpf_professor CHECK (CPF REGEXP '^[0-9]{11}$'),
   CONSTRAINT chk_telefone_prof CHECK (telefone REGEXP '^[0-9]{11}$'),
   CONSTRAINT chk_salario CHECK (salario > 0),
   CONSTRAINT chk_status_professor CHECK (status IN ('A','I'))
) COMMENT 'Tabela de cadastro de professores';

/* Tabela MODALIDADE */
CREATE TABLE MODALIDADE (
   codModalidade INT AUTO_INCREMENT,
   nome VARCHAR(50) NOT NULL,
   descricao VARCHAR(200),
   requisitos VARCHAR(200),
   status CHAR(1) DEFAULT 'A',
   CONSTRAINT pk_modalidade PRIMARY KEY (codModalidade),
   CONSTRAINT chk_status_modalidade CHECK (status IN ('A','I'))
) COMMENT 'Tabela de modalidades de aulas';

/* Tabela TURMA */
CREATE TABLE TURMA (
   codTurma INT AUTO_INCREMENT,
   codModalidade INT NOT NULL,
   CPF_professor CHAR(11) NOT NULL,
   horario TIME NOT NULL,
   diaSemana ENUM('Segunda','Terça','Quarta','Quinta','Sexta','Sábado','Domingo') NOT NULL,
   capacidade INT NOT NULL,
   status CHAR(1) DEFAULT 'A',
   CONSTRAINT pk_turma PRIMARY KEY (codTurma),
   CONSTRAINT fk_turma_modalidade FOREIGN KEY (codModalidade) 
       REFERENCES MODALIDADE (codModalidade)
       ON DELETE RESTRICT
       ON UPDATE CASCADE,
   CONSTRAINT fk_turma_professor FOREIGN KEY (CPF_professor) 
       REFERENCES PROFESSOR (CPF)
       ON DELETE RESTRICT
       ON UPDATE CASCADE,
   CONSTRAINT chk_capacidade CHECK (capacidade > 0),
   CONSTRAINT chk_status_turma CHECK (status IN ('A','I'))
) COMMENT 'Tabela de turmas';

/* Tabela PLANO */
CREATE TABLE PLANO (
   codPlano INT AUTO_INCREMENT,
   nome VARCHAR(50) NOT NULL,
   valor DECIMAL(10,2) NOT NULL,
   duracao INT NOT NULL,
   descricao VARCHAR(200),
   status CHAR(1) DEFAULT 'A',
   CONSTRAINT pk_plano PRIMARY KEY (codPlano),
   CONSTRAINT chk_valor_plano CHECK (valor > 0),
   CONSTRAINT chk_duracao CHECK (duracao > 0),
   CONSTRAINT chk_status_plano CHECK (status IN ('A','I'))
) COMMENT 'Tabela de planos disponíveis';

/* Tabela MATRICULA */
CREATE TABLE MATRICULA (
   codMatricula INT AUTO_INCREMENT,
   CPF_aluno CHAR(11) NOT NULL,
   codPlano INT NOT NULL,
   dataInicio DATE NOT NULL,
   dataFim DATE,
   status CHAR(1) DEFAULT 'A',
   CONSTRAINT pk_matricula PRIMARY KEY (codMatricula),
   CONSTRAINT fk_matricula_aluno FOREIGN KEY (CPF_aluno) 
       REFERENCES ALUNO (CPF)
       ON DELETE RESTRICT
       ON UPDATE CASCADE,
   CONSTRAINT fk_matricula_plano FOREIGN KEY (codPlano) 
       REFERENCES PLANO (codPlano)
       ON DELETE RESTRICT
       ON UPDATE CASCADE,
   CONSTRAINT chk_datas CHECK (dataFim IS NULL OR dataFim > dataInicio),
   CONSTRAINT chk_status_matricula CHECK (status IN ('A','I'))
) COMMENT 'Tabela de matrículas dos alunos';

/* Tabela PAGAMENTO */
CREATE TABLE PAGAMENTO (
   codPagamento INT AUTO_INCREMENT,
   codMatricula INT NOT NULL,
   dataPagamento DATE NOT NULL,
   valor DECIMAL(10,2) NOT NULL,
   formaPagamento ENUM('Dinheiro','Cartão Débito','Cartão Crédito','PIX') NOT NULL,
   status CHAR(1) DEFAULT 'A',
   CONSTRAINT pk_pagamento PRIMARY KEY (codPagamento),
   CONSTRAINT fk_pagamento_matricula FOREIGN KEY (codMatricula) 
       REFERENCES MATRICULA (codMatricula)
       ON DELETE RESTRICT
       ON UPDATE CASCADE,
   CONSTRAINT chk_valor_pagamento CHECK (valor > 0),
   CONSTRAINT chk_status_pagamento CHECK (status IN ('A','I'))
) COMMENT 'Tabela de pagamentos';

/* Tabela AVALIACAO */
CREATE TABLE AVALIACAO (
   codAvaliacao INT AUTO_INCREMENT,
   CPF_aluno CHAR(11) NOT NULL,
   CPF_professor CHAR(11) NOT NULL,
   data DATE NOT NULL,
   peso DECIMAL(5,2),
   altura DECIMAL(3,2),
   percentualGordura DECIMAL(5,2),
   observacoes VARCHAR(500),
   CONSTRAINT pk_avaliacao PRIMARY KEY (codAvaliacao),
   CONSTRAINT fk_avaliacao_aluno FOREIGN KEY (CPF_aluno) 
       REFERENCES ALUNO (CPF)
       ON DELETE RESTRICT
       ON UPDATE CASCADE,
   CONSTRAINT fk_avaliacao_professor FOREIGN KEY (CPF_professor) 
       REFERENCES PROFESSOR (CPF)
       ON DELETE RESTRICT
       ON UPDATE CASCADE,
   CONSTRAINT chk_peso CHECK (peso > 0),
   CONSTRAINT chk_altura CHECK (altura > 0 AND altura < 3),
   CONSTRAINT chk_gordura CHECK (percentualGordura >= 0 AND percentualGordura <= 100)
) COMMENT 'Tabela de avaliações físicas';

/* Tabela ALUNO_TURMA */
CREATE TABLE ALUNO_TURMA (
   codAluno_Turma INT AUTO_INCREMENT,
   codTurma INT NOT NULL,
   CPF_aluno CHAR(11) NOT NULL,
   dataInscricao DATE NOT NULL DEFAULT (CURRENT_DATE),
   status CHAR(1) DEFAULT 'A',
   CONSTRAINT pk_aluno_turma PRIMARY KEY (codAluno_Turma),
   CONSTRAINT fk_alunoturma_turma FOREIGN KEY (codTurma) 
       REFERENCES TURMA (codTurma)
       ON DELETE RESTRICT
       ON UPDATE CASCADE,
   CONSTRAINT fk_alunoturma_aluno FOREIGN KEY (CPF_aluno) 
       REFERENCES ALUNO (CPF)
       ON DELETE RESTRICT
       ON UPDATE CASCADE,
   CONSTRAINT uk_aluno_turma UNIQUE (codTurma, CPF_aluno),
   CONSTRAINT chk_status_alunoturma CHECK (status IN ('A','I'))
) COMMENT 'Tabela associativa entre alunos e turmas';


-- Inserir ENDERECO
INSERT INTO ENDERECO (rua, numero, complemento, bairro, cidade, estado, CEP) VALUES
('Rua das Flores', '123', 'Apto 101', 'Centro', 'São Paulo', 'SP', '01234567'),
('Av Principal', '456', NULL, 'Jardins', 'São Paulo', 'SP', '01234568'),
('Rua do Comércio', '789', 'Casa', 'Vila Nova', 'São Paulo', 'SP', '01234569'),
('Alameda Santos', '321', 'Bloco A', 'Jardins', 'São Paulo', 'SP', '01234570'),
('Rua Augusta', '654', NULL, 'Consolação', 'São Paulo', 'SP', '01234571');

-- Inserir ALUNO
INSERT INTO ALUNO (CPF, nome, email, telefone, codEndereco, status) VALUES
('12345678901', 'João Silva', 'joao@email.com', '11999998888', 1, 'A'),
('23456789012', 'Maria Santos', 'maria@email.com', '11999997777', 2, 'A'),
('34567890123', 'Pedro Souza', 'pedro@email.com', '11999996666', 3, 'A'),
('45678901234', 'Ana Costa', 'ana@email.com', '11999995555', 4, 'A'),
('56789012345', 'Carlos Oliveira', 'carlos@email.com', '11999994444', 5, 'A');

-- Inserir PROFESSOR
INSERT INTO PROFESSOR (CPF, nome, telefone, especializacao, salario, status) VALUES
('98765432101', 'Paulo Rodrigues', '11988887777', 'Musculação', 3500.00, 'A'),
('87654321012', 'Mariana Lima', '11988886666', 'Yoga', 3000.00, 'A'),
('76543210923', 'Roberto Santos', '11988885555', 'Spinning', 3200.00, 'A'),
('65432109834', 'Carla Mendes', '11988884444', 'Pilates', 3800.00, 'A'),
('54321098745', 'Fernando Costa', '11988883333', 'CrossFit', 4000.00, 'A');

-- Inserir MODALIDADE
INSERT INTO MODALIDADE (nome, descricao, requisitos, status) VALUES
('Musculação', 'Treino com pesos', 'Idade mínima 16 anos', 'A'),
('Yoga', 'Práticas de relaxamento e equilíbrio', 'Nenhum', 'A'),
('Spinning', 'Aula de bike indoor', 'Nenhum', 'A'),
('Pilates', 'Exercícios de força e flexibilidade', 'Nenhum', 'A'),
('CrossFit', 'Treino funcional de alta intensidade', 'Avaliação física obrigatória', 'A');

-- Inserir TURMA
INSERT INTO TURMA (codModalidade, CPF_professor, horario, diaSemana, capacidade, status) VALUES
(1, '98765432101', '07:00:00', 'Segunda', 20, 'A'),
(2, '87654321012', '08:00:00', 'Terça', 15, 'A'),
(3, '76543210923', '09:00:00', 'Quarta', 25, 'A'),
(4, '65432109834', '10:00:00', 'Quinta', 10, 'A'),
(5, '54321098745', '11:00:00', 'Sexta', 15, 'A');

-- Inserir PLANO
INSERT INTO PLANO (nome, valor, duracao, descricao, status) VALUES
('Basic', 89.90, 1, 'Acesso à musculação', 'A'),
('Standard', 129.90, 3, 'Musculação + 1 modalidade', 'A'),
('Premium', 169.90, 6, 'Acesso total', 'A'),
('VIP', 199.90, 12, 'Acesso total + Personal', 'A'),
('Day Pass', 29.90, 1, 'Acesso diário', 'A');

-- Inserir MATRICULA
INSERT INTO MATRICULA (CPF_aluno, codPlano, dataInicio, dataFim, status) VALUES
('12345678901', 1, '2024-01-01', '2024-02-01', 'A'),
('23456789012', 2, '2024-01-01', '2024-04-01', 'A'),
('34567890123', 3, '2024-01-01', '2024-07-01', 'A'),
('45678901234', 4, '2024-01-01', '2025-01-01', 'A'),
('56789012345', 5, '2024-01-01', '2024-01-02', 'A');

-- Inserir PAGAMENTO
INSERT INTO PAGAMENTO (codMatricula, dataPagamento, valor, formaPagamento, status) VALUES
(1, '2024-01-01', 89.90, 'Cartão Crédito', 'A'),
(2, '2024-01-01', 129.90, 'PIX', 'A'),
(3, '2024-01-01', 169.90, 'Cartão Débito', 'A'),
(4, '2024-01-01', 199.90, 'Dinheiro', 'A'),
(5, '2024-01-01', 29.90, 'PIX', 'A');

-- Inserir AVALIACAO
INSERT INTO AVALIACAO (CPF_aluno, CPF_professor, data, peso, altura, percentualGordura, observacoes) VALUES
('12345678901', '98765432101', '2024-01-02', 70.5, 1.75, 15.5, 'Iniciante'),
('23456789012', '87654321012', '2024-01-02', 65.3, 1.65, 18.2, 'Intermediário'),
('34567890123', '76543210923', '2024-01-02', 80.0, 1.80, 12.8, 'Avançado'),
('45678901234', '65432109834', '2024-01-02', 58.7, 1.60, 20.1, 'Iniciante'),
('56789012345', '54321098745', '2024-01-02', 75.2, 1.78, 14.3, 'Intermediário');

-- Inserir ALUNO_TURMA
INSERT INTO ALUNO_TURMA (codTurma, CPF_aluno, dataInscricao, status) VALUES
(1, '12345678901', '2024-01-02', 'A'),
(2, '23456789012', '2024-01-02', 'A'),
(3, '34567890123', '2024-01-02', 'A'),
(4, '45678901234', '2024-01-02', 'A'),
(5, '56789012345', '2024-01-02', 'A');


/* 1. VIEWS PRINCIPAIS */

-- View de Alunos Ativos com seus Planos
CREATE VIEW vw_alunos_ativos AS
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
WHERE a.status = 'A' AND m.status = 'A';

-- View de Turmas com Professores
CREATE VIEW vw_turmas_detalhes AS
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
GROUP BY t.codTurma;

/* 2. CONSULTAS PARA RELATÓRIOS */

-- Relatório de Inadimplência
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
);

-- Relatório de Ocupação das Turmas
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
ORDER BY m.nome, t.diaSemana, t.horario;

/* 3. CONSULTAS OPERACIONAIS */

-- Busca de Alunos por Modalidade
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
ORDER BY m.nome, a.nome;

-- Faturamento por Período e Forma de Pagamento
SELECT 
    DATE_FORMAT(dataPagamento, '%Y-%m') AS mes,
    formaPagamento,
    COUNT(*) AS quantidade,
    SUM(valor) AS total
FROM PAGAMENTO
WHERE status = 'A'
GROUP BY DATE_FORMAT(dataPagamento, '%Y-%m'), formaPagamento
ORDER BY mes, formaPagamento;

/* 4. CONSULTAS DE ACOMPANHAMENTO */

-- Evolução das Avaliações Físicas
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
ORDER BY a.nome, av.data;

-- Histórico de Frequência nas Modalidades
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
ORDER BY a.nome, m.nome;

/* 5. CONSULTAS ADMINISTRATIVAS */

-- Análise de Desempenho dos Professores
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
GROUP BY p.CPF, m.codModalidade;

-- Análise de Renovações de Matrícula
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
ORDER BY total_renovacoes DESC;

/* 6. CONSULTAS ANALÍTICAS */

-- Análise de Ocupação da Academia por Horário
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
    t.horario;
