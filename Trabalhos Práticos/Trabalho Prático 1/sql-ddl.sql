-- Criação do banco de dados
CREATE DATABASE IF NOT EXISTS academia_fitpro;
USE academia_fitpro;

-- Tabela Aluno
CREATE TABLE Aluno (
    id_aluno INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf CHAR(11) NOT NULL UNIQUE,
    data_nascimento DATE NOT NULL,
    telefone VARCHAR(15) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    rua VARCHAR(100) NOT NULL,
    numero VARCHAR(10) NOT NULL,
    bairro VARCHAR(50) NOT NULL,
    cidade VARCHAR(50) NOT NULL,
    cep CHAR(8) NOT NULL,
    status ENUM('ativo', 'inativo', 'pendente') DEFAULT 'ativo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT chk_cpf_aluno CHECK (LENGTH(cpf) = 11),
    CONSTRAINT chk_email_aluno CHECK (email LIKE '%@%.%'),
    CONSTRAINT chk_cep CHECK (LENGTH(cep) = 8)
);

-- Tabela Plano
CREATE TABLE Plano (
    id_plano INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE,
    valor DECIMAL(10,2) NOT NULL,
    duracao_meses INT NOT NULL,
    descricao TEXT,
    status ENUM('ativo', 'inativo') DEFAULT 'ativo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT chk_valor_plano CHECK (valor > 0),
    CONSTRAINT chk_duracao CHECK (duracao_meses > 0)
);

-- Tabela Funcionario
CREATE TABLE Funcionario (
    id_funcionario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf CHAR(11) NOT NULL UNIQUE,
    cargo ENUM('instrutor', 'personal', 'nutricionista', 'recepcionista', 'gerente') NOT NULL,
    registro_profissional VARCHAR(20),
    telefone VARCHAR(15) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    salario_base DECIMAL(10,2) NOT NULL,
    status ENUM('ativo', 'inativo') DEFAULT 'ativo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT chk_cpf_func CHECK (LENGTH(cpf) = 11),
    CONSTRAINT chk_email_func CHECK (email LIKE '%@%.%'),
    CONSTRAINT chk_salario CHECK (salario_base > 0)
);

-- Tabela Matricula
CREATE TABLE Matricula (
    id_matricula INT AUTO_INCREMENT PRIMARY KEY,
    id_aluno INT NOT NULL,
    id_plano INT NOT NULL,
    data_inicio DATE NOT NULL,
    data_fim DATE NOT NULL,
    status ENUM('ativa', 'cancelada', 'pendente', 'vencida') DEFAULT 'ativa',
    valor_pago DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_aluno) REFERENCES Aluno(id_aluno),
    FOREIGN KEY (id_plano) REFERENCES Plano(id_plano),
    CONSTRAINT chk_datas_matricula CHECK (data_fim >= data_inicio),
    CONSTRAINT chk_valor_matricula CHECK (valor_pago > 0)
);

-- Tabela Avaliacao_Fisica
CREATE TABLE Avaliacao_Fisica (
    id_avaliacao INT AUTO_INCREMENT PRIMARY KEY,
    id_aluno INT NOT NULL,
    id_funcionario INT NOT NULL,
    data_avaliacao DATE NOT NULL,
    peso DECIMAL(5,2) NOT NULL,
    altura DECIMAL(3,2) NOT NULL,
    imc DECIMAL(4,2) NOT NULL,
    percentual_gordura DECIMAL(4,2),
    observacoes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_aluno) REFERENCES Aluno(id_aluno),
    FOREIGN KEY (id_funcionario) REFERENCES Funcionario(id_funcionario),
    CONSTRAINT chk_peso CHECK (peso > 0),
    CONSTRAINT chk_altura CHECK (altura > 0)
);

-- Tabela Exercicio
CREATE TABLE Exercicio (
    id_exercicio INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    grupo_muscular ENUM('peito', 'costas', 'pernas', 'ombros', 'biceps', 'triceps', 'abdomen', 'gluteos') NOT NULL,
    descricao TEXT,
    nivel ENUM('iniciante', 'intermediario', 'avancado') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela Treino
CREATE TABLE Treino (
    id_treino INT AUTO_INCREMENT PRIMARY KEY,
    id_aluno INT NOT NULL,
    id_funcionario INT NOT NULL,
    data_criacao DATE NOT NULL,
    data_validade DATE NOT NULL,
    tipo ENUM('iniciante', 'intermediario', 'avancado') NOT NULL,
    objetivo TEXT,
    status ENUM('ativo', 'inativo') DEFAULT 'ativo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_aluno) REFERENCES Aluno(id_aluno),
    FOREIGN KEY (id_funcionario) REFERENCES Funcionario(id_funcionario),
    CONSTRAINT chk_datas_treino CHECK (data_validade >= data_criacao)
);

-- Tabela Ficha_Treino
CREATE TABLE Ficha_Treino (
    id_ficha INT AUTO_INCREMENT PRIMARY KEY,
    id_treino INT NOT NULL,
    id_exercicio INT NOT NULL,
    series INT NOT NULL,
    repeticoes INT NOT NULL,
    carga DECIMAL(5,2),
    observacao TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_treino) REFERENCES Treino(id_treino),
    FOREIGN KEY (id_exercicio) REFERENCES Exercicio(id_exercicio),
    CONSTRAINT chk_series CHECK (series > 0),
    CONSTRAINT chk_repeticoes CHECK (repeticoes > 0),
    CONSTRAINT chk_carga CHECK (carga IS NULL OR carga > 0)
);

-- Tabela Presenca
CREATE TABLE Presenca (
    id_presenca INT AUTO_INCREMENT PRIMARY KEY,
    id_aluno INT NOT NULL,
    data DATE NOT NULL,
    hora_entrada TIME NOT NULL,
    hora_saida TIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_aluno) REFERENCES Aluno(id_aluno),
    CONSTRAINT chk_hora_presenca CHECK (hora_saida IS NULL OR hora_saida > hora_entrada)
);

-- Tabela Pagamento
CREATE TABLE Pagamento (
    id_pagamento INT AUTO_INCREMENT PRIMARY KEY,
    id_matricula INT NOT NULL,
    data_pagamento DATE NOT NULL,
    valor DECIMAL(10,2) NOT NULL,
    metodo ENUM('dinheiro', 'cartao_credito', 'cartao_debito', 'pix') NOT NULL,
    status ENUM('pendente', 'confirmado', 'cancelado') DEFAULT 'pendente',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_matricula) REFERENCES Matricula(id_matricula),
    CONSTRAINT chk_valor_pagamento CHECK (valor > 0)
);

-- Tabela Produto
CREATE TABLE Produto (
    id_produto INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    categoria ENUM('suplemento', 'vestuario', 'acessorio') NOT NULL,
    preco_venda DECIMAL(10,2) NOT NULL,
    estoque INT NOT NULL DEFAULT 0,
    status ENUM('ativo', 'inativo') DEFAULT 'ativo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT chk_preco_venda CHECK (preco_venda > 0),
    CONSTRAINT chk_estoque CHECK (estoque >= 0)
);

-- Tabela Venda
CREATE TABLE Venda (
    id_venda INT AUTO_INCREMENT PRIMARY KEY,
    id_aluno INT NOT NULL,
    id_funcionario INT NOT NULL,
    data_venda DATE NOT NULL,
    valor_total DECIMAL(10,2) NOT NULL,
    metodo_pagamento ENUM('dinheiro', 'cartao_credito', 'cartao_debito', 'pix') NOT NULL,
    status ENUM('finalizada', 'cancelada') DEFAULT 'finalizada',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_aluno) REFERENCES Aluno(id_aluno),
    FOREIGN KEY (id_funcionario) REFERENCES Funcionario(id_funcionario),
    CONSTRAINT chk_valor_total CHECK (valor_total > 0)
);

-- Tabela Item_Venda
CREATE TABLE Item_Venda (
    id_item INT AUTO_INCREMENT PRIMARY KEY,
    id_venda INT NOT NULL,
    id_produto INT NOT NULL,
    quantidade INT NOT NULL,
    valor_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_venda) REFERENCES Venda(id_venda),
    FOREIGN KEY (id_produto) REFERENCES Produto(id_produto),
    CONSTRAINT chk_quantidade CHECK (quantidade > 0),
    CONSTRAINT chk_valor_unitario CHECK (valor_unitario > 0),
    CONSTRAINT chk_subtotal CHECK (subtotal > 0)
);

-- Índices para otimização
CREATE INDEX idx_aluno_nome ON Aluno(nome);
CREATE INDEX idx_aluno_cpf ON Aluno(cpf);
CREATE INDEX idx_funcionario_nome ON Funcionario(nome);
CREATE INDEX idx_matricula_status ON Matricula(status);
CREATE INDEX idx_treino_data ON Treino(data_criacao);
CREATE INDEX idx_presenca_data ON Presenca(data);
CREATE INDEX idx_pagamento_status ON Pagamento(status);
CREATE INDEX idx_produto_nome ON Produto(nome);
CREATE INDEX idx_venda_data ON Venda(data_venda);
