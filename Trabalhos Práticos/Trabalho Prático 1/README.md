# Trabalho Prático 1 - Sistema de Academia

Este repositório contém a implementação do primeiro trabalho prático da disciplina de Banco de Dados.

## 📁 Estrutura do Repositório

- [Scripts completo TP1.sql](Scripts%20completo%20TP1.sql) - **Arquivo completo com todos os scripts (DDL, DML e Consultas)**
- [Consultas-sql-resumo.md](Consultas-sql-resumo.md) - Consultas SQL para análise de dados
- [DDL-academia.sql](DDL-academia.sql) - Scripts de criação do banco e tabelas
- [DML-academia.sql](DML-academia.sql) - Scripts de inserção de dados
- [Modelo físico - não normalizado.pdf](Modelo%20fisico%20-%20nao%20normalizado.pdf) - Modelo físico inicial
- [Modelo físico - normalizado.pdf](Modelo%20fisico%20-%20normalizado.pdf) - Modelo físico após normalização
- [Modelo lógico - não normalizado.pdf](Modelo%20logico%20-%20nao%20normalizado.pdf) - Modelo lógico inicial
- [Modelo lógico - normalizado.pdf](Modelo%20logico%20-%20normalizado.pdf) - Modelo lógico após normalização
- [Modelos conceituais.png](Modelos%20conceituais.png) - Diagramas Entidade-Relacionamento
- [Normalizacao-academia.md](Normalizacao-academia.md) - Processo de normalização detalhado
- [Resumo-negocio.md](Resumo-negocio.md) - Descrição do negócio e regras

## 📝 Sobre o Projeto

Sistema desenvolvido para gerenciamento de uma academia, incluindo controle de alunos, professores, turmas, modalidades, matrículas e pagamentos.

### Principais Funcionalidades
- Gestão de alunos
- Controle de professores
- Gerenciamento de turmas
- Controle de modalidades
- Matrículas e pagamentos
- Avaliações físicas

### Tecnologias Utilizadas
- MySQL 8.0
- Workbench 8.0

## 🔍 Detalhamento dos Arquivos

### Scripts SQL Consolidados
O arquivo [Scripts completo TP1.sql](Scripts%20completo%20TP1.sql) contém:
- Todo o código DDL para criação do banco e tabelas
- Todos os comandos DML para inserção de dados
- Todas as consultas e análises desenvolvidas
- Views e relatórios implementados

### Modelos
- **Conceitual**: Ver [Modelos conceituais.png](Modelos%20conceituais.png)
- **Lógico**: Ver modelos [não normalizado](Modelo%20logico%20-%20nao%20normalizado.pdf) e [normalizado](Modelo%20logico%20-%20normalizado.pdf)
- **Físico**: Ver modelos [não normalizado](Modelo%20fisico%20-%20nao%20normalizado.pdf) e [normalizado](Modelo%20fisico%20-%20normalizado.pdf)

### Scripts SQL Separados
- **DDL**: Ver [DDL-academia.sql](DDL-academia.sql)
- **DML**: Ver [DML-academia.sql](DML-academia.sql)
- **Consultas**: Ver [Consultas-sql-resumo.md](Consultas-sql-resumo.md)

### Documentação
- Processo de normalização: Ver [Normalizacao-academia.md](Normalizacao-academia.md)
- Descrição do negócio: Ver [Resumo-negocio.md](Resumo-negocio.md)
- Consultas e análises: Ver [Consultas-sql-resumo.md](Consultas-sql-resumo.md)

## 🚀 Como Utilizar

1. Clone o repositório
2. Para implementação completa:
   - Execute o [Scripts completo TP1.sql](Scripts%20completo%20TP1.sql)
3. Ou execute os scripts separadamente:
   1. [DDL-academia.sql](DDL-academia.sql)
   2. [DML-academia.sql](DML-academia.sql)
   3. Consultas do arquivo [Consultas-sql-resumo.md](Consultas-sql-resumo.md)

## ✨ Funcionalidades Implementadas

- [x] Cadastro de alunos e professores
- [x] Gestão de turmas e modalidades
- [x] Controle de matrículas
- [x] Gestão de pagamentos
- [x] Avaliações físicas
- [x] Análises e relatórios

## 📊 Modelo de Dados

O banco de dados foi projetado considerando:
- Normalização até 3FN (documentado em [Normalizacao-academia.md](Normalizacao-academia.md))
- Integridade referencial
- Restrições de domínio
- Índices apropriados

## 🤝 Autor

Claudio Meireles
- Curso: Engenharia de Software
- Disciplina: Banco de Dados
- Professor(a): Lorena Borges
- Instituição: IDP
