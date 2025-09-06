from comunidadepython import app, db
from comunidadepython.models import Usuario, Post


# with app.app_context():
#     db.create_all()


# with app.app_context():
#     usuario = Usuario(username='Felipe', email='FelipeMonsef@gmail.com', senha='asdf1234')
#     usuario2 = Usuario(username='Luana', email='Luana@gmail.com', senha='1234asd')

#     db.session.add(usuario)
#     db.session.add(usuario2)

#     db.session.commit()


# with app.app_context():
#     meus_users = Usuario.query.all()
#     print(meus_users)


# with app.app_context():
#     # user_teste = Usuario.query.filter_by(id=1).all()
#     user_teste = Usuario.query.filter_by(id=1).first()
#     print(user_teste.email)
#     print(user_teste.posts)


# with app.app_context():
#     meu_post = Post(id_usuario=1, titulo='Segundo post do Felipe', corpo='Esse é um post de teste')

#     db.session.add(meu_post)

#     db.session.commit()


# with app.app_context():
#     post_teste = Post.query.first()
#     print(post_teste.titulo)
#     print(post_teste.autor.email)


with app.app_context():
    db.drop_all()
    db.create_all()