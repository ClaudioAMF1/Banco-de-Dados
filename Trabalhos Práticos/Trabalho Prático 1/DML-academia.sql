-- Usar o banco de dados
USE academia;

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
