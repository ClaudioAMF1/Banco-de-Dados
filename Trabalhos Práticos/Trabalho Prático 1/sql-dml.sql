-- Inserção de Planos
INSERT INTO Plano (nome, valor, duracao_meses, descricao) VALUES
('Plano Basic', 89.90, 1, 'Acesso à academia em horário comercial'),
('Plano Premium', 129.90, 1, 'Acesso à academia 24h e aulas em grupo'),
('Plano Basic Trimestral', 249.90, 3, 'Plano Basic com desconto trimestral'),
('Plano Premium Trimestral', 359.90, 3, 'Plano Premium com desconto trimestral'),
('Plano Basic Anual', 899.90, 12, 'Plano Basic com desconto anual'),
('Plano Premium Anual', 1299.90, 12, 'Plano Premium com desconto anual');

-- Inserção de Funcionários
INSERT INTO Funcionario (nome, cpf, cargo, registro_profissional, telefone, email, salario_base) VALUES
('João Silva', '12345678901', 'instrutor', 'CREF12345', '11999887766', 'joao.silva@fitpro.com', 2500.00),
('Maria Santos', '23456789012', 'personal', 'CREF23456', '11999887755', 'maria.santos@fitpro.com', 3500.00),
('Pedro Oliveira', '34567890123', 'nutricionista', 'CRN12345', '11999887744', 'pedro.oliveira@fitpro.com', 4000.00),
('Ana Costa', '45678901234', 'recepcionista', NULL, '11999887733', 'ana.costa@fitpro.com', 2000.00),
('Carlos Ferreira', '56789012345', 'gerente', NULL, '11999887722', 'carlos.ferreira@fitpro.com', 5000.00);

-- Inserção de Alunos
INSERT INTO Aluno (nome, cpf, data_nascimento, telefone, email, rua, numero, bairro, cidade, cep) VALUES
('Lucas Mendes', '78901234567', '1990-03-15', '11988776655', 'lucas.mendes@email.com', 'Rua das Flores', '123', 'Centro', 'São Paulo', '01234567'),
('Julia Almeida', '89012345678', '1995-07-22', '11988776644', 'julia.almeida@email.com', 'Av Principal', '456', 'Jardins', 'São Paulo', '12345678'),
('Roberto Santos', '90123456789', '1988-11-30', '11988776633', 'roberto.santos@email.com', 'Rua do Comércio', '789', 'Vila Nova', 'São Paulo', '23456789'),
('Mariana Lima', '01234567890', '1992-05-10', '11988776622', 'mariana.lima@email.com', 'Rua das Palmeiras', '321', 'Moema', 'São Paulo', '34567890');

-- Inserção de Matrículas
INSERT INTO Matricula (id_aluno, id_plano, data_inicio, data_fim, valor_pago) VALUES
(1, 2, '2024-01-01', '2024-02-01', 129.90),
(2, 4, '2024-01-15', '2024-04-15', 359.90),
(3, 6, '2024-02-01', '2025-02-01', 1299.90),
(4, 1, '2024-02-15', '2024-03-15', 89.90);

-- Inserção de Exercícios
INSERT INTO Exercicio (nome, grupo_muscular, descricao, nivel) VALUES
('Supino Reto', 'peito', 'Exercício para peitoral com barra', 'intermediario'),
('Agachamento', 'pernas', 'Exercício para quadríceps com barra', 'avancado'),
('Puxada Alta', 'costas', 'Exercício para dorsal na polia', 'iniciante'),
('Desenvolvimento', 'ombros', 'Exercício para deltoides com halter', 'intermediario'),
('Rosca Direta', 'biceps', 'Exercício para bíceps com barra', 'iniciante'),
('Extensão Triceps', 'triceps', 'Exercício para tríceps na polia', 'intermediario'),
('Abdominal', 'abdomen', 'Exercício para abdômen no solo', 'iniciante'),
('Elevação Pélvica', 'gluteos', 'Exercício para glúteos com peso', 'intermediario');

-- Inserção de Avaliações Físicas
INSERT INTO Avaliacao_Fisica (id_aluno, id_funcionario, data_avaliacao, peso, altura, imc, percentual_gordura, observacoes) VALUES
(1, 3, '2024-01-02', 75.5, 1.75, 24.65, 18.5, 'Bom condicionamento físico'),
(2, 3, '2024-01-16', 65.0, 1.65, 23.88, 25.0, 'Necessita fortalecimento muscular'),
(3, 3, '2024-02-02', 85.0, 1.80, 26.23, 22.0, 'Foco em perda de peso'),
(4, 3, '2024-02-16', 58.0, 1.60, 22.66, 23.5, 'Foco em ganho de massa muscular');

-- Inserção de Treinos
INSERT INTO Treino (id_aluno, id_funcionario, data_criacao, data_validade, tipo, objetivo) VALUES
(1, 1, '2024-01-02', '2024-04-02', 'intermediario', 'Hipertrofia'),
(2, 1, '2024-01-16', '2024-04-16', 'iniciante', 'Condicionamento'),
(3, 2, '2024-02-02', '2024-05-02', 'avancado', 'Emagrecimento'),
(4, 2, '2024-02-16', '2024-05-16', 'iniciante', 'Ganho de massa');

-- Inserção de Fichas de Treino
INSERT INTO Ficha_Treino (id_treino, id_exercicio, series, repeticoes, carga, observacao) VALUES
(1, 1, 4, 12, 40.0, 'Intervalo 60s'),
(1, 3, 4, 12, 50.0, 'Intervalo 60s'),
(1, 5, 3, 15, 15.0, 'Intervalo 45s'),
(2, 2, 3, 15, 30.0, 'Intervalo 60s'),
(2, 4, 3, 12, 8.0, 'Intervalo 45s'),
(2, 7, 3, 20, NULL, 'Intervalo 30s'),
(3, 2, 4, 10, 60.0, 'Intervalo 90s'),
(3, 6, 4, 12, 25.0, 'Intervalo 60s'),
(3, 8, 4, 15, 40.0, 'Intervalo 60s'),
(4, 1, 3, 12, 20.0, 'Intervalo 60s'),
(4, 3, 3, 12, 30.0, 'Intervalo 60s'),
(4, 7, 3, 15, NULL, 'Intervalo 45s');

-- Inserção de Presenças
INSERT INTO Presenca (id_aluno, data, hora_entrada, hora_saida) VALUES
(1, '2024-02-19', '08:00:00', '09:30:00'),
(2, '2024-02-19', '10:00:00', '11:15:00'),
(3, '2024-02-19', '16:00:00', '17:30:00'),
(4, '2024-02-19', '18:00:00', '19:00:00'),
(1, '2024-02-20', '08:00:00', '09:15:00'),
(2, '2024-02-20', '10:00:00', '11:30:00'),
(3, '2024-02-20', '16:00:00', '17:45:00'),
(4, '2024-02-20', '18:00:00', '19:30:00');

-- Inserção de Pagamentos
INSERT INTO Pagamento (id_matricula, data_pagamento, valor, metodo, status) VALUES
(1, '2024-01-01', 129.90, 'cartao_credito', 'confirmado'),
(2, '2024-01-15', 359.90, 'pix', 'confirmado'),
(3, '2024-02-01', 1299.90, 'cartao_credito', 'confirmado'),
(4, '2024-02-15', 89.90, 'cartao_debito', 'confirmado');

-- Inserção de Produtos
INSERT INTO Produto (nome, categoria, preco_venda, estoque) VALUES
('Whey Protein 900g', 'suplemento', 129.90, 50),
('BCAA 120 caps', 'suplemento', 59.90, 30),
('Camiseta Fitness', 'vestuario', 49.90, 100),
('Luva de Treino', 'acessorio', 39.90, 45),
('Creatina 300g', 'suplemento', 89.90, 40),
('Shake', 'acessorio', 29.90, 60);

-- Inserção de Vendas e Itens de Venda
INSERT INTO Venda (id_aluno, id_funcionario, data_venda, valor_total, metodo_pagamento) VALUES
(1, 4, '2024-02-19', 189.80, 'cartao_credito'),
(2, 4, '2024-02-19', 119.80, 'pix'),
(3, 4, '2024-02-20', 219.70, 'cartao_debito');

INSERT INTO Item_Venda (id_venda, id_produto, quantidade, valor_unitario, subtotal) VALUES
(1, 1, 1, 129.90, 129.90),
(1, 4, 1, 39.90, 39.90),
(2, 2, 2, 59.90, 119.80),
(3, 5, 2, 89.90, 179.80),
(3, 6, 1, 29.90, 29.90);
