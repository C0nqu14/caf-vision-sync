import base64
import io
import matplotlib.pyplot as plt
from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from textblob import TextBlob
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'
app.secret_key = 'keyConquia'

db = SQLAlchemy(app)

class Estudante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.String(500), nullable=False)
    sentimento = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

@app.route('/cadastro_estudante1', methods=['GET', 'POST'])
def cadastro_estudante1():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        senha_hashed = generate_password_hash(senha)

        new_estudante = Estudante(nome=nome, email=email, senha=senha_hashed)
        db.session.add(new_estudante)
        db.session.commit()

        session['email'] = email
        flash('Cadastro realizado com sucesso! Continue para completar o cadastro.', 'success')
        return redirect(url_for('cadastro_estudante2'))

    return render_template('cadastro_estudante1.html')


@app.route('/cadastro_estudante2', methods=['GET', 'POST'])
def cadastro_estudante2():
    if request.method == 'POST':

        classe_turma = request.form['classe_turma']
        sexo = request.form['sexo']
        flash('Cadastro completo! Faça login para continuar.', 'success')
        return redirect(url_for('login'))

    return render_template('cadastro_estudante2.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        estudante = Estudante.query.filter_by(email=email).first()
        if estudante and check_password_hash(estudante.senha, senha):
            session['user_id'] = estudante.id
            flash('Login bem-sucedido!')
            return redirect(url_for('feedback'))
        else:
            flash('Email ou senha incorretos.')

    return render_template('login.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if 'user_id' not in session:
        flash('Você precisa estar logado para acessar essa página.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        conteudo = request.form['conteudo']
        user_id = session.get('user_id')

        sentimento = TextBlob(conteudo).sentiment.polarity
        if sentimento > 0:
            sentimento_str = 'Positivo'
        elif sentimento < 0:
            sentimento_str = 'Negativo'
        else:
            sentimento_str = 'Neutro'

        new_feedback = Feedback(conteudo=conteudo, sentimento=sentimento_str, user_id=user_id)
        db.session.add(new_feedback)
        db.session.commit()

        flash('Feedback enviado com sucesso!')
        return redirect(url_for('feedback'))

    return render_template('feedback.html')

@app.route('/analise_sentimentos', methods=['GET'])
def analise_sentimentos():
    feedbacks = Feedback.query.all()

    sentimentos_count = {
        'Positivo': 0,
        'Negativo': 0,
        'Neutro': 0
    }

    for feedback in feedbacks:
        sentimentos_count[feedback.sentimento] += 1

    plt.figure(figsize=(8, 5))
    plt.bar(sentimentos_count.keys(), sentimentos_count.values(), color=['green', 'red', 'gray'])
    plt.title('Análise de Sentimentos dos Feedbacks')
    plt.xlabel('Sentimentos')
    plt.ylabel('Número de Feedbacks')
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    graph_url = base64.b64encode(buf.getvalue()).decode('utf-8')

    plt.close()

    return render_template('analise_sentimentos.html', graph_url=graph_url)


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True , port=4444)
