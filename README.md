# 🎓 Sistema Acadêmico Integrado com Suporte de IA

> **Projeto Integrado Multidisciplinar (PIM II)** > Curso Superior de Tecnologia em Análise e Desenvolvimento de Sistemas - UNIP

## 📄 Sobre o Projeto

Este projeto consiste no desenvolvimento de um **Sistema Acadêmico Colaborativo** com foco na otimização de processos internos e melhoria da comunicação entre estudantes, professores e a instituição.

O sistema foi projetado para operar em rede local, reduzindo tarefas manuais e promovendo a transformação digital no ambiente acadêmico. Um dos grandes diferenciais é a integração com **Inteligência Artificial (Gemini)** para fornecer feedbacks motivacionais e suporte aos usuários.

---

## 🚀 Funcionalidades Principais

### 👥 Perfis de Acesso
O sistema possui controle de acesso seguro via níveis de usuário:
* **Administrador:** Gerenciamento de contas e configurações do sistema.
* **Secretaria/Coordenação:** Gestão administrativa de turmas, matrículas e alunos.
* **Professor:** Registro de diário eletrônico, lançamento de notas, controle de frequência e publicação de atividades.
* **Aluno:** Acesso ao portal para consulta de notas, frequência, materiais de aula e envio de atividades.

### 🛠️ Recursos do Sistema
* **Gestão Acadêmica:** CRUD completo (Criação, Leitura, Atualização e Exclusão) de turmas, alunos e disciplinas.
* **Diário Eletrônico:** Substituição de registros físicos por digitais para maior agilidade.
* **Integração com IA:** Utilização da API do Google Gemini para gerar feedbacks pedagógicos personalizados e mensagens motivacionais para os alunos.
* **Segurança:** Autenticação robusta com criptografia de senhas (Hash/Bcrypt) e tokens de sessão.
* **Interface Responsiva:** Design moderno com tema escuro (Dark Mode), adaptável para Desktop e dispositivos móveis.

---

## 💻 Tecnologias Utilizadas

O projeto foi desenvolvido seguindo a arquitetura **MVC (Model-View-Controller)** e o modelo **Cliente-Servidor**.

### Back-end
* ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) **Python 3**: Linguagem base do sistema.
* ![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white) **Flask**: Framework web utilizado para construção da API e rotas.
* **Google Generative AI**: Integração com o modelo Gemini para recursos de IA.

### Front-end
* ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white) **HTML5**
* ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white) **CSS3**
* ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black) **JavaScript**

### Banco de Dados
* ![MySQL](https://img.shields.io/badge/MySQL-005C84?style=flat&logo=mysql&logoColor=white) **MySQL**: Banco de dados relacional (modelagem normalizada até a 3FN).
* **Connector/Python**: Biblioteca para integração e manipulação de dados SQL via script.

---

## ⚙️ Instalação e Execução

Siga os passos abaixo para rodar o projeto em sua máquina local.

### Pré-requisitos
* Python 3.x instalado.
* MySQL Server instalado e rodando.
* Chave de API do Google Gemini (necessária para as funcionalidades de IA).

### Passo a Passo

1.  **Clone o repositório**
    ```bash
    git clone [https://github.com/SoRickDev/PIM2.git](https://github.com/SoRickDev/PIM2.git)
    cd PIM2
    ```

2.  **Crie e ative o ambiente virtual**
    ```bash
    # Criação do ambiente
    python -m venv venv

    # Ativação no Windows:
    venv\Scripts\activate

    # Ativação no Linux/Mac:
    source venv/bin/activate
    ```

3.  **Instale as dependências**
    ```bash
    pip install mysql-connector-python bcrypt flask google-generativeai pandas numpy
    ```

4.  **Configure o Banco de Dados**
    * Acesse a pasta `Database/`.
    * Execute o script `database.sql` no seu gerenciador MySQL para criar as tabelas.
    * Execute o script `popular_dados.sql` para inserir os dados iniciais de teste.
    * *Atenção:* Verifique se as credenciais do banco (usuário/senha) no arquivo `config_db` (dentro do código Python) correspondem às da sua máquina.

5.  **Execute a aplicação**
    ```bash
    python app.py
    ```
    O sistema estará acessível em: `http://127.0.0.1:5000`

---

## 👨‍💻 Autores

Projeto desenvolvido pela equipe de Análise e Desenvolvimento de Sistemas (UNIP Rio Preto/SP - 2025):

* **Aldenor Dantas dos Santos** (RA: R863824)
* **Rafael Henrique Jubilato Batista** (RA: H70CJG2)
* **Hugo Vinicius Brito Pereira** (RA: H233CA2)
* **Leonardo Socreppa de Souza** (RA: R839JG7)
* **Eduardo Felix dos Santos Taino** (RA: R841FI9)
* **Rickson Pedreira** (RA: H520BA0)

---

## 📚 Status do Projeto
✅ **Concluído** (Entrega do PIM - 2º Semestre)