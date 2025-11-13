import os
import pymysql
import bcrypt
import random
import jwt  # Adicionado para JWT
from datetime import date, datetime, timedelta  # Adicionado datetime e timedelta
from functools import wraps  # Adicionado para o decorator
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ======================================================
# 🔑 CONFIGURAÇÃO DE CHAVE SECRETA (Modificado)
# ======================================================
# ATENÇÃO: Troque "SUA_CHAVE_SECRETA_MUITO_FORTE_E_ALEATORIA" por uma string segura!
# Você pode gerar uma no terminal com: python -c "import os; print(os.urandom(24).hex())"
app.config['SECRET_KEY'] = "SUA_CHAVE_SECRETA_MUITO_FORTE_E_ALEATORIA"

# ------------------------------------------------------
# 🔧 CONFIGURAÇÃO DO BANCO DE DADOS
# ------------------------------------------------------
db_config = {
    "host": "localhost",
    "user": "root",
    "password": os.getenv("DB_PASSWORD", "280802"),
    "database": "CADASTRO"
}


# ======================================================
# 🔐 LOGIN (Modificado com JWT)
# ======================================================
@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return jsonify({"erro": "Email e senha são obrigatórios"}), 400

    conn = None
    try:
        conn = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM usuario WHERE email = %s", (email,))
        usuario = cursor.fetchone()

        if not usuario:
            return jsonify({"erro": "Usuário não encontrado"}), 401

        if not bcrypt.checkpw(senha.encode("utf-8"), usuario["senha_hash"].encode("utf-8")):
            return jsonify({"erro": "Senha incorreta"}), 401

        # Geração do Token JWT (Modificado)
        exp_time = datetime.utcnow() + timedelta(hours=24)
        
        payload = {
            "id_user": usuario["id_user"],
            "nome": usuario["nome"],
            "id_nivel": usuario["id_nivel"],
            "exp": exp_time  # Data de expiração
        }

        # Gera o token
        token = jwt.encode(
            payload,
            app.config["SECRET_KEY"], # Usa a chave secreta
            algorithm="HS256"
        )

        # Retorna o token ao invés dos dados do usuário (Modificado)
        return jsonify({"mensagem": "Login bem-sucedido", "token": token}), 200

    except Exception as err:
        print("Erro MySQL:", err)
        return jsonify({"erro": "Erro no servidor ou banco de dados"}), 500
    finally:
        if conn:
            conn.close()


# ======================================================
# 🛡️ GUARDIÃO DE ROTA (DECORATOR) (Adicionado)
# ======================================================
# Este decorator vai "embrulhar" nossas rotas seguras
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # 1. Verifica se o token foi enviado no cabeçalho 'Authorization'
        if "Authorization" in request.headers:
            # O formato esperado é "Bearer <token>"
            try:
                token = request.headers["Authorization"].split(" ")[1]
            except IndexError:
                return jsonify({"erro": "Formato de token inválido. Esperado 'Bearer <token>'"}), 401

        if not token:
            return jsonify({"erro": "Token é obrigatório"}), 401

        try:
            # 2. Tenta decodificar o token
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            
            # 3. Busca o usuário no banco (para garantir que ele ainda existe)
            conn = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)
            cursor = conn.cursor()
            cursor.execute("SELECT id_user, nome, email, id_nivel FROM usuario WHERE id_user = %s", (data["id_user"],))
            current_user = cursor.fetchone()

            if not current_user:
                 conn.close()
                 return jsonify({"erro": "Usuário do token não encontrado"}), 401
            
            # 4. Passa os dados do usuário para a rota
            # Colocamos o usuário na 'kwargs' para a próxima função receber
            kwargs["current_user"] = current_user

        except jwt.ExpiredSignatureError:
            return jsonify({"erro": "Token expirou"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"erro": "Token inválido"}), 401
        except Exception as e:
            print(f"Erro no decorator: {e}")
            return jsonify({"erro": "Erro interno ao validar token"}), 500
        finally:
            if 'conn' in locals() and conn:
                conn.close()
        
        # 5. Se tudo estiver OK, executa a rota original
        return f(*args, **kwargs)

    return decorated


# ======================================================
# 📝 CADASTRO DE USUÁRIOS (Rota Pública)
# ======================================================
@app.route("/api/auth/register", methods=["POST"])
def register():
    # ... (Sem alterações nesta rota, ela deve ser pública)
    data = request.get_json()
    nome = data.get("nome")
    cpf = data.get("cpf")
    datanasc = data.get("datanasc")
    telefone = data.get("telefone")
    email = data.get("email")
    senha = data.get("senha")
    id_nivel = int(data.get("id_nivel"))
    id_curso = data.get("id_curso")

    if not all([nome, cpf, datanasc, telefone, email, senha, id_nivel]):
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400

    conn = None
    try:
        senha_hash = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        conn = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()

        # Inserir usuário
        cursor.execute("""
            INSERT INTO usuario (cpf, nome, sexo, datanasc, telefone, email, senha_hash, id_nivel)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (cpf, nome, "Não informado", datanasc, telefone, email, senha_hash, id_nivel))
        conn.commit()

        id_user = cursor.lastrowid

        # Se for aluno → inserir dados acadêmicos + matrícula + distribuir em turmas
        if id_nivel == 3 and id_curso:
            matricula = f"A{random.randint(10000, 99999)}"
            cursor.execute("""
                INSERT INTO dados_aluno (id_user, id_curso, matricula, status_aluno, data_ingresso)
                VALUES (%s, %s, %s, %s, %s)
            """, (id_user, id_curso, matricula, "Ativo", date.today()))
            conn.commit()

            # Encontrar até 2 turmas disponíveis do curso
            cursor.execute("""
                SELECT t.id_turma 
                FROM turmas t
                JOIN disciplinas d ON t.id_disciplina = d.id_disciplina
                WHERE d.id_curso = %s
                LIMIT 2
            """, (id_curso,))
            turmas = cursor.fetchall()

            for t in turmas:
                cursor.execute("""
                    INSERT INTO turma_alunos (id_turma, id_aluno, nota_final, frequencia)
                    VALUES (%s, %s, NULL, NULL)
                """, (t["id_turma"], id_user))
            conn.commit()

        return jsonify({"mensagem": "Usuário cadastrado com sucesso!"}), 201

    except pymysql.err.IntegrityError as e:
        print("Erro de integridade:", e)
        return jsonify({"erro": "Email ou CPF já cadastrados."}), 400
    except Exception as err:
        print("Erro MySQL:", err)
        return jsonify({"erro": "Erro no servidor ou banco de dados"}), 500
    finally:
        if conn:
            conn.close()


# ======================================================
# 📚 LISTAR CURSOS (Rota Pública)
# ======================================================
@app.route("/api/cursos", methods=["GET"])
def listar_cursos():
    # ... (Sem alterações nesta rota, necessária para o cadastro)
    try:
        conn = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()
        cursor.execute("SELECT id_curso, nome_curso FROM cursos")
        cursos = cursor.fetchall()
        return jsonify(cursos), 200
    except Exception as err:
        print("Erro MySQL:", err)
        return jsonify({"erro": "Erro ao buscar cursos"}), 500
    finally:
        if conn:
            conn.close()


# ======================================================
# 👩‍🏫 PROFESSOR - TURMAS E ALUNOS (Modificado com JWT)
# ======================================================
@app.route("/api/professor/turmas", methods=["GET"]) # Modificado: URL simplificada
@token_required # Modificado: Rota protegida
def turmas_professor(current_user): # Modificado: Recebe 'current_user' do token
    
    # Verifica se o usuário logado é um professor (id_nivel = 2)
    if current_user["id_nivel"] != 2:
        return jsonify({"erro": "Acesso não autorizado. Rota para professores."}), 403

    id_professor = current_user["id_user"] # Modificado: ID vem do token

    try:
        conn = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                t.id_turma, 
                d.nome_disciplina, 
                c.nome_curso, 
                t.ano_semestre
            FROM turmas t
            JOIN disciplinas d ON t.id_disciplina = d.id_disciplina
            JOIN cursos c ON d.id_curso = c.id_curso
            WHERE t.id_professor = %s
        """, (id_professor,)) # Modificado: usa id_professor do token
        turmas = cursor.fetchall()
        return jsonify(turmas), 200
    except Exception as err:
        print("Erro MySQL:", err)
        return jsonify({"erro": "Erro ao buscar turmas"}), 500
    finally:
        if conn:
            conn.close()


@app.route("/api/professor/turmas/<int:id_turma>/alunos", methods=["GET"])
@token_required # Modificado: Rota protegida
def alunos_da_turma(current_user, id_turma): # Modificado: Recebe 'current_user'
    
    if current_user["id_nivel"] != 2:
        return jsonify({"erro": "Acesso não autorizado."}), 403
    
    # (Opcional: verificar se este professor realmente dá aula para esta turma)

    try:
        conn = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                u.id_user,
                u.nome,
                u.email,
                da.matricula,
                ta.nota_final,
                ta.frequencia
            FROM turma_alunos ta
            JOIN usuario u ON ta.id_aluno = u.id_user
            JOIN dados_aluno da ON u.id_user = da.id_user
            WHERE ta.id_turma = %s
        """, (id_turma,))
        alunos = cursor.fetchall()
        return jsonify(alunos), 200
    except Exception as err:
        print("Erro MySQL:", err)
        return jsonify({"erro": "Erro ao buscar alunos"}), 500
    finally:
        if conn:
            conn.close()


@app.route("/api/professor/turmas/<int:id_turma>/alunos/<int:id_aluno>", methods=["PUT"])
@token_required # Modificado: Rota protegida
def atualizar_aluno(current_user, id_turma, id_aluno): # Modificado: Recebe 'current_user'
    
    if current_user["id_nivel"] != 2:
        return jsonify({"erro": "Acesso não autorizado."}), 403

    # (Opcional: verificar se este professor realmente dá aula para esta turma)

    data = request.get_json()
    nota = data.get("nota_final")
    frequencia = data.get("frequencia")

    if nota is None or frequencia is None:
        return jsonify({"erro": "Nota e frequência são obrigatórias"}), 400

    try:
        conn = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE turma_alunos
            SET nota_final = %s, frequencia = %s
            WHERE id_turma = %s AND id_aluno = %s
        """, (nota, frequencia, id_turma, id_aluno))
        
        if cursor.rowcount == 0:
             conn.commit()
             return jsonify({"erro": "Aluno ou turma não encontrado"}), 404

        conn.commit()
        return jsonify({"mensagem": "Nota e frequência atualizadas com sucesso!"}), 200

    except Exception as err:
        print("Erro MySQL:", err)
        return jsonify({"erro": "Erro ao lançar nota"}), 500
    finally:
        if conn:
            conn.close()


# ======================================================
# 🎓 ALUNO - DADOS E TURMAS (Modificado com JWT)
# ======================================================
@app.route("/api/aluno/dados", methods=["GET"]) # Modificado: URL simplificada
@token_required # Modificado: Rota protegida
def dados_aluno(current_user): # Modificado: Recebe 'current_user'
    
    if current_user["id_nivel"] != 3:
        return jsonify({"erro": "Acesso não autorizado. Rota para alunos."}), 403
        
    id_user = current_user["id_user"] # Modificado: ID vem do token

    try:
        conn = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT da.matricula, da.status_aluno, c.nome_curso
            FROM dados_aluno da
            JOIN cursos c ON da.id_curso = c.id_curso
            WHERE da.id_user = %s
        """, (id_user,)) # Modificado: usa id_user do token
        dados = cursor.fetchone()
        if not dados:
            return jsonify({"erro": "Aluno não encontrado"}), 404
        return jsonify(dados), 200
    except Exception as err:
        print("Erro MySQL:", err)
        return jsonify({"erro": "Erro ao buscar dados do aluno"}), 500
    finally:
        if conn:
            conn.close()


@app.route("/api/aluno/turmas", methods=["GET"]) # Modificado: URL simplificada
@token_required # Modificado: Rota protegida
def turmas_aluno(current_user): # Modificado: Recebe 'current_user'
    
    if current_user["id_nivel"] != 3:
        return jsonify({"erro": "Acesso não autorizado. Rota para alunos."}), 403

    id_user = current_user["id_user"] # Modificado: ID vem do token

    try:
        conn = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                t.id_turma,
                c.nome_curso,
                d.nome_disciplina,
                u.nome AS professor,
                ta.nota_final,
                ta.frequencia
            FROM turma_alunos ta
            JOIN turmas t ON ta.id_turma = t.id_turma
            JOIN disciplinas d ON t.id_disciplina = d.id_disciplina
            JOIN cursos c ON d.id_curso = c.id_curso
            JOIN usuario u ON t.id_professor = u.id_user
            WHERE ta.id_aluno = %s
        """, (id_user,)) # Modificado: usa id_user do token
        turmas = cursor.fetchall()
        return jsonify(turmas), 200
    except Exception as err:
        print("Erro MySQL:", err)
        return jsonify({"erro": "Erro ao buscar turmas"}), 500
    finally:
        if conn:
            conn.close()


# ======================================================
# ⚙️ ROTAS ADMINISTRATIVAS (Modificado com JWT)
# ======================================================
# (Assumindo que admin é id_nivel = 1)

@app.route("/api/admin/curso", methods=["POST"])
@token_required
def admin_add_curso(current_user):
    if current_user["id_nivel"] != 1:
        return jsonify({"erro": "Acesso não autorizado."}), 403
        
    data = request.get_json()
    nome_curso = data.get("nome_curso")
    if not nome_curso:
        return jsonify({"erro": "Nome do curso obrigatório"}), 400

    try:
        conn = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cursos (nome_curso) VALUES (%s)", (nome_curso,))
        conn.commit()
        return jsonify({"mensagem": "Curso adicionado com sucesso!"}), 201
    except pymysql.err.IntegrityError:
        return jsonify({"erro": "Curso já cadastrado"}), 400
    except Exception as err:
        print("Erro MySQL:", err)
        return jsonify({"erro": "Erro ao adicionar curso"}), 500
    finally:
        if conn:
            conn.close()


@app.route("/api/admin/disciplina", methods=["POST"])
@token_required
def admin_add_disciplina(current_user):
    if current_user["id_nivel"] != 1:
        return jsonify({"erro": "Acesso não autorizado."}), 403
        
    data = request.get_json()
    nome_disciplina = data.get("nome_disciplina")
    id_curso = data.get("id_curso")

    if not nome_disciplina or not id_curso:
        return jsonify({"erro": "Campos obrigatórios"}), 400

    try:
        conn = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO disciplinas (nome_disciplina, id_curso) VALUES (%s, %s)
        """, (nome_disciplina, id_curso))
        conn.commit()
        return jsonify({"mensagem": "Disciplina cadastrada com sucesso!"}), 201
    except Exception as err:
        print("Erro MySQL:", err)
        return jsonify({"erro": "Erro ao cadastrar disciplina"}), 500
    finally:
        if conn:
            conn.close()


@app.route("/api/disciplinas", methods=["GET"])
@token_required
def listar_disciplinas(current_user):
    if current_user["id_nivel"] != 1: # Protegido
        return jsonify({"erro": "Acesso não autorizado."}), 403
        
    try:
        conn = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT d.id_disciplina, d.nome_disciplina, c.nome_curso
            FROM disciplinas d
            JOIN cursos c ON d.id_curso = c.id_curso
        """)
        disciplinas = cursor.fetchall()
        return jsonify(disciplinas), 200
    except Exception as err:
        print("Erro MySQL:", err)
        return jsonify({"erro": "Erro ao listar disciplinas"}), 500
    finally:
        if conn:
            conn.close()


@app.route("/api/admin/turma", methods=["POST"])
@token_required
def admin_criar_turma(current_user):
    if current_user["id_nivel"] != 1:
        return jsonify({"erro": "Acesso não autorizado."}), 403

    data = request.get_json()
    id_curso = data.get("id_curso")
    id_disciplina = data.get("id_disciplina")
    id_professor = data.get("id_professor")
    ano_semestre = data.get("ano_semestre")

    if not all([id_curso, id_disciplina, id_professor, ano_semestre]):
        return jsonify({"erro": "Campos obrigatórios"}), 400

    try:
        conn = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO turmas (id_disciplina, id_professor, ano_semestre)
            VALUES (%s, %s, %s)
        """, (id_disciplina, id_professor, ano_semestre))
        conn.commit()
        return jsonify({"mensagem": "Turma criada com sucesso!"}), 201
    except Exception as err:
        print("Erro MySQL:", err)
        return jsonify({"erro": "Erro ao criar turma"}), 500
    finally:
        if conn:
            conn.close()


@app.route("/api/turmas", methods=["GET"])
@token_required
def listar_turmas(current_user):
    if current_user["id_nivel"] != 1:
        return jsonify({"erro": "Acesso não autorizado."}), 403
        
    try:
        conn = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                t.id_turma,
                c.nome_curso,
                d.nome_disciplina,
                u.nome AS nome_professor,
                t.ano_semestre
            FROM turmas t
            JOIN disciplinas d ON t.id_disciplina = d.id_disciplina
            JOIN cursos c ON d.id_curso = c.id_curso
            JOIN usuario u ON t.id_professor = u.id_user
        """)
        turmas = cursor.fetchall()
        return jsonify(turmas), 200
    except Exception as err:
        print("Erro MySQL:", err)
        return jsonify({"erro": "Erro ao listar turmas"}), 500
    finally:
        if conn:
            conn.close()


@app.route("/api/admin/usuarios", methods=["GET"])
@token_required
def listar_usuarios(current_user):
    if current_user["id_nivel"] != 1:
        return jsonify({"erro": "Acesso não autorizado."}), 403

    try:
        conn = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()
        cursor.execute("SELECT id_user, nome, email, id_nivel FROM usuario")
        usuarios = cursor.fetchall()
        return jsonify(usuarios), 200
    except Exception as err:
        print("Erro MySQL:", err)
        return jsonify({"erro": "Erro ao listar usuários"}), 500
    finally:
        if conn:
            conn.close()


@app.route("/api/admin/professores", methods=["GET"])
@token_required
def listar_professores(current_user):
    if current_user["id_nivel"] != 1:
        return jsonify({"erro": "Acesso não autorizado."}), 403
        
    try:
        conn = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()
        cursor.execute("SELECT id_user, nome FROM usuario WHERE id_nivel = 2")
        professores = cursor.fetchall()
        return jsonify(professores), 200
    except Exception as err:
        print("Erro MySQL:", err)
        return jsonify({"erro": "Erro ao listar professores"}), 500
    finally:
        if conn:
            conn.close()

# ======================================================
# ROTA DE VALIDAÇÃO (Removida)
# ======================================================
# A antiga rota /api/auth/validate foi removida.
# O decorator @token_required agora faz a validação em
# CADA rota protegida, o que é muito mais seguro.


# ======================================================
# 🚀 RODAR SERVIDOR
# ======================================================
if __name__ == "__main__":
    app.run(debug=True)