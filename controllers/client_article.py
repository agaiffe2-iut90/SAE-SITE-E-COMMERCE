# Importez ces fonctions pour utiliser la méthode generate_password_hash
from flask import Blueprint, render_template, session
from connexion_db import get_db

client_article = Blueprint('client_article', __name__, template_folder='templates')


@client_article.route('/client/index')
@client_article.route('/client/article/show')
def client_article_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    # Sélection des Parfums
    sql = ''' SELECT parfum.id_parfum
                , parfum.nom_parfum
                , parfum.prix_parfum
                , parfum.stock
                , parfum.image
                FROM parfum;
    '''
    mycursor.execute(sql)
    parfums = mycursor.fetchall()
    print(parfums)

    # Pour le filtre
    sql_filtre = '''SELECT DISTINCT nom_genre FROM genre;'''
    mycursor.execute(sql_filtre)
    genre = mycursor.fetchall()
    print(genre)

    articles_panier = []

    if len(articles_panier) >= 1:
        # Calcul du prix total du panier
        sql_prix_total = ''' Calcul du prix total du panier '''
        mycursor.execute(sql_prix_total)
        prix_total = mycursor.fetchone()['prix_total']
    else:
        prix_total = None

    return render_template('client/boutique/panier_article.html',
                           parfums=parfums,
                           articles_panier=articles_panier,
                           prix_total=prix_total,
                           items_filtre=genre)
