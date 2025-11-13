CREATE DATABASE IF NOT EXISTS CADASTRO;
USE CADASTRO;

-- -----------------------------------------------------
-- Tabela 1: niveis_user 
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS niveis_user (
    id_nivel INT AUTO_INCREMENT,
    nome_nivel VARCHAR(20) NOT NULL,
    PRIMARY KEY (id_nivel),
    UNIQUE (nome_nivel)
);

-- Dados essenciais do sistema
INSERT INTO niveis_user (nome_nivel) VALUES ('admin'), ('professor'), ('aluno');

-- -----------------------------------------------------
-- Tabela 2: cursos 
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS cursos (
    id_curso INT AUTO_INCREMENT,
    nome_curso VARCHAR(50) NOT NULL,
    PRIMARY KEY (id_curso),
    UNIQUE (nome_curso)
);

-- -----------------------------------------------------
-- Tabela 3: usuario 
-- -----------------------------------------------------
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
    UNIQUE (cpf),
    UNIQUE (telefone),
    UNIQUE (email),
    FOREIGN KEY (id_nivel) REFERENCES niveis_user(id_nivel)
);

-- -----------------------------------------------------
-- Tabela 4: dados_aluno 
-- -----------------------------------------------------
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

-- -----------------------------------------------------
-- Tabela 5: disciplinas
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS disciplinas (
    id_disciplina INT AUTO_INCREMENT,
    nome_disciplina VARCHAR(100) NOT NULL,
    id_curso INT NOT NULL,
    
    PRIMARY KEY (id_disciplina),
    FOREIGN KEY (id_curso) REFERENCES cursos(id_curso)
);

-- -----------------------------------------------------
-- Tabela 6: turmas
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS turmas (
    id_turma INT AUTO_INCREMENT,
    id_disciplina INT NOT NULL,
    id_professor INT NOT NULL, 
    ano_semestre VARCHAR(10) NOT NULL,
    
    PRIMARY KEY (id_turma),
    FOREIGN KEY (id_disciplina) REFERENCES disciplinas(id_disciplina),
    FOREIGN KEY (id_professor) REFERENCES usuario(id_user)
);

-- -----------------------------------------------------
-- Tabela 7: turma_alunos 
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS turma_alunos (
    id_turma INT NOT NULL,
    id_aluno INT NOT NULL, 
    nota_final DECIMAL(4, 2) NULL, 
    frequencia INT NULL,
    
    PRIMARY KEY (id_turma, id_aluno),
    FOREIGN KEY (id_turma) REFERENCES turmas(id_turma),
    FOREIGN KEY (id_aluno) REFERENCES dados_aluno(id_user) 
);

-- -----------------------------------------------------
-- Tabela 8: aulas_diario
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS aulas_diario (
    id_aula INT AUTO_INCREMENT,
    id_turma INT NOT NULL,
    data_aula DATE NOT NULL,
    conteudo_ministrado TEXT NULL, 
    
    PRIMARY KEY (id_aula),
    FOREIGN KEY (id_turma) REFERENCES turmas(id_turma)
        ON DELETE CASCADE
);

-- -----------------------------------------------------
-- Tabela 9: aulas_presenca
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS aulas_presenca (
    id_aula INT NOT NULL,
    id_aluno INT NOT NULL, 
    presente BOOLEAN NOT NULL DEFAULT FALSE,
    
    PRIMARY KEY (id_aula, id_aluno),
    FOREIGN KEY (id_aula) REFERENCES aulas_diario(id_aula)
        ON DELETE CASCADE,
    FOREIGN KEY (id_aluno) REFERENCES dados_aluno(id_user)
        ON DELETE CASCADE
);