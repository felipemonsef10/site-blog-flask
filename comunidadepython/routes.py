from flask import render_template, redirect, flash, url_for, request
from comunidadepython import app, db, bcrypt
from comunidadepython.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost
from comunidadepython.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required
from secrets import token_hex
import os
from PIL import Image


@app.route('/')
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)


@app.route('/contatos')
def contato():
    return render_template('contatos.html')


@app.route('/usuarios')
@login_required
def usuarios():
    usuarios = Usuario.query.all()
    return render_template('usuarios.html', usuarios=usuarios)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()

        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_login.data)
            flash('Login feito com sucesso. Email: {}'.format(form_login.email.data), 'alert-success')
            param_next = request.args.get('next')

            if param_next:
                return redirect(param_next)
            else:
                return redirect(url_for('home'))
        else:
            flash('Falha no Login. E-mail ou senha incorretos', 'alert-danger')

    if form_criarconta.validate_on_submit() and 'botao_submit_criar_conta' in request.form:
        senha_criptografada = bcrypt.generate_password_hash(form_criarconta.senha.data)

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
    if current_user.cursos == 'Não Informado':
        qtd_cursos = 0
    else:
        qtd_cursos = len(current_user.cursos.split(';'))

    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))

    return render_template('perfil.html', foto_perfil=foto_perfil, qtd_cursos=qtd_cursos)


@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form = FormCriarPost()

    if form.validate_on_submit():
        post = Post(
            titulo=form.titulo.data,
            corpo=form.corpo.data,
            autor=current_user
        )

        db.session.add(post)
        db.session.commit()

        flash('Post Criado com Sucesso!!', 'alert-success')
        return redirect(url_for('home'))

    return render_template('criarpost.html', form=form)


def salvar_imagem(imagem):
    codigo = token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_imagem_codificada = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static\\fotos_perfil', nome_imagem_codificada)

    tamanho_imagem = (200, 200)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho_imagem)

    imagem_reduzida.save(caminho_completo)

    return nome_imagem_codificada


def atualizar_cursos(form):
    cursos = []
    for campo in form:
        if campo.name.startswith('curso_'):
            if campo.data == True:
                cursos.append(campo.label.text)

    if len(cursos) == 0:
        return 'Não Informado'

    return (';').join(cursos)


def verificar_cursos(form, cursos_usuario):
    for campo in form:
        if campo.name.startswith('curso_'):
            if campo.label.text in cursos_usuario:
                campo.data = True


@app.route('/perfil/editar',  methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()

    if form.validate_on_submit():
        mudou = False
        
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
            mudou = True
        
        if current_user.email != form.email.data:
            current_user.email = form.email.data
            mudou = True

        if current_user.username != form.username.data:
            current_user.username = form.username.data
            mudou = True

        if current_user.cursos != atualizar_cursos(form):
            current_user.cursos = atualizar_cursos(form)
            mudou = True

        if mudou:
            db.session.commit()
            flash(f'Perfil atualizado com Sucesso', 'alert-success')

            
        return redirect(url_for('perfil'))

    elif request.method == "GET":
        form.email.data = current_user.email
        form.username.data = current_user.username
        verificar_cursos(form, current_user.cursos)

    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editar_perfil.html', foto_perfil=foto_perfil, form=form)