 #! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

client_coordonnee = Blueprint('client_coordonnee', __name__,
                        template_folder='templates')


@client_coordonnee.route('/client/coordonnee/show')
def client_coordonnee_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_adresse_fav = 0

    # Récupération des informations de l'utilisateur
    sql = "SELECT * FROM utilisateur WHERE id_utilisateur = %s;"
    mycursor.execute(sql, (id_client,))
    utilisateur = mycursor.fetchone()

    sql = '''
        SELECT 
            adresse.id_adresse, nom, rue, code_postal, ville, 
            COUNT(commande.id_commande) as nb_utilisation, adresse.valide
        FROM adresse
        LEFT JOIN commande ON commande.id_adresse = adresse.id_adresse
        WHERE adresse.utilisateur_id  = %s
        GROUP BY nom, rue, code_postal, ville, adresse.id_adresse, adresse.valide
        ORDER BY date_utilisation DESC; '''
    
    mycursor.execute(sql, (id_client,))
    adresses = mycursor.fetchall()
    nb_adresses = 0
    for ligne in adresses:
        if ligne['valide'] == 0:
            continue
        else:
            nb_adresses += 1

    if nb_adresses > 1:
        
        sql = '''
            SELECT id_adresse
            FROM adresse
            ORDER BY date_utilisation DESC
            LIMIT 1; '''

        mycursor.execute(sql)
        address_fav = mycursor.fetchone()
        
        if address_fav != None:
            id_adresse_fav = mycursor.fetchone()['id_adresse']

    return render_template('client/coordonnee/show_coordonnee.html'
                           , utilisateur=utilisateur
                          , adresses=adresses
                         ,nb_adresses=nb_adresses, id_adresse_fav = id_adresse_fav
                           )


@client_coordonnee.route('/client/coordonnee/edit', methods=['GET'])
def client_coordonnee_edit():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql = "SELECT * FROM utilisateur WHERE id_utilisateur = %s;"
    mycursor.execute(sql, (id_client,))
    utilisateur = mycursor.fetchone()

    return render_template('client/coordonnee/edit_coordonnee.html'
                           ,utilisateur=utilisateur
                           )

@client_coordonnee.route('/client/coordonnee/edit', methods=['POST'])
def client_coordonnee_edit_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    nom=request.form.get('nom')
    login = request.form.get('login')
    email = request.form.get('email')

    utilisateur = None
    if utilisateur:
        flash(u'votre cet Email ou ce Login existe déjà pour un autre utilisateur', 'alert-warning')
        return render_template('client/coordonnee/edit_coordonnee.html'
                               #, user=user
                               )


    get_db().commit()
    return redirect('/client/coordonnee/show')


@client_coordonnee.route('/client/coordonnee/delete_adresse',methods=['POST'])
def client_coordonnee_delete_adresse():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_adresse= request.form.get('id_adresse')
    sql = '''
        SELECT  
            COUNT(commande.id_commande) AS nb_utilisation, nom
        FROM adresse
        LEFT JOIN commande ON commande.id_adresse = adresse.id_adresse
        WHERE adresse.utilisateur_id  = %s
        GROUP BY nom; '''
    mycursor.execute(sql, (id_client))
    adresse = mycursor.fetchone()
    print(adresse)

    nb_utilisation = adresse['nb_utilisation']
    print(nb_utilisation)

    if adresse:
        if nb_utilisation > 0:
            sql = ''' UPDATE adresse SET valide = FALSE WHERE id_adresse = %s; '''
            mycursor.execute(sql, (id_adresse,))

            message = '''cette adresse est utilisée dans au moins une commande : 
                            vous ne pouvez pas la supprimer ; cependant cette adresse ne sera plus utilisable '''
            flash(message, 'alert-warning')
        else:
            sql = ''' DELETE FROM adresse WHERE id_adresse = %s AND utilisateur_id = %s; '''
            mycursor.execute(sql, (id_adresse, id_client))

        get_db().commit()
        message = f"Adresse supprimée : {id_adresse}"
        flash(message, 'alert-success')
    return redirect('/client/coordonnee/show')

@client_coordonnee.route('/client/coordonnee/add_adresse')
def client_coordonnee_add_adresse():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql = "SELECT * FROM utilisateur WHERE id_utilisateur = %s;"
    mycursor.execute(sql, (id_client,))
    utilisateur = mycursor.fetchone()

    return render_template('client/coordonnee/add_adresse.html', utilisateur=utilisateur)

@client_coordonnee.route('/client/coordonnee/add_adresse',methods=['POST'])
def client_coordonnee_add_adresse_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    nom= request.form.get('nom')
    rue = request.form.get('rue')
    code_postal = request.form.get('code_postal')
    ville = request.form.get('ville')
    tuple_insertion = (nom, rue, code_postal, ville, id_client)
    sql = ''' 
        INSERT INTO adresse (nom, rue, code_postal, ville, id_utilisateur )
        VALUES (%s, %s, %s, %s, %s); '''
    mycursor.execute(sql, tuple_insertion)
    get_db().commit()

    message = f"Adresse ajoutée avec succès Nom : {nom} Rue : {rue} Code postal : {code_postal} Ville : {ville}"
    flash(message, 'alert-success')
    return redirect('/client/coordonnee/show')

@client_coordonnee.route('/client/coordonnee/edit_adresse')
def client_coordonnee_edit_adresse():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_adresse = request.args.get('id_adresse')
    sql = "SELECT * FROM utilisateur WHERE id_utilisateur = %s;"
    
    mycursor.execute(sql, (id_client,))
    utilisateur = mycursor.fetchone()
    sql = '''
            SELECT * FROM adresse 
            WHERE id_adresse = %s AND id_utilisateur = %s; '''
    
    mycursor.execute(sql, (id_adresse, id_client))
    adresse = mycursor.fetchone()
    return render_template('/client/coordonnee/edit_adresse.html'
                            ,utilisateur=utilisateur
                            ,adresse=adresse
                           )

@client_coordonnee.route('/client/coordonnee/edit_adresse',methods=['POST'])
def client_coordonnee_edit_adresse_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    nom= request.form.get('nom')
    rue = request.form.get('rue')
    code_postal = request.form.get('code_postal')
    ville = request.form.get('ville')
    id_adresse = request.form.get('id_adresse')
    sql_update=(nom, rue, code_postal, ville, id_adresse, id_client)
    sql = ''' 
        UPDATE adresse SET nom=%s, rue=%s, code_postal=%s, ville=%s
        WHERE id_adresse = %s AND id_utilisateur = %s; '''
    
    mycursor.execute(sql, sql_update)
    get_db().commit()

    message = f"Adresse mise à jour avec succès Nom : {nom} Rue : {rue} Code postal : {code_postal} Ville : {ville}"
    flash(message, 'alert-success')
    return redirect('/client/coordonnee/show')
