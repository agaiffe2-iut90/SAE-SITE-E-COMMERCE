#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime
from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__,
                        template_folder='templates')


# validation de la commande : partie 2 -- vue pour choisir les adresses (livraision et facturation)
@client_commande.route('/client/commande/valide', methods=['POST'])
def client_commande_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = '''SELECT ligne_panier.quantite as quantite, parfum.prix_parfum as prix, genre.nom_genre as nom , volume.nom_volume as taille , parfum.stock as stock , parfum.id_parfum as id_parfum 
                    FROM ligne_panier
                    INNER JOIN parfum ON parfum.id_parfum = ligne_panier.parfum_id
                    INNER JOIN genre ON parfum.type_parfum_id = genre.id_genre
                    INNER JOIN volume ON parfum.volume_id = volume.id_volume
                    WHERE ligne_panier.utilisateur_id = %s;
                    '''
    mycursor.execute(sql, (id_client))
    articles_panier = mycursor.fetchall()
    print(articles_panier, "article panier")

    if len(articles_panier) >= 1:
        sql = ''' SELECT SUM(ligne_panier.quantite * parfum.prix_parfum) AS prix_total FROM ligne_panier 
                        INNER JOIN parfum ON parfum.id_parfum = ligne_panier.parfum_id
                        INNER JOIN genre ON parfum.type_parfum_id = genre.id_genre
                        '''
        mycursor.execute(sql)
        prix_total = mycursor.fetchone()['prix_total']

    else:
        prix_total = None
    # etape 2 : selection des adresses
    return render_template('client/boutique/panier_validation_adresses.html'
                           #, adresses=adresses
                           , articles_panier=articles_panier
                           , prix_total= prix_total
                           , validation=1
                           #, id_adresse_fav=id_adresse_fav
                           )


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()

    # choix de(s) (l')adresse(s)

    id_client = session['id_user']
    sql = ''' selection du contenu du panier de l'utilisateur '''
    items_ligne_panier = []
    # if items_ligne_panier is None or len(items_ligne_panier) < 1:
    #     flash(u'Pas d\'articles dans le ligne_panier', 'alert-warning')
    #     return redirect('/client/article/show')
                                           # https://pynative.com/python-mysql-transaction-management-using-commit-rollback/
    #a = datetime.strptime('my date', "%b %d %Y %H:%M")

    sql = ''' creation de la commande '''

    sql = '''SELECT last_insert_id() as last_insert_id'''
    # numéro de la dernière commande
    for item in items_ligne_panier:
        sql = ''' suppression d'une ligne de panier '''
        sql = "  ajout d'une ligne de commande'"

    get_db().commit()
    flash(u'Commande ajoutée','alert-success')
    return redirect('/client/article/show')




@client_commande.route('/client/commande/show', methods=['get','post'])
def client_commande_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = '''SELECT date_achat,COUNT(*) AS nbr_articles, SUM(ligne_commande.quantite * prix)  AS prix_total ,commande.etat_id AS etat_id, etat.libelle, commande.id_commande 
         FROM commande 
         INNER JOIN ligne_commande
         ON commande.id_commande=ligne_commande.commande_id 
         INNER JOIN etat 
         ON commande.etat_id=etat.id_etat
         WHERE utilisateur_id=%s 
         GROUP BY commande.id_commande 
         ORDER BY commande.etat_id ASC,date_achat DESC;'''
    mycursor.execute(sql, (id_client))
    commandes = mycursor.fetchall()

    articles_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande')
    print(id_commande, 2222222 ,"id commande lol")
    if id_commande != None:

        sql = '''SELECT nom_genre as nom, quantite, parfum.prix_parfum AS prix, sum(parfum.prix_parfum * ligne_commande.quantite) as prix_ligne
                from ligne_commande
                INNER JOIN commande on commande.id_commande = ligne_commande.commande_id
                INNER JOIN parfum on ligne_commande.parfum_id = parfum.id_parfum
                INNER JOIn genre on parfum.type_parfum_id = genre.id_genre
                WHERE commande.id_commande=%s
                GROUP BY parfum.id_parfum;
                '''
        mycursor.execute(sql, (id_commande))
        articles_commande = mycursor.fetchall()
        print(articles_commande)


    return render_template('client/commandes/show.html'
                           , commandes=commandes
                           , articles_commande=articles_commande
                           , commande_adresses=commande_adresses
                           )

