-- ==========================================================
-- 1. LIMPEZA E CRIAÇÃO DO BANCO (O TERRENO)
-- ==========================================================
DROP DATABASE IF EXISTS CADASTRO;
CREATE DATABASE IF NOT EXISTS CADASTRO;
USE CADASTRO;

-- ==========================================================
-- 2. CRIAÇÃO DAS TABELAS (AS PAREDES)
-- ==========================================================

-- Tabela Niveis
CREATE TABLE IF NOT EXISTS niveis_user (
    id_nivel INT AUTO_INCREMENT,
    nome_nivel VARCHAR(20) NOT NULL,
    PRIMARY KEY (id_nivel),
    UNIQUE (nome_nivel)
);
-- Inserir niveis obrigatórios agora
INSERT INTO niveis_user (nome_nivel) VALUES ('admin'), ('professor'), ('aluno');

-- Tabela Cursos
CREATE TABLE IF NOT EXISTS cursos (
    id_curso INT AUTO_INCREMENT,
    nome_curso VARCHAR(50) NOT NULL,
    PRIMARY KEY (id_curso),
    UNIQUE (nome_curso)
);

-- Tabela Usuario
CREATE TABLE IF NOT EXISTS usuario (
    id_user INT AUTO_INCREMENT,
    cpf CHAR(11) NOT NULL,
    nome VARCHAR(50) NOT NULL,
    sexo VARCHAR(15) NOT NULL,
    datanasc DATE NOT NULL,
    telefone VARCHAR(15) NOT NULL,
    email VARCHAR(50) NOT NULL,
    senha_hash VARCHAR(255) NOT NULL, 
    id_nivel INT,
    PRIMARY KEY (id_user),
    UNIQUE (cpf), UNIQUE (telefone), UNIQUE (email),
    FOREIGN KEY (id_nivel) REFERENCES niveis_user(id_nivel)
);

-- Tabela Dados Aluno
CREATE TABLE IF NOT EXISTS dados_aluno (
    id_user INT,
    id_curso INT NOT NULL,
    matricula VARCHAR(20) NOT NULL,
    status_aluno VARCHAR(20) NOT NULL DEFAULT 'Ativo',
    data_ingresso DATE NOT NULL,
    PRIMARY KEY (id_user),
    FOREIGN KEY (id_user) REFERENCES usuario(id_user),
    FOREIGN KEY (id_curso) REFERENCES cursos(id_curso),
    UNIQUE (matricula)
);

-- Tabela Disciplinas
CREATE TABLE IF NOT EXISTS disciplinas (
    id_disciplina INT AUTO_INCREMENT,
    nome_disciplina VARCHAR(100) NOT NULL,
    id_curso INT NOT NULL,
    PRIMARY KEY (id_disciplina),
    FOREIGN KEY (id_curso) REFERENCES cursos(id_curso)
);

-- Tabela Turmas
CREATE TABLE IF NOT EXISTS turmas (
    id_turma INT AUTO_INCREMENT,
    id_disciplina INT NOT NULL,
    id_professor INT NOT NULL, 
    ano_semestre VARCHAR(10) NOT NULL,
    PRIMARY KEY (id_turma),
    FOREIGN KEY (id_disciplina) REFERENCES disciplinas(id_disciplina),
    FOREIGN KEY (id_professor) REFERENCES usuario(id_user)
);

-- Tabela Turma_Alunos
CREATE TABLE IF NOT EXISTS turma_alunos (
    id_turma INT NOT NULL,
    id_aluno INT NOT NULL, 
    nota_final DECIMAL(4, 2) NULL, 
    frequencia INT NULL,
    PRIMARY KEY (id_turma, id_aluno),
    FOREIGN KEY (id_turma) REFERENCES turmas(id_turma),
    FOREIGN KEY (id_aluno) REFERENCES dados_aluno(id_user) 
);

-- Tabelas de Aulas (Diario e Presença)
CREATE TABLE IF NOT EXISTS aulas_diario (
    id_aula INT AUTO_INCREMENT,
    id_turma INT NOT NULL,
    data_aula DATE NOT NULL,
    conteudo_ministrado TEXT NULL, 
    PRIMARY KEY (id_aula),
    FOREIGN KEY (id_turma) REFERENCES turmas(id_turma) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS aulas_presenca (
    id_aula INT NOT NULL,
    id_aluno INT NOT NULL, 
    presente BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (id_aula, id_aluno),
    FOREIGN KEY (id_aula) REFERENCES aulas_diario(id_aula) ON DELETE CASCADE,
    FOREIGN KEY (id_aluno) REFERENCES dados_aluno(id_user) ON DELETE CASCADE
);

-- ==========================================================
-- 3. INSERÇÃO DOS DADOS (OS MÓVEIS)
-- ==========================================================

-- Cursos
INSERT INTO cursos (nome_curso) VALUES
('Análise e Desenvolvimento de Sistemas'),
('Engenharia de Software'),
('Ciência da Computação'),
('Sistemas de Informação'),
('Banco de Dados');

-- Disciplinas
INSERT INTO disciplinas (nome_disciplina, id_curso) VALUES
('Algoritmos e Lógica de Programação', 1), ('Estruturas de Dados', 1), ('Banco de Dados I', 1), ('Desenvolvimento Web', 1), ('Engenharia de Software I', 1),
('Requisitos de Software', 2), ('Arquitetura de Software', 2), ('Banco de Dados II', 2), ('Testes e Qualidade de Software', 2), ('Gerência de Projetos', 2),
('Programação Orientada a Objetos', 3), ('Computação Gráfica', 3), ('Inteligência Artificial', 3), ('Sistemas Operacionais', 3), ('Redes de Computadores', 3),
('Gestão de Sistemas', 4), ('Análise de Dados', 4), ('Desenvolvimento Mobile', 4), ('Cloud Computing', 4), ('Segurança da Informação', 4),
('Modelagem de Dados', 5), ('Administração de Banco de Dados', 5), ('SQL Avançado', 5), ('Big Data', 5), ('Data Mining', 5);

-- USUÁRIOS (Admin ID 1 + Professores IDs 2 a 6)
INSERT INTO usuario (cpf, nome, sexo, datanasc, telefone, email, senha_hash, id_nivel) VALUES
('11111111111', 'Administrador', 'Outro', '1990-01-01', '000000000', 'admin@admin.com', '$2b$12$optQOVxJ/WTtkq.NqjZZ4u1io50HD7TYHRkXR29gvpg3h3m2QJMWK', 1),
('22233344455', 'Prof. Ana Souza', 'Feminino', '1980-03-05', '999111222', 'ana.prof@example.com', '$2b$12$KCm6cOylO1eCwFkaF5AJTOOW0M/t/wiFIls97xAOrM62E5LW0TACC', 2),
('33344455566', 'Prof. Carlos Lima', 'Masculino', '1985-07-22', '999222333', 'carlos.prof@example.com', '$2b$12$x0bVsQkrLfzoMtBup9XI0.tY3Cq4u3kdqxqa4BGGshgI9vuu4q7Ve', 2),
('44455566677', 'Prof. Júlia Mendes', 'Feminino', '1988-09-12', '999333444', 'julia.prof@example.com', '$2b$12$JK.pef2aRhG94oeHPwKG9Ots1hrRqVoy0fDGHCHL/fpqvwlMjVsnS', 2),
('55566677788', 'Prof. Paulo Santos', 'Masculino', '1990-11-30', '999444555', 'paulo.prof@example.com', '$2b$12$roQG4iOovOOH8h1sqenYbOWAkC1ClFff6ujShE7DcoWZpxTz94fK2', 2),
('66677788899', 'Prof. Laura Nogueira', 'Feminino', '1992-02-10', '999555666', 'laura.prof@example.com', '$2b$12$p8GjLs9KYBaKw6Z/XubnPu3y37syodYYeerp6GaRP..gepMtQhwqO', 2);

-- Turmas

INSERT INTO turmas (id_disciplina, id_professor, ano_semestre) VALUES
(1, 2, '2025/1'), (2, 2, '2025/2'),
(6, 3, '2025/1'), (7, 3, '2025/2'),
(11, 4, '2025/1'), (12, 4, '2025/2'),
(16, 5, '2025/1'), (17, 5, '2025/2'),
(21, 6, '2025/1'), (22, 6, '2025/2');