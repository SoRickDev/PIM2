import os
import pymysql
import bcrypt
import random
import jwt
import subprocess
from datetime import date, datetime, timedelta, timezone
from functools import wraps
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ======================================================
# ⚠️ CONFIGURAÇÃO
# ======================================================
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "CHAVE_MUITO_SECRETA_PIM_2025")

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "280802", # Sua senha
    "database": "CADASTRO"
}

# ======================================================
# 🧠 ALGORITMOS (Python)
# ======================================================
def bubble_sort_alunos(lista_alunos):
    """Ordenação manual de alunos por nota (Requisito PIM)"""
    n = len(lista_alunos)
    for i in range(n):
        for j in range(0, n - i - 1):
            nota_a = float(lista_alunos[j].get('nota_final') or 0)
            nota_b = float(lista_alunos[j + 1].get('nota_final') or 0)
            if nota_a < nota_b:
                lista_alunos[j], lista_alunos[j + 1] = lista_alunos[j + 1], lista_alunos[j]
    return lista_alunos

# ======================================================
# 🔌 INTEGRAÇÃO COM C (SIMULADA / BYPASS)
# ======================================================
def calcular_media_via_c(nota, atividade):
    """Calcula média (Simulação para evitar erro de falta de executável)"""
    print(f"Calculando média: Nota={nota}, Ativ={atividade}")
    try:
        n_prova = float(str(nota).replace(',', '.'))
        n_trab = float(str(atividade).replace(',', '.'))
        media = (n_prova * 0.7) + (n_trab * 0.3)
        return round(media, 2)
    except Exception as e:
        print(f"Erro cálculo: {e}")
        return -1

# ======================================================
# 🛡️ AUTH DECORATOR
# ======================================================
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            try:
                token = request.headers["Authorization"].split(" ")[1]
            except IndexError:
                return jsonify({"erro": "Token inválido"}), 401
        if not token:
            return jsonify({"erro": "Token obrigatório"}), 401
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            conn = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)
            with conn.cursor() as cursor:
                cursor.execute("SELECT id_user, nome, id_nivel FROM usuario WHERE id_user = %s", (data["id_user"],))
                current_user = cursor.fetchone()
            conn.close()
            if not current_user:
                 return jsonify({"erro": "Usuário inválido"}), 401
            kwargs["current_user"] = current_user
        except Exception:
            return jsonify({"erro": "Token expirado"}), 401
        return f(*args, **kwargs)
    return decorated

# ======================================================
# 🚀 ROTAS
# ======================================================

# --- LOGIN ---
@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    senha = data.get("senha")
    
    if not email or not senha: return jsonify({"erro": "Dados incompletos"}), 400

    conn = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM usuario WHERE email = %s", (email,))
            usuario = cursor.fetchone()

            if usuario and bcrypt.checkpw(senha.encode("utf-8"), usuario["senha_hash"].encode("utf-8")):
                token = jwt.encode({
                    "id_user": usuario["id_user"],
                    "nome": usuario["nome"],
                    "id_nivel": usuario["id_nivel"],
                    "exp": datetime.now(timezone.utc) + timedelta(hours=24)
                }, app.config["SECRET_KEY"], algorithm="HS256")
                
                # Retorna o nível para o frontend saber redirecionar
                return jsonify({"token": token, "nivel": usuario["id_nivel"]}), 200
            return jsonify({"erro": "Email ou senha incorretos"}), 401
    finally:
        conn.close()

# ... (Mantenha os imports e configs anteriores iguais)

# ======================================================
# 👑 MÓDULO ADMIN (CRUD COMPLETO)
# ======================================================

@app.route("/api/admin/dashboard", methods=["GET"])
@token_required
def admin_dashboard(current_user):
    if current_user["id_nivel"] != 1: 
        return jsonify({"erro": "Acesso negado."}), 403
    
    conn = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)
    try:
        with conn.cursor() as cursor:
            # Stats
            cursor.execute("SELECT COUNT(*) as total FROM usuario WHERE id_nivel = 3")
            alunos = cursor.fetchone()['total']
            cursor.execute("SELECT COUNT(*) as total FROM turmas")
            turmas = cursor.fetchone()['total']
            cursor.execute("SELECT COUNT(*) as total FROM usuario WHERE id_nivel = 2")
            professores = cursor.fetchone()['total']
            
            # Lista COMPLETA de Alunos
            cursor.execute("""
                SELECT u.id_user, u.nome, u.email, u.telefone, c.nome_curso, da.matricula
                FROM usuario u
                JOIN dados_aluno da ON u.id_user = da.id_user
                JOIN cursos c ON da.id_curso = c.id_curso
                ORDER BY u.nome ASC
            """)
            lista_alunos = cursor.fetchall()

            # Lista COMPLETA de Professores
            cursor.execute("""
                SELECT id_user, nome, email, telefone, cpf
                FROM usuario
                WHERE id_nivel = 2
                ORDER BY nome ASC
            """)
            lista_profs = cursor.fetchall()
            
        return jsonify({
            "stats": {"alunos": alunos, "turmas": turmas, "professores": professores}, 
            "alunos": lista_alunos,
            "professores": lista_profs
        }), 200
    finally:
        conn.close()

# --- ROTA DE EDIÇÃO (UPDATE) ---
@app.route("/api/admin/usuario/<int:id_user>", methods=["PUT"])
@token_required
def update_usuario(current_user, id_user):
    if current_user["id_nivel"] != 1: return jsonify({"erro": "Acesso negado"}), 403
    
    data = request.get_json()
    conn = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)
    try:
        with conn.cursor() as cursor:
            # Atualiza dados básicos na tabela usuario
            cursor.execute("""
                UPDATE usuario 
                SET nome = %s, email = %s, telefone = %s
                WHERE id_user = %s
            """, (data['nome'], data['email'], data['telefone'], id_user))
            conn.commit()
        return jsonify({"mensagem": "Usuário atualizado com sucesso!"}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        conn.close()

# --- ROTA DE EXCLUSÃO (DELETE) ---
@app.route("/api/admin/usuario/<int:id_user>", methods=["DELETE"])
@token_required
def delete_usuario(current_user, id_user):
    if current_user["id_nivel"] != 1: return jsonify({"erro": "Acesso negado"}), 403
    
    # Impede que o admin se delete
    if id_user == current_user['id_user']:
        return jsonify({"erro": "Você não pode excluir a si mesmo."}), 400

    conn = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)
    try:
        with conn.cursor() as cursor:
            # Graças ao ON DELETE CASCADE no banco, basta apagar da tabela pai
            cursor.execute("DELETE FROM usuario WHERE id_user = %s", (id_user,))
            conn.commit()
        return jsonify({"mensagem": "Usuário excluído com sucesso!"}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        conn.close()

# --- ROTAS DE CADASTRO E CURSOS ---
@app.route("/api/cursos", methods=["GET"])
def listar_cursos():
    conn = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_curso, nome_curso FROM cursos")
            return jsonify(cursor.fetchall()), 200
    finally: conn.close()

@app.route("/api/auth/register", methods=["POST"])
def register():
    d = request.get_json()
    conn = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)
    try:
        senha_hash = bcrypt.hashpw(d["senha"].encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO usuario (cpf, nome, sexo, datanasc, telefone, email, senha_hash, id_nivel) VALUES (%s,%s,'Outro',%s,%s,%s,%s,%s)",
                           (d["cpf"], d["nome"], d["datanasc"], d["telefone"], d["email"], senha_hash, int(d["id_nivel"])))
            id_user = cursor.lastrowid
            conn.commit()
            if int(d["id_nivel"]) == 3 and d.get("id_curso"):
                 mat = f"A{random.randint(10000,99999)}"
                 cursor.execute("INSERT INTO dados_aluno (id_user, id_curso, matricula, status_aluno, data_ingresso) VALUES (%s,%s,%s,'Ativo',%s)", (id_user, d["id_curso"], mat, date.today()))
                 conn.commit()
                 cursor.execute("SELECT t.id_turma FROM turmas t JOIN disciplinas d ON t.id_disciplina=d.id_disciplina WHERE d.id_curso=%s LIMIT 2", (d["id_curso"],))
                 for t in cursor.fetchall():
                     cursor.execute("INSERT INTO turma_alunos (id_turma, id_aluno) VALUES (%s, %s)", (t["id_turma"], id_user))
                 conn.commit()
        return jsonify({"msg": "Cadastro OK"}), 201
    except Exception as e: return jsonify({"erro": str(e)}), 400
    finally: conn.close()

# --- ROTAS DO PROFESSOR ---
@app.route("/api/professor/turmas", methods=["GET"])
@token_required
def professor_turmas(current_user):
    if current_user["id_nivel"] != 2: return jsonify({"erro": "Proibido"}), 403
    conn = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT t.id_turma, d.nome_disciplina, c.nome_curso, t.ano_semestre
                FROM turmas t
                JOIN disciplinas d ON t.id_disciplina = d.id_disciplina
                JOIN cursos c ON d.id_curso = c.id_curso
                WHERE t.id_professor = %s
            """, (current_user["id_user"],))
            return jsonify(cursor.fetchall()), 200
    finally: conn.close()

@app.route("/api/professor/turmas/<int:id_turma>/alunos", methods=["GET"])
@token_required
def alunos_da_turma(current_user, id_turma):
    if current_user["id_nivel"] != 2: return jsonify({"erro": "Proibido"}), 403
    conn = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT u.id_user, u.nome, da.matricula, ta.nota_final, ta.frequencia
                FROM turma_alunos ta
                JOIN usuario u ON ta.id_aluno = u.id_user
                JOIN dados_aluno da ON u.id_user = da.id_user
                WHERE ta.id_turma = %s
            """, (id_turma,))
            alunos = cursor.fetchall()
        return jsonify(bubble_sort_alunos(alunos)), 200
    finally: conn.close()

@app.route("/api/professor/calcular_nota", methods=["POST"])
@token_required
def calcular_e_salvar(current_user):
    if current_user["id_nivel"] != 2: return jsonify({"erro": "Proibido"}), 403
    data = request.get_json()
    media = calcular_media_via_c(data.get("nota_prova"), data.get("nota_trabalho"))
    conn = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)
    try:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE turma_alunos SET nota_final = %s, frequencia = %s WHERE id_turma = %s AND id_aluno = %s", 
                           (media, data.get("frequencia"), data.get("id_turma"), data.get("id_aluno")))
            conn.commit()
        return jsonify({"mensagem": "Salvo", "media": media}), 200
    except Exception as e: return jsonify({"erro": str(e)}), 500
    finally: conn.close()

# --- ROTAS DO ALUNO ---
@app.route("/api/aluno/dados", methods=["GET"])
@token_required
def aluno_dados(current_user):
    if current_user["id_nivel"] != 3: return jsonify({"erro": "Proibido"}), 403
    conn = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT da.matricula, da.status_aluno, c.nome_curso
                FROM dados_aluno da JOIN cursos c ON da.id_curso = c.id_curso
                WHERE da.id_user = %s
            """, (current_user["id_user"],))
            return jsonify(cursor.fetchone()), 200
    finally: conn.close()

@app.route("/api/aluno/turmas", methods=["GET"])
@token_required
def aluno_turmas(current_user):
    if current_user["id_nivel"] != 3: return jsonify({"erro": "Proibido"}), 403
    conn = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT t.id_turma, c.nome_curso, d.nome_disciplina, u.nome AS professor, ta.nota_final, ta.frequencia
                FROM turma_alunos ta
                JOIN turmas t ON ta.id_turma = t.id_turma
                JOIN disciplinas d ON t.id_disciplina = d.id_disciplina
                JOIN cursos c ON d.id_curso = c.id_curso
                JOIN usuario u ON t.id_professor = u.id_user
                WHERE ta.id_aluno = %s
            """, (current_user["id_user"],))
            return jsonify(cursor.fetchall()), 200
    finally: conn.close()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)