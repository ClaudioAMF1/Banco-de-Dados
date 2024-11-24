# Sistema de Gestão - Academia Fitness 🏋️‍♂️

Sistema completo de gestão para academias desenvolvido com Python, Streamlit e MySQL.

## 🎯 Funcionalidades

### Módulos Principais
- **Alunos**
 - Cadastro completo de alunos
 - Gerenciamento de matrículas
 - Histórico de pagamentos
 - Registro de avaliações físicas

- **Professores**
 - Cadastro de professores
 - Atribuição de turmas
 - Gestão de horários
 - Especialidades

- **Aulas/Turmas**
 - Cadastro de modalidades
 - Controle de ocupação
 - Gestão de horários
 - Acompanhamento de frequência

- **Matrículas**
 - Gestão de planos
 - Controle de vencimentos
 - Renovações
 - Status de pagamento

- **Financeiro**
 - Controle de pagamentos
 - Gestão de mensalidades
 - Relatórios financeiros
 - Indicadores de inadimplência

### Features Adicionais
- Dashboard interativo
- Relatórios gerenciais
- Sistema de login seguro
- Views personalizadas
- Exportação de dados
- Gráficos e métricas

## 🛠 Tecnologias

- Python 3.8+
- Streamlit 
- MySQL
- Pandas
- Plotly
- Python-dotenv

## 📋 Requisitos

- Python 3.8 ou superior
- MySQL 8.0 ou superior
- pip (gerenciador de pacotes Python)
- Git (opcional)

## 🚀 Instalação

1. Clone o repositório:
```bash
https://github.com/ClaudioAMF1/Banco-de-Dados.git
cd sistema-academia
```
2. Crie um ambiente virtual:
```bash
python -m venv venv
```
3. Ative o ambiente virtual:
   Windows:
   ```bash
   .\venv\Scripts\activate
   ```
   Linux/Mac:
   ```bash
   source venv/bin/activate
   ```
4. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 📁 Estrutura do Projeto
```
sistema_academia/
│
├── venv/
├── src/
│   ├── database/
│   │   ├── __init__.py
│   │   └── conexao.py
│   ├── paginas/
│   │   ├── __init__.py
│   │   ├── alunos.py
│   │   ├── aulas.py
│   │   ├── home.py
│   │   ├── matriculas.py
│   │   ├── modalidades.py
│   │   ├── pagamentos.py
│   │   ├── professores.py
│   │   ├── relatorios.py
│   │   └── views.py
│   └── utils/
│       ├── __init__.py
│       └── helper.py
├── .env
├── app.py
├── requirements.txt
└── readme.md
```

## ⚙️ Configuração do Banco de Dados

1. Execute o script SQL para criar o banco de dados, suas tabelas, informações e views:

[Scripts completo TP1.SQL](https://github.com/ClaudioAMF1/Banco-de-Dados/blob/main/Trabalhos%20Pr%C3%A1ticos/Trabalho%20Pr%C3%A1tico%201/Scripts%20completo%20TP1.sql)


2. Configure o arquivo [.env](https://github.com/ClaudioAMF1/Banco-de-Dados/blob/main/Trabalhos%20Pr%C3%A1ticos/Trabalho%20Pr%C3%A1tico%201/sistema-academia/.env):
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha
DB_NAME=academia
DB_PORT=3306
```

## 🖥 Executando o Sistema

1. Certifique-se que o MySQL está rodando
  
2. Ative o ambiente virtual:
```bash
.\venv\Scripts\activate # Windows
source venv/bin/activate # Linux/Mac
```

3. Execute o aplicativo:
```bash
streamlit run app.py
```

4. Acesse o sistema:
   - URL: http://localhost:8501
   - Usuário padrão: admin
   - Senha padrão: admin

## 🔍 Uso do Sistema

**Login**

- Use as credenciais padrão para primeiro acesso
- Altere a senha após o primeiro login
- Mantenha suas credenciais seguras

**Navegação**

- Use o menu lateral para acessar os módulos
- Cada módulo possui suas funcionalidades específicas
- Utilize os filtros para encontrar informações
- Os botões de ação estão claramente identificados
- Siga o fluxo de navegação indicado

**Módulos Principais**

- **Alunos**

  - Cadastre novos alunos
  - Gerencie matrículas
  - Visualize histórico
  - Acompanhe pagamentos
  - Registre avaliações

- **Professores**

  - Cadastre professores
  - Atribua turmas
  - Gerencie horários
  - Defina especializações

- **Aulas**

  - Crie novas turmas
  - Controle frequência
  - Monitore ocupação
  - Gerencie horários

- **Matrículas**

  - Registre matrículas
  - Gerencie planos
  - Controle vencimentos
  - Faça renovações

- **Financeiro**

  - Registre pagamentos
  - Acompanhe mensalidades
  - Gere relatórios
  - Visualize inadimplência

- **Views**

  - Acesse as principais views
  - Hórarios com maior ocupação
  - Melhores professores

- **Relatórios**

  - Acesse a seção de relatórios
  - Utilize os filtros disponíveis
  - Exporte dados em CSV/Excel
  - Visualize gráficos interativos
  - Analise métricas e KPIs
 
---

Desenvolvido para o trabalho final de Banco de Dados por Claudio Meireles - 2024/2

      
