from flask import Flask, render_template, request, redirect, url_for, session, flash, Response
import os
import logging
from werkzeug.utils import secure_filename
import spacy
from typing import List, Optional
from manage import inserir, atualizar, deletar, tudo

app = Flask(__name__)
app.secret_key = 'e5y53heam7sdfh'  # Chave secreta para a sessão

# Configuração de upload de arquivos
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif'}

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Dados de autenticação simples
USERNAME = 'netolx0885@gmail.com'
PASSWORD = '123412'

# Carregar o modelo de língua do spaCy
nlp = spacy.load('pt_core_news_sm')

def allowed_file(filename: Optional[str]) -> bool:
    """Verifica se o arquivo tem uma extensão permitida."""
    return filename is not None and '.' in filename and filename.rsplit('.', 1)[-1].lower() in app.config['ALLOWED_EXTENSIONS']

def get_db_connection() -> List[dict]:
    """Retorna todos os produtos do banco de dados."""
    return tudo()

def lemmatize_query(query: str) -> str:
    """Retorna a consulta lematizada para busca eficiente."""
    doc = nlp(query)
    return ' '.join([token.lemma_ for token in doc if not token.is_stop and not token.is_punct])

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/sobre', endpoint='sobre')
def about():
    return render_template("sobre.html")

@app.route('/produtos')
def produtos():
    query = request.args.get('query', '').strip().lower()
    lemmatized_query = lemmatize_query(query)
    words = lemmatized_query.split()

    produtos = get_db_connection()

    try:
        if words:
            conditions = ' OR '.join(['LOWER(nome) LIKE ? OR LOWER(descricao) LIKE ?' for _ in words])
            parameters = ['%' + word + '%' for word in words for _ in (0, 1)]
            produtos = [p for p in produtos if any(word in p['nome'].lower() or word in p['descricao'].lower() for word in words)]
        else:
            produtos = produtos
    except Exception as e:
        logger.error(f"Erro ao consultar dados: {e}")
        produtos = []

    return render_template("produtos.html", produtos=produtos, query=query)

@app.route('/imagem/<int:id>')
def get_image(id: int):
    produtos = get_db_connection()
    produto = next((p for p in produtos if p['id'] == id), None)
    if produto and produto['imagem']:
        return Response(produto['imagem'], mimetype=f'image/{produto["imagem_ext"]}')
    return 'Imagem não encontrada', 404

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            password = request.form.get('password')

            if username == USERNAME and password == PASSWORD:
                session['logged_in'] = True
                return redirect(url_for('admin'))
            else:
                flash('Usuário ou senha inválidos', 'error')
        except Exception as e:
            logger.error(f"Erro ao processar login: {e}")
            flash('Erro ao processar login', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    produtos = get_db_connection()

    if request.method == 'POST':
        try:
            if 'add' in request.form:
                nome = request.form['nome']
                descricao = request.form['descricao']
                preco = request.form['preco']
                link = request.form['link']
                imagem = request.files.get('imagem')

                if imagem and allowed_file(imagem.filename):
                    imagem_filename = imagem.filename
                    imagem_ext = imagem_filename.rsplit('.', 1)[-1].lower() if imagem_filename else ''
                    imagem_blob = imagem.read() if imagem_filename else None
                    imagem_filename = secure_filename(imagem_filename) if imagem_filename else ''
                else:
                    imagem_ext = ''
                    imagem_blob = None
                    imagem_filename = ''

                inserir(None, nome, descricao, preco, link, imagem_blob, imagem_ext)
                flash('Produto adicionado com sucesso!', 'success')
                return redirect(url_for('admin'))

            if 'update' in request.form:
                id = int(request.form['id'])
                nome = request.form['nome']
                descricao = request.form['descricao']
                preco = request.form['preco']
                link = request.form['link']
                imagem = request.files.get('imagem')

                if imagem and allowed_file(imagem.filename):
                    imagem_filename = imagem.filename
                    imagem_ext = imagem_filename.rsplit('.', 1)[-1].lower() if imagem_filename else ''
                    imagem_blob = imagem.read() if imagem_filename else None
                    imagem_filename = secure_filename(imagem_filename) if imagem_filename else ''
                else:
                    imagem_ext = ''
                    imagem_blob = None
                    imagem_filename = ''

                atualizar(id, nome, descricao, preco, link, imagem_blob, imagem_ext)
                flash('Produto atualizado com sucesso!', 'success')
                return redirect(url_for('admin'))

            if 'delete' in request.form:
                id = int(request.form['id'])
                deletar(id)
                flash('Produto deletado com sucesso!', 'success')
                return redirect(url_for('admin'))

        except Exception as e:
            logger.error(f"Erro ao processar admin: {e}")
            flash('Erro ao processar a operação', 'error')

    return render_template('admin.html', produtos=produtos)

if __name__ == "__main__":
    app.run(port=8000)