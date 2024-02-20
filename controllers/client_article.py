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

    tuple_sql = []
    condition_and = ""
    if "filter_word" in session or "filter_prix_min" in session or "filter_prix_max" in session or "filter_types" in session:
        sql = sql + " WHERE "

    if "filter_word" in session:
        sql = sql + "nom_parfum LIKE %s"
        recherche = "%" + session["filter_word"] + "%"
        tuple_sql.append(recherche)
        condition_and = " AND "
    if "filter_prix_min" in session or "filter_prix_max" in session:
        sql = sql + condition_and + " prix BETWEEN %s AND %s"
        tuple_sql.append(session["filter_prix_min"])
        tuple_sql.append(session["filter_prix_max"])
        condition_and = " AND "
    if "filter_types" in session:

        sql = sql + condition_and + "("
        last_item = session['filter_types'][-1]
        for item in session['filter_types']:
            sql = sql + " id_genre = %s "
            if item != last_item:
                sql = sql + " OR "
            tuple_sql.append(item)

        sql = sql + ")"
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
