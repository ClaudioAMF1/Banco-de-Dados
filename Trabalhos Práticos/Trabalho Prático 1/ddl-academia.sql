/* Criação do Banco de Dados */
CREATE DATABASE academia

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
