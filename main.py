from flask import Flask, render_template, url_for
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


@app.route('/login')
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()
    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)


if __name__ == '__main__':
    app.run(debug=True)