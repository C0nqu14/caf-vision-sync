import base64
import io
import matplotlib.pyplot as plt
from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import google.generativeai as genai
from datetime import datetime
from static.passwd import passwd


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'
app.secret_key = 'keyConquia'


db = SQLAlchemy(app)


genai.configure(api_key="AIzaSyC3FRVJRGrot2zsczCkp4M-rNBRv0LWLAQ")
modelo = genai.GenerativeModel("gemini-1.5-flash")


class Estudante(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	nome = db.Column(db.String(100), nullable=False)
	sobrenome = db.Column(db.String(100), nullable=False)
	email = db.Column(db.String(100), unique=True, nullable=False)
	data = db.Column(db.Date)
	genero = db.Column(db.Enum('Feminino' , "Masculino"))
	turma = db.Column(db.String(50))
	senha = db.Column(db.String(100), nullable=False)

class Feedback(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	conteudo = db.Column(db.String(500), nullable=False)
	sentimento = db.Column(db.String(10), nullable=False)
	user_id = db.Column(db.Integer, nullable=False)
	historico = db.Column(db.DateTime, default=db.func.now())
	tema = db.Column(db.String(50))

class ADMIN(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	nome = db.Column(db.String(50))
	username = db.Column(db.String(20))
	email = db.Column(db.String(100), nullable=False)
	senha = db.Column(db.String(100) , nullable=False)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():

	if request.method == 'POST':

		nome = request.form['firstname']
		sobrenome = request.form['lastname']
		email = request.form['email']
		data = request.form['date']
		data = datetime.strptime(data , "%Y-%m-%d").date()
		genero = request.form['gender']
		turma = request.form['clt']
		senha = request.form['password']
		senha_hashed = generate_password_hash(senha)

		new_estudante = Estudante(nome=nome, sobrenome=sobrenome, email=email, data=data , genero=genero, turma=turma, senha=senha_hashed)
		db.session.add(new_estudante)
		db.session.commit()

		session['email'] = email
		flash('Cadastro realizado com sucesso!', 'success')
		return redirect(url_for('login'))

	return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['password']

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

		conteudo = request.form['textarea']
		user_id = session.get('user_id')


		prompt = f"Analise o seguinte feedback: {conteudo} e classifique o sentimento como: Positivo, Negativo ou Neutro. Responda apenas com a classificação, sem explicações."
		resposta = modelo.generate_content(prompt)
		sentimento = resposta.text.strip().rstrip('.')
		prompt_tema = f"Com base no seguinte feedback: {conteudo}, sugira um tema relevante para um projeto escolar. Responda apenas com o tema, sem explicações."
		tema = modelo.generate_content(prompt_tema)
		resposta_tema = tema.text.strip().rstrip('.')

		new_feedback = Feedback(conteudo=conteudo, sentimento=sentimento, user_id=user_id, tema=resposta_tema)
		db.session.add(new_feedback)
		db.session.commit()

		flash('Feedback enviado com sucesso!')
		return redirect(url_for('feedback'))

	user_id = session.get('user_id')
	feedbacks_usuario = Feedback.query.filter_by(user_id=user_id).order_by(Feedback.historico.desc()).all()

	return render_template('feedback.html' , feedbacks=feedbacks_usuario)


@app.route('/analise_sentimentos', methods=['GET'])
def analise_sentimentos():

	if not session.get('admin_logged_in'):

		flash('Você precisa fazer login para acessar esta página.', 'warning')
		return redirect(url_for('login'))

	feedbacks = Feedback.query.all()

	sentimentos_count = {

        	'Positivo': 0,
        	'Negativo': 0,
        	'Neutro': 0
    	}

	for feedback in feedbacks:

		sentimento = feedback.sentimento.strip().rstrip('.')
		if sentimento in sentimentos_count:

			sentimentos_count[sentimento] += 1
		else:

			sentimentos_count['Neutro'] += 1 

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

	return render_template('analise_sentimentos.html', graph_url=graph_url, admin_username=session.get('admin_username'))

@app.route("/login_admin" ,  methods=["GET" , "POST"])
def login_admin():

	if request.method == 'POST':

		username = request.form['username']
		senha = request.form['password']

		admin = ADMIN.query.filter_by(username=username).first()
		if admin and check_password_hash(admin.senha, senha):

			session['admin_logged_in'] = True
			session['admin_username'] = username
			flash('Login bem-sucedido!')
			return redirect(url_for('analise_sentimentos'))

		else:

			flash('Email ou senha incorretos.')

	return render_template('login_admin.html')

@app.route('/logout_admin')
def logout_admin():

    session.clear()
    flash('Você saiu do sistema com sucesso.', 'info')
    return redirect(url_for('login'))


with app.app_context():

    db.create_all()

    if not ADMIN.query.filter_by(email="joaomanuelconquia@gmail.com").first():
        adm = ADMIN(nome="João Conquia", username="C0nqu14" , email="joaomanuelconquia@gmail.com", senha=passwd)
        db.session.add(adm)
        db.session.commit()


if __name__ == '__main__':
    app.run(debug=True, port=4444)
