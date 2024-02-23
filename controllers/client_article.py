# Importez ces fonctions pour utiliser la méthode generate_password_hash
from flask import Blueprint, render_template, session
from connexion_db import get_db

client_article = Blueprint('client_article', __name__, template_folder='templates')


@client_article.route('/client/index')
@client_article.route('/client/parfum/show')
def client_parfum_show():
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

    tuple_sql = []
    condition_and = ""

    tuple_sql = tuple(tuple_sql)
    print(sql, tuple_sql)
    mycursor.execute(sql, tuple_sql)
    articles = mycursor.fetchall()
    # utilisation du filtre
    sql3 = ''' prise en compte des commentaires et des notes dans le SQL    '''

    sql = '''SELECT DISTINCT nom_genre FROM genre;'''
    mycursor.execute(sql)
    genre = mycursor.fetchall()
    types_article = genre

    sql = '''
    SELECT ligne_panier.utilisateur_id, parfum.nom_parfum AS nom, ligne_panier.date_ajout, ligne_panier.quantite, parfum.prix_parfum AS prix, ligne_panier.parfum_id, parfum.stock
    FROM ligne_panier
    JOIN parfum ON ligne_panier.parfum_id = parfum.id_parfum
    WHERE ligne_panier.utilisateur_id = %s ;
    '''
    mycursor.execute(sql, (id_client))
    articles_panier = mycursor.fetchall()
    prix_total = 123  # requete à faire
    # articles_panier = []

    if len(articles_panier) >= 1:
        sql = ''' calcul du prix total du panier '''
        prix_total = None
    else:
        prix_total = None

    return render_template('client/boutique/panier_article.html',
                           parfums=parfums,
                           articles_panier=articles_panier,
                           # prix_total=prix_total,
                           items_filtre=types_article)