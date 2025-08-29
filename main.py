from flask import Flask, render_template, url_for, request, flash, redirect
from forms import FormLogin, FormCriarConta

app = Flask(__name__)

app.config['SECRET_KEY'] = 'cafe21d28999850c8855b75bb3192523'


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
def usuarios():
    return render_template('usuarios.html', lista_users=lista_users)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        flash('Login feito com sucesso. Email: {}'.format(form_login.email.data), 'alert-success')
        return redirect(url_for('home'))
    
    if form_criarconta.validate_on_submit() and 'botao_submit_criar_conta' in request.form:
        flash('Conta criada com sucesso. Email: {}'.format(form_criarconta.email.data), 'alert-success')
        return redirect(url_for('home'))

    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)


if __name__ == '__main__':
    app.run(debug=True)