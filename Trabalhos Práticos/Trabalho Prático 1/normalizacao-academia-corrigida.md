# Normalização do Sistema de Academia

## Descrição do Processo
Este documento descreve o processo de normalização aplicado às tabelas do banco de dados da academia, utilizando as três primeiras formas normais (1FN, 2FN e 3FN).

## Processo de Normalização

### Primeira Forma Normal (1FN)
*Elimina grupos repetitivos e garante atomicidade dos dados*

**Situação Identificada:**
- Endereço do aluno continha múltiplos dados em um único campo
- Telefones podiam ter múltiplos valores

**Solução Aplicada:**
```
ANTES:
Aluno (CPF, nome, endereço[rua, número, bairro, cidade], telefones[1,2,3])

DEPOIS:
Aluno (CPF, nome, codEndereco)
Endereco (codEndereco, rua, numero, bairro, cidade, cep)
Telefone (codTelefone, CPF_aluno, numero)
```

### Segunda Forma Normal (2FN)
*Remove dependências parciais da chave primária*

**Situação Identificada:**
- Na tabela Turma_Aluno, informações do aluno dependiam apenas do CPF

**Solução Aplicada:**
```
ANTES:
Turma_Aluno (CPF_aluno, codTurma, nomeAluno, emailAluno, dataNascimento)

DEPOIS:
Aluno (CPF, nome, email, dataNascimento)
Aluno_Turma (codAluno_Turma, CPF_aluno, codTurma, dataInscricao)
```

### Terceira Forma Normal (3FN)
*Elimina dependências transitivas*

**Situação Identificada:**
- Na tabela Matricula, informações do plano dependiam do código do plano

**Solução Aplicada:**
```
ANTES:
Matricula (codMatricula, CPF_aluno, nomePlano, valorPlano, dataInicio)

DEPOIS:
Matricula (codMatricula, CPF_aluno, codPlano, dataInicio)
Plano (codPlano, nome, valor)
```

## Resultado da Normalização

### Tabelas Normalizadas
1. Aluno 
2. Professor
3. Turma
4. Modalidade
5. Matricula
6. Plano
7. Pagamento
8. Avaliacao
9. Endereco
10. Aluno_Turma

### Benefícios Alcançados
1. Eliminação de redundâncias
2. Integridade dos dados
3. Facilidade de manutenção
4. Economia de espaço
5. Melhor performance em consultas

## Considerações Finais
- A normalização focou em organizar os dados de forma eficiente
- Todas as tabelas atendem às três primeiras formas normais
- A estrutura resultante evita anomalias de inserção, atualização e exclusão

---
*Observação: Este processo de normalização considerou as regras de negócio específicas de uma academia.*