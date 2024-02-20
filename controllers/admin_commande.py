#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_commande = Blueprint('admin_commande', __name__,
                        template_folder='templates')

@admin_commande.route('/admin')
@admin_commande.route('/admin/commande/index')
def admin_index():
    return render_template('admin/layout_admin.html')


@admin_commande.route('/admin/commande/show', methods=['get', 'post'])
def admin_commande_show():
    mycursor = get_db().cursor()
    admin_id = session['id_user']
    # Mettez à jour la requête SQL selon votre nouvelle structure
    sql = '''
        SELECT c.date_achat, COUNT(*) AS nbr_articles, SUM(lc.quantite * lc.prix) AS prix_total, 
        c.etat_id, e.libelle AS libelle, c.id_commande, u.login AS login
        FROM commande c
        INNER JOIN ligne_commande lc ON c.id_commande = lc.commande_id
        INNER JOIN etat e ON c.etat_id = e.id_etat
        INNER JOIN utilisateur u ON c.utilisateur_id = u.id_utilisateur
        GROUP BY c.id_commande
        ORDER BY c.etat_id ASC, c.date_achat DESC;
        '''

    mycursor.execute(sql)
    commandes = mycursor.fetchall()
    print("commandes", commandes)

    articles_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    print(id_commande)
    if id_commande is not None:
        sql = '''
        SELECT p.nom_parfum AS nom, lc.quantite, lc.prix, SUM(lc.prix * lc.quantite) AS prix_ligne
        FROM ligne_commande lc
        INNER JOIN parfum p ON lc.parfum_id = p.id_parfum
        WHERE lc.commande_id = %s
        GROUP BY p.id_parfum;
        '''
        mycursor.execute(sql, (id_commande,))
        articles_commande = mycursor.fetchall()
    return render_template('admin/commandes/show.html'
                           , commandes=commandes
                           , articles_commande=articles_commande
                           , commande_adresses=commande_adresses
                           )


@admin_commande.route('/admin/commande/valider', methods=['get','post'])
def admin_commande_valider():
    mycursor = get_db().cursor()
    commande_id = request.form.get('id_commande', None)
    if commande_id != None:
        sql = '''UPDATE commande SET etat_id=2 WHERE id_commande=%s;'''
        mycursor.execute(sql, commande_id)
        get_db().commit()
    return redirect('/admin/commande/show')
