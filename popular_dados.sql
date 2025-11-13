USE CADASTRO;

-- -----------------------------------------------------
-- CURSOS
-- -----------------------------------------------------
INSERT INTO cursos (nome_curso) VALUES
('Análise e Desenvolvimento de Sistemas'),
('Engenharia de Software'),
('Ciência da Computação'),
('Sistemas de Informação'),
('Banco de Dados');

-- -----------------------------------------------------
-- DISCIPLINAS (5 por curso)
-- -----------------------------------------------------
INSERT INTO disciplinas (nome_disciplina, id_curso) VALUES
-- Curso 1
('Algoritmos e Lógica de Programação', 1),
('Estruturas de Dados', 1),
('Banco de Dados I', 1),
('Desenvolvimento Web', 1),
('Engenharia de Software I', 1),

-- Curso 2
('Requisitos de Software', 2),
('Arquitetura de Software', 2),
('Banco de Dados II', 2),
('Testes e Qualidade de Software', 2),
('Gerência de Projetos', 2),

-- Curso 3
('Programação Orientada a Objetos', 3),
('Computação Gráfica', 3),
('Inteligência Artificial', 3),
('Sistemas Operacionais', 3),
('Redes de Computadores', 3),

-- Curso 4
('Gestão de Sistemas', 4),
('Análise de Dados', 4),
('Desenvolvimento Mobile', 4),
('Cloud Computing', 4),
('Segurança da Informação', 4),

-- Curso 5
('Modelagem de Dados', 5),
('Administração de Banco de Dados', 5),
('SQL Avançado', 5),
('Big Data', 5),
('Data Mining', 5);

-- -----------------------------------------------------
-- PROFESSORES DE EXEMPLO (id_nivel=2)
-- -----------------------------------------------------
INSERT INTO usuario (cpf, nome, sexo, datanasc, telefone, email, senha_hash, id_nivel)
VALUES
('22233344455', 'Prof. Ana Souza', 'Feminino', '1980-03-05', '999111222', 'ana.prof@example.com',
 '$2b$12$AXUcJmC5ib9NeAFta6qoUuNqxevdn1J4H2g.aEixRYNgDi2BJtlT.', 2),
('33344455566', 'Prof. Carlos Lima', 'Masculino', '1985-07-22', '999222333', 'carlos.prof@example.com',
 '$2b$12$AXUcJmC5ib9NeAFta6qoUuNqxevdn1J4H2g.aEixRYNgDi2BJtlT.', 2),
('44455566677', 'Prof. Júlia Mendes', 'Feminino', '1988-09-12', '999333444', 'julia.prof@example.com',
 '$2b$12$AXUcJmC5ib9NeAFta6qoUuNqxevdn1J4H2g.aEixRYNgDi2BJtlT.', 2),
('55566677788', 'Prof. Paulo Santos', 'Masculino', '1990-11-30', '999444555', 'paulo.prof@example.com',
 '$2b$12$AXUcJmC5ib9NeAFta6qoUuNqxevdn1J4H2g.aEixRYNgDi2BJtlT.', 2),
('66677788899', 'Prof. Laura Nogueira', 'Feminino', '1992-02-10', '999555666', 'laura.prof@example.com',
 '$2b$12$AXUcJmC5ib9NeAFta6qoUuNqxevdn1J4H2g.aEixRYNgDi2BJtlT.', 2);

-- -----------------------------------------------------
-- TURMAS (2 por curso)
-- Nota: Os IDs dos professores (2, 3, 4, 5, 6) 
-- correspondem aos IDs gerados no INSERT acima.
-- -----------------------------------------------------
INSERT INTO turmas (id_disciplina, id_professor, ano_semestre)
VALUES
-- Curso 1 (ADS) - Prof. Ana (ID 2)
(1, 2, '2025/1'), (2, 2, '2025/2'),
-- Curso 2 (Eng. Soft) - Prof. Carlos (ID 3)
(6, 3, '2025/1'), (7, 3, '2025/2'),
-- Curso 3 (C. Comp) - Prof. Júlia (ID 4)
(11, 4, '2025/1'), (12, 4, '2025/2'),
-- Curso 4 (SI) - Prof. Paulo (ID 5)
(16, 5, '2025/1'), (17, 5, '2025/2'),
-- Curso 5 (BD) - Prof. Laura (ID 6)
(21, 6, '2025/1'), (22, 6, '2025/2');