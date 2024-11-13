# Consultas SQL - Academia

## 1. VIEWS

### View de Alunos Ativos
```sql
CREATE VIEW vw_alunos_ativos AS
SELECT 
    a.CPF, a.nome AS nome_aluno, a.telefone,
    m.dataInicio, m.dataFim,
    p.nome AS nome_plano, p.valor
FROM ALUNO a
INNER JOIN MATRICULA m ON a.CPF = m.CPF_aluno
INNER JOIN PLANO p ON m.codPlano = p.codPlano
WHERE a.status = 'A' AND m.status = 'A';
```
*Exibe informações dos alunos ativos com seus planos atuais*

### View de Turmas
```sql
CREATE VIEW vw_turmas_detalhes AS
SELECT 
    t.codTurma, m.nome AS modalidade,
    p.nome AS professor, t.horario,
    t.diaSemana, t.capacidade,
    COUNT(at.CPF_aluno) AS alunos_matriculados
FROM TURMA t
INNER JOIN MODALIDADE m ON t.codModalidade = m.codModalidade
INNER JOIN PROFESSOR p ON t.CPF_professor = p.CPF
LEFT JOIN ALUNO_TURMA at ON t.codTurma = at.codTurma
WHERE t.status = 'A'
GROUP BY t.codTurma;
```
*Mostra detalhes das turmas com quantidade de alunos*

## 2. CONSULTAS DE GESTÃO

### Inadimplência
```sql
SELECT 
    a.nome AS aluno, a.telefone,
    m.dataFim AS vencimento, p.valor,
    DATEDIFF(CURRENT_DATE, m.dataFim) AS dias_atraso
FROM MATRICULA m
INNER JOIN ALUNO a ON m.CPF_aluno = a.CPF
INNER JOIN PLANO p ON m.codPlano = p.codPlano
WHERE m.dataFim < CURRENT_DATE
AND m.status = 'A';
```
*Lista alunos com pagamentos atrasados*

### Ocupação de Turmas
```sql
SELECT 
    m.nome AS modalidade, t.diaSemana,
    t.horario, p.nome AS professor,
    t.capacidade AS vagas_totais,
    COUNT(at.CPF_aluno) AS vagas_ocupadas
FROM TURMA t
INNER JOIN MODALIDADE m ON t.codModalidade = m.codModalidade
INNER JOIN PROFESSOR p ON t.CPF_professor = p.CPF
LEFT JOIN ALUNO_TURMA at ON t.codTurma = at.codTurma
WHERE t.status = 'A'
GROUP BY t.codTurma;
```
*Mostra ocupação atual de cada turma*

## 3. CONSULTAS OPERACIONAIS

### Alunos por Modalidade
```sql
SELECT 
    m.nome AS modalidade,
    a.nome AS aluno, a.telefone,
    at.dataInscricao
FROM ALUNO_TURMA at
INNER JOIN TURMA t ON at.codTurma = t.codTurma
INNER JOIN MODALIDADE m ON t.codModalidade = m.codModalidade
INNER JOIN ALUNO a ON at.CPF_aluno = a.CPF
WHERE at.status = 'A';
```
*Lista alunos inscritos em cada modalidade*

### Faturamento
```sql
SELECT 
    DATE_FORMAT(dataPagamento, '%Y-%m') AS mes,
    formaPagamento,
    COUNT(*) AS quantidade,
    SUM(valor) AS total
FROM PAGAMENTO
WHERE status = 'A'
GROUP BY DATE_FORMAT(dataPagamento, '%Y-%m'), formaPagamento;
```
*Resumo do faturamento por período e forma de pagamento*

## 4. CONSULTAS DE ACOMPANHAMENTO

### Avaliações Físicas
```sql
SELECT 
    a.nome AS aluno, av.data,
    av.peso, av.altura, av.percentualGordura,
    p.nome AS professor
FROM AVALIACAO av
INNER JOIN ALUNO a ON av.CPF_aluno = a.CPF
INNER JOIN PROFESSOR p ON av.CPF_professor = p.CPF;
```
*Histórico de avaliações físicas dos alunos*

### Frequência
```sql
SELECT 
    a.nome AS aluno,
    m.nome AS modalidade,
    COUNT(at.codAluno_Turma) AS total_frequencia
FROM ALUNO a
INNER JOIN ALUNO_TURMA at ON a.CPF = at.CPF_aluno
INNER JOIN TURMA t ON at.codTurma = t.codTurma
INNER JOIN MODALIDADE m ON t.codModalidade = m.codModalidade
WHERE at.status = 'A'
GROUP BY a.CPF, m.codModalidade;
```
*Frequência dos alunos por modalidade*

## 5. CONSULTAS ADMINISTRATIVAS

### Desempenho de Professores
```sql
SELECT 
    p.nome AS professor,
    m.nome AS modalidade,
    COUNT(DISTINCT at.CPF_aluno) AS total_alunos,
    COUNT(DISTINCT t.codTurma) AS total_turmas
FROM PROFESSOR p
INNER JOIN TURMA t ON p.CPF = t.CPF_professor
INNER JOIN MODALIDADE m ON t.codModalidade = m.codModalidade
LEFT JOIN ALUNO_TURMA at ON t.codTurma = at.codTurma
GROUP BY p.CPF, m.codModalidade;
```
*Indicadores de desempenho dos professores*

### Renovações
```sql
SELECT 
    a.nome AS aluno,
    p.nome AS plano,
    COUNT(*) AS total_renovacoes,
    MAX(m.dataInicio) AS ultima_matricula
FROM ALUNO a
INNER JOIN MATRICULA m ON a.CPF = m.CPF_aluno
INNER JOIN PLANO p ON m.codPlano = p.codPlano
GROUP BY a.CPF, p.codPlano
HAVING COUNT(*) > 1;
```
*Histórico de renovações de matrícula*

---
*Todas as consultas podem ser adaptadas conforme necessidade específica do negócio.*