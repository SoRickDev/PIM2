import bcrypt

# Configuração das senhas desejadas (Nome + 1234)
usuarios = [
    # Nível 1 - Admin
    {"nome": "Administrador", "email": "admin@admin.com", "senha_plana": "Admin1234", "cpf": "11111111111", "sexo": "Outro", "nasc": "1990-01-01", "tel": "000000000", "nivel": 1},
    
    # Nível 2 - Professores
    {"nome": "Prof. Ana Souza", "email": "ana.prof@example.com", "senha_plana": "Ana1234", "cpf": "22233344455", "sexo": "Feminino", "nasc": "1980-03-05", "tel": "999111222", "nivel": 2},
    {"nome": "Prof. Carlos Lima", "email": "carlos.prof@example.com", "senha_plana": "Carlos1234", "cpf": "33344455566", "sexo": "Masculino", "nasc": "1985-07-22", "tel": "999222333", "nivel": 2},
    {"nome": "Prof. Júlia Mendes", "email": "julia.prof@example.com", "senha_plana": "Julia1234", "cpf": "44455566677", "sexo": "Feminino", "nasc": "1988-09-12", "tel": "999333444", "nivel": 2},
    {"nome": "Prof. Paulo Santos", "email": "paulo.prof@example.com", "senha_plana": "Paulo1234", "cpf": "55566677788", "sexo": "Masculino", "nasc": "1990-11-30", "tel": "999444555", "nivel": 2},
    {"nome": "Prof. Laura Nogueira", "email": "laura.prof@example.com", "senha_plana": "Laura1234", "cpf": "66677788899", "sexo": "Feminino", "nasc": "1992-02-10", "tel": "999555666", "nivel": 2}
]

print("-- COPIE O BLOCO ABAIXO E SUBSTITUA NO SEU ARQUIVO SQL --")
print("INSERT INTO usuario (cpf, nome, sexo, datanasc, telefone, email, senha_hash, id_nivel) VALUES")

linhas_sql = []

for u in usuarios:
    # Gera o hash seguro
    senha_bytes = u["senha_plana"].encode('utf-8')
    salt = bcrypt.gensalt()
    hash_senha = bcrypt.hashpw(senha_bytes, salt).decode('utf-8')
    
    # Formata a linha SQL
    linha = f"('{u['cpf']}', '{u['nome']}', '{u['sexo']}', '{u['nasc']}', '{u['tel']}', '{u['email']}', '{hash_senha}', {u['nivel']})"
    linhas_sql.append(linha)

# Junta tudo com vírgula e finaliza com ponto e vírgula
print(",\n".join(linhas_sql) + ";")
print("-- FIM DO BLOCO --")