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
    parfums_panier = mycursor.fetchall()
    print(parfums_panier, "article panier")

    if len(parfums_panier) >= 1:
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
                           , articles_panier=parfums_panier
                           #prix_total= prix_total
                           , validation=1
                           #, id_adresse_fav=id_adresse_fav
                           )


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()
    id_client = session.get('id_user')
    adresse_livraison = request.form.get('id_adresse_livraison')
    adresse_identique = request.form.get('adresse_identique')
    adresse_facturation = request.form.get('id_adresse_facturation')

    if adresse_identique == 'on':  # Si la checkbox est cochée, le formulaire renvoie 'on'
        adresse_facturation = adresse_livraison
        flash(u'Adresse de facturation identique à l\'adresse de livraison', 'alert-info')

    mycursor.execute('''SELECT * FROM ligne_panier WHERE utilisateur_id = %s;''', (id_client,))
    items_ligne_panier = mycursor.fetchall()

    if not items_ligne_panier:
        flash(u'Pas de parfum dans le panier', 'alert-warning')
        return redirect(url_for('client_index'))

    # Insertion de la commande
    mycursor.execute(
        '''INSERT INTO commande (id_commande, date_achat, utilisateur_id, etat_id) VALUES (NULL, current_timestamp, %s, 1);''',
        ( id_client ))
    id_commande = mycursor.lastrowid  # Récupère l'ID de la commande insérée

    for item in items_ligne_panier:
        id_parfum = item['parfum_id']
        quantite = item['quantite']
        # Sélection du prix directement lors de l'insertion dans ligne_commande
        mycursor.execute('''SELECT type_parfum_id, prix_parfum AS prix FROM parfum WHERE id_parfum = %s;''', (id_parfum,))
        parfum_info = mycursor.fetchone()

        if parfum_info:
            mycursor.execute(
                '''INSERT INTO ligne_commande (commande_id, parfum_id, prix, quantite) VALUES (%s, %s, %s, %s);''',
                (id_commande, id_parfum, parfum_info['prix'],quantite))

    # Suppression des éléments du panier après avoir ajouté la commande
    mycursor.execute('''DELETE FROM ligne_panier WHERE utilisateur_id = %s;''', (id_client,))

    get_db().commit()
    flash(u'Commande ajoutée avec succès', 'alert-success')
    return redirect('/client/parfum/show')




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

