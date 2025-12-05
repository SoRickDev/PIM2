# 🎓 Sistema Acadêmico Integrado com Suporte de IA

> [cite_start]Projeto Integrado Multidisciplinar (PIM II) - Análise e Desenvolvimento de Sistemas (UNIP) [cite: 1]

## 📄 Sobre o Projeto
[cite_start]Este projeto consiste no desenvolvimento de um **Sistema Acadêmico Colaborativo** com foco na otimização de processos internos e melhoria da comunicação entre estudantes, professores e a instituição[cite: 2].

[cite_start]O sistema foi projetado para operar em rede local, reduzindo tarefas manuais e promovendo a transformação digital no ambiente acadêmico[cite: 4, 6, 22]. [cite_start]Um dos diferenciais é a integração com **Inteligência Artificial (Gemini)** para fornecer feedbacks motivacionais e suporte aos usuários[cite: 24, 138].

---

## 🚀 Funcionalidades Principais

### 👥 Perfis de Acesso
[cite_start]O sistema possui controle de acesso via níveis de usuário (criptografia com Bcrypt)[cite: 34, 139]:
* **Administrador:** Gerenciamento de contas e sistema.
* **Secretaria/Coordenação:** Gestão de turmas e alunos.
* **Professor:** Registro de diário, notas, frequência e publicação de atividades.
* [cite_start]**Aluno:** Consulta de notas, frequência, materiais e upload de atividades[cite: 34, 48].

### 🛠️ Recursos do Sistema
* [cite_start]**Gestão Acadêmica:** CRUD completo de turmas, alunos e disciplinas[cite: 49].
* [cite_start]**Diário Eletrônico:** Substituição de registros físicos por digitais[cite: 51].
* [cite_start]**Integração com IA:** Uso da API do Google Gemini para gerar feedbacks pedagógicos personalizados e motivacionais[cite: 138].
* [cite_start]**Segurança:** Autenticação segura com hash de senhas e tokens de sessão[cite: 139, 148].
* [cite_start]**Interface Responsiva:** Design moderno (Dark Mode) adaptável para Desktop e Mobile[cite: 44, 145].

---

## 💻 Tecnologias Utilizadas

[cite_start]O projeto segue a arquitetura **MVC (Model-View-Controller)** e **Cliente-Servidor**[cite: 121, 136].

### Back-end
* [cite_start]![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) **Python 3**: Linguagem principal[cite: 81].
* [cite_start]![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white) **Flask**: Framework web para API e rotas[cite: 118].
* [cite_start]**Google Generative AI**: Integração com modelo Gemini[cite: 91].

### Front-end
* ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white) ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
* [cite_start]Interface desenvolvida com foco em acessibilidade e usabilidade[cite: 43].

### Banco de Dados
* [cite_start]![MySQL](https://img.shields.io/badge/MySQL-005C84?style=for-the-badge&logo=mysql&logoColor=white) **MySQL**: Banco de dados relacional normalizado até a 3FN[cite: 70, 88].
* [cite_start]**Connector/Python**: Para manipulação de dados via script[cite: 81].

---

## ⚙️ Como Executar o Projeto

### Pré-requisitos
* Python 3.x instalado.
* MySQL Server rodando.
* Chave de API do Google Gemini (para funcionalidades de IA).

### Passo a Passo

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/SoRickDev/PIM2.git](https://github.com/SoRickDev/PIM2.git)
    cd PIM2
    ```

2.  [cite_start]**Crie e ative o ambiente virtual:** [cite: 119]
    ```bash
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # Linux/Mac:
    source venv/bin/activate
    ```

3.  [cite_start]**Instale as dependências:** [cite: 119]
    ```bash
    pip install mysql-connector-python bcrypt flask google-generativeai pandas numpy
    ```

4.  **Configure o Banco de Dados:**
    * [cite_start]Execute o script `database.sql` na pasta `Database/` para criar a estrutura[cite: 115].
    * [cite_start]Execute `popular_dados.sql` para inserir dados de teste[cite: 132].
    * [cite_start]*Nota:* Configure suas credenciais do MySQL no arquivo `config_db` dentro do código Python[cite: 138].

5.  [cite_start]**Inicie o Servidor:** [cite: 118]
    ```bash
    python app.py
    ```
    O sistema estará rodando em: `http://127.0.0.1:5000`

---

## 👨‍💻 Autores

[cite_start]Este projeto foi desenvolvido pelos alunos do curso de Análise e Desenvolvimento de Sistemas da UNIP[cite: 1]:

* **Aldenor Dantas dos Santos** (RA: R863824)
* **Rafael Henrique Jubilato Batista** (RA: H70CJG2)
* **Hugo Vinicius Brito Pereira** (RA: H233CA2)
* **Leonardo Socreppa de Souza** (RA: R839JG7)
* **Eduardo Felix dos Santos Taino** (RA: R841FI9)
* **Rickson Pedreira** (RA: H520BA0)

---

## 📚 Documentação
[cite_start]A modelagem do sistema inclui Diagramas de Caso de Uso UML, Diagramas Conceituais de Banco de Dados e documentação de requisitos funcionais/não funcionais[cite: 3, 34, 61].

---
*Status do Projeto: ✅ Concluído (PIM 2º Semestre)*