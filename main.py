from flask import Flask, render_template

app = Flask(__name__)

lista_users = [
    'Felipe',
    'João',
    'Fernanda'
]


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/contato')
def contato():
    return render_template('contato.html')


@app.route('/usuarios')
def usuarios():
    return render_template('usuarios.html', lista_users=lista_users)



if __name__ == '__main__':
    app.run(debug=True)