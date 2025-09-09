from flask import render_template, redirect, flash, url_for, request
from comunidadepython import app, db, bcrypt
from comunidadepython.forms import FormLogin, FormCriarConta
from comunidadepython.models import Usuario
from flask_login import login_user, logout_user, current_user, login_required


lista_users = [
    'Felipe',
    'João',
    'Fernanda'
]


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/contatos')
def contato():
    return render_template('contatos.html')


@app.route('/usuarios')
@login_required
def usuarios():
    return render_template('usuarios.html', lista_users=lista_users)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_login.data)
            flash('Login feito com sucesso. Email: {}'.format(form_login.email.data), 'alert-success')
            return redirect(url_for('home'))
        else:
            flash('Falha no Login. E-mail ou senha incorretos', 'alert-danger')

    if form_criarconta.validate_on_submit() and 'botao_submit_criar_conta' in request.form:
        senha_criptografada = bcrypt.generate_password_hash(form_criarconta.senha.data)
        with app.app_context():
            # criar usuario
            usuario = Usuario(
                username=form_criarconta.username.data,
                email=form_criarconta.email.data,
                senha=senha_criptografada,
            )

            # adicionar a sessao
            db.session.add(usuario)
            
            # commit na sessao
            db.session.commit()
            
        flash('Conta criada com sucesso. Email: {}'.format(form_criarconta.email.data), 'alert-success')
        return redirect(url_for('home'))

    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso.', 'alert-success')
    return redirect(url_for('home'))


@app.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html')


@app.route('/post/criar')
@login_required
def criar_post():
    return render_template('criarpost.html')