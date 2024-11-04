# Modelo Físico e Normalização - Academia FitPro

## Processo de Normalização

### Primeira Forma Normal (1FN)
- Eliminação de grupos repetitivos
- Cada atributo possui apenas valores atômicos
- Identificação de chaves primárias

Exemplo de aplicação na tabela Aluno:
* Antes da 1FN:
```
Aluno (id_aluno, nome, telefones[principal, secundário], endereço[rua, número, bairro, cidade])
```
* Depois da 1FN:
```
Aluno (id_aluno, nome, telefone, email, rua, numero, bairro, cidade, cep)
```

### Segunda Forma Normal (2FN)
- Atende à 1FN
- Todos os atributos não-chave são totalmente dependentes da chave primária

Exemplo de aplicação na tabela Treino e Exercícios:
* Antes da 2FN:
```
Treino_Exercicios (id_treino, id_exercicio, nome_exercicio, grupo_muscular, series, repeticoes)
```
* Depois da 2FN:
```
Treino (id_treino, data_criacao, objetivo)
Exercicio (id_exercicio, nome, grupo_muscular)
Ficha_Treino (id_ficha, id_treino, id_exercicio, series, repeticoes)
```

### Terceira Forma Normal (3FN)
- Atende à 2FN
- Não existem dependências transitivas

Exemplo de aplicação na tabela Matricula:
* Antes da 3FN:
```
Matricula (id_matricula, id_aluno, id_plano, nome_plano, valor_plano, data_inicio)
```
* Depois da 3FN:
```
Matricula (id_matricula, id_aluno, id_plano, data_inicio)
Plano (id_plano, nome, valor)
```

## Modelo Físico Detalhado

### Tabela: Aluno
- id_aluno: INT AUTO_INCREMENT (PK)
- nome: VARCHAR(100) NOT NULL
- cpf: CHAR(11) NOT NULL UNIQUE
- data_nascimento: DATE NOT NULL
- telefone: VARCHAR(15) NOT NULL
- email: VARCHAR(100) NOT NULL UNIQUE
- rua: VARCHAR(100) NOT NULL
- numero: VARCHAR(10) NOT NULL
- bairro: VARCHAR(50) NOT NULL
- cidade: VARCHAR(50) NOT NULL
- cep: CHAR(8) NOT NULL
- status: ENUM('ativo', 'inativo', 'pendente') DEFAULT 'ativo'
- created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- updated_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

### Tabela: Plano
- id_plano: INT AUTO_INCREMENT (PK)
- nome: VARCHAR(50) NOT NULL UNIQUE
- valor: DECIMAL(10,2) NOT NULL
- duracao_meses: INT NOT NULL
- descricao: TEXT
- status: ENUM('ativo', 'inativo') DEFAULT 'ativo'
- created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- updated_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

### Tabela: Matricula
- id_matricula: INT AUTO_INCREMENT (PK)
- id_aluno: INT NOT NULL (FK)
- id_plano: INT NOT NULL (FK)
- data_inicio: DATE NOT NULL
- data_fim: DATE NOT NULL
- status: ENUM('ativa', 'cancelada', 'pendente', 'vencida') DEFAULT 'ativa'
- valor_pago: DECIMAL(10,2) NOT NULL
- created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- updated_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

### Tabela: Funcionario
- id_funcionario: INT AUTO_INCREMENT (PK)
- nome: VARCHAR(100) NOT NULL
- cpf: CHAR(11) NOT NULL UNIQUE
- cargo: ENUM('instrutor', 'personal', 'nutricionista', 'recepcionista', 'gerente') NOT NULL
- registro_profissional: VARCHAR(20)
- telefone: VARCHAR(15) NOT NULL
- email: VARCHAR(100) NOT NULL UNIQUE
- salario_base: DECIMAL(10,2) NOT NULL
- status: ENUM('ativo', 'inativo') DEFAULT 'ativo'
- created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- updated_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

### Tabela: Avaliacao_Fisica
- id_avaliacao: INT AUTO_INCREMENT (PK)
- id_aluno: INT NOT NULL (FK)
- id_funcionario: INT NOT NULL (FK)
- data_avaliacao: DATE NOT NULL
- peso: DECIMAL(5,2) NOT NULL
- altura: DECIMAL(3,2) NOT NULL
- imc: DECIMAL(4,2) NOT NULL
- percentual_gordura: DECIMAL(4,2)
- observacoes: TEXT
- created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

### Tabela: Treino
- id_treino: INT AUTO_INCREMENT (PK)
- id_aluno: INT NOT NULL (FK)
- id_funcionario: INT NOT NULL (FK)
- data_criacao: DATE NOT NULL
- data_validade: DATE NOT NULL
- tipo: ENUM('iniciante', 'intermediario', 'avancado') NOT NULL
- objetivo: TEXT
- status: ENUM('ativo', 'inativo') DEFAULT 'ativo'
- created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- updated_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

### Tabela: Exercicio
- id_exercicio: INT AUTO_INCREMENT (PK)
- nome: VARCHAR(100) NOT NULL
- grupo_muscular: ENUM('peito', 'costas', 'pernas', 'ombros', 'biceps', 'triceps', 'abdomen', 'gluteos') NOT NULL
- descricao: TEXT
- nivel: ENUM('iniciante', 'intermediario', 'avancado') NOT NULL
- created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

### Tabela: Ficha_Treino
- id_ficha: INT AUTO_INCREMENT (PK)
- id_treino: INT NOT NULL (FK)
- id_exercicio: INT NOT NULL (FK)
- series: INT NOT NULL
- repeticoes: INT NOT NULL
- carga: DECIMAL(5,2)
- observacao: TEXT
- created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- updated_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

### Tabela: Presenca
- id_presenca: INT AUTO_INCREMENT (PK)
- id_aluno: INT NOT NULL (FK)
- data: DATE NOT NULL
- hora_entrada: TIME NOT NULL
- hora_saida: TIME
- created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

### Tabela: Pagamento
- id_pagamento: INT AUTO_INCREMENT (PK)
- id_matricula: INT NOT NULL (FK)
- data_pagamento: DATE NOT NULL
- valor: DECIMAL(10,2) NOT NULL
- metodo: ENUM('dinheiro', 'cartao_credito', 'cartao_debito', 'pix') NOT NULL
- status: ENUM('pendente', 'confirmado', 'cancelado') DEFAULT 'pendente'
- created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

### Tabela: Produto
- id_produto: INT AUTO_INCREMENT (PK)
- nome: VARCHAR(100) NOT NULL
- categoria: ENUM('suplemento', 'vestuario', 'acessorio') NOT NULL
- preco_venda: DECIMAL(10,2) NOT NULL
- estoque: INT NOT NULL DEFAULT 0
- status: ENUM('ativo', 'inativo') DEFAULT 'ativo'
- created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- updated_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

### Tabela: Venda
- id_venda: INT AUTO_INCREMENT (PK)
- id_aluno: INT NOT NULL (FK)
- id_funcionario: INT NOT NULL (FK)
- data_venda: DATE NOT NULL
- valor_total: DECIMAL(10,2) NOT NULL
- metodo_pagamento: ENUM('dinheiro', 'cartao_credito', 'cartao_debito', 'pix') NOT NULL
- status: ENUM('finalizada', 'cancelada') DEFAULT 'finalizada'
- created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

### Tabela: Item_Venda
- id_item: INT AUTO_INCREMENT (PK)
- id_venda: INT NOT NULL (FK)
- id_produto: INT NOT NULL (FK)
- quantidade: INT NOT NULL
- valor_unitario: DECIMAL(10,2) NOT NULL
- subtotal: DECIMAL(10,2) NOT NULL
- created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
