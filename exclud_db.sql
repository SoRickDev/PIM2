USE CADASTRO;

-- Garante que ao deletar usuário, os dados de aluno sumam
ALTER TABLE dados_aluno
DROP FOREIGN KEY dados_aluno_ibfk_1;

ALTER TABLE dados_aluno
ADD CONSTRAINT dados_aluno_ibfk_1
FOREIGN KEY (id_user) REFERENCES usuario(id_user) ON DELETE CASCADE;

-- Garante que ao deletar usuário, as turmas/notas sumam
ALTER TABLE turma_alunos
DROP FOREIGN KEY turma_alunos_ibfk_2;

ALTER TABLE turma_alunos
ADD CONSTRAINT turma_alunos_ibfk_2
FOREIGN KEY (id_aluno) REFERENCES dados_aluno(id_user) ON DELETE CASCADE;