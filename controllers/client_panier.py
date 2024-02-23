#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                        template_folder='templates')


@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_parfum = request.form.get('id_parfum')
    print(id_parfum, "artocle od ,flez")
    quantite = request.form.get('quantite')

    sql = '''SELECT * FROM ligne_panier WHERE parfum_id=%s AND utilisateur_id=%s'''
    mycursor.execute(sql, (id_parfum, id_client))
    article_panier = mycursor.fetchone()
    print(article_panier, "article_panier")

    mycursor.execute("SELECT * FROM parfum WHERE id_parfum=%s", (id_parfum,))
    article = mycursor.fetchone()
    print("article", article)

    if article_panier is not None and article_panier['quantite'] >= 1:
        tuple_update = (quantite, id_client, id_parfum)
        print(tuple_update, "tuple_update")
        sql = '''UPDATE ligne_panier SET quantite = quantite + %s WHERE utilisateur_id = %s AND parfum_id = %s'''
        mycursor.execute(sql, tuple_update)
        tuple = (quantite, id_parfum)
        sql2 = '''UPDATE parfum SET stock = stock - %s WHERE id_parfum =%s '''
        mycursor.execute(sql2, tuple)
        
    else:
        tuple_insert = (id_client, id_parfum, quantite)
        print(tuple_insert, "tuple_insert")
        sql = '''INSERT INTO ligne_panier(utilisateur_id, parfum_id, quantite, date_ajout) VALUES (%s, %s, %s, current_timestamp)'''
        mycursor.execute(sql, tuple_insert)
        tuple2 = (quantite, id_parfum)
        sql_2 = '''UPDATE parfum SET stock = stock - %s WHERE id_parfum =%s '''
        mycursor.execute(sql_2, tuple2)

    get_db().commit()
    return redirect('/client/parfum/show')

@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_parfum = request.form.get('id_parfum', '')
    quantite = request.form.get('quantite', 1)
    sql = '''SELECT * FROM parfum WHERE id_parfum = %s'''
    mycursor.execute(sql, (id_parfum))
    parfum = mycursor.fetchone()
    if parfum != None:
        sql = '''SELECT * FROM ligne_panier WHERE utilisateur_id = %s AND parfum_id = %s'''
        mycursor.execute(sql, (id_client, parfum['id_parfum']))
        article_panier = mycursor.fetchone()
        if article_panier != None:
            if article_panier['quantite'] > 1:
                sql = '''UPDATE ligne_panier SET quantite = quantite - %s WHERE utilisateur_id = %s AND parfum_id = %s'''
                mycursor.execute(sql, (quantite, id_client, parfum['id_parfum']))
                sql = '''UPDATE parfum SET stock = stock + %s WHERE id_parfum = %s'''
                mycursor.execute(sql, (quantite, parfum['id_parfum']))
            else:
                sql = '''DELETE FROM ligne_panier WHERE utilisateur_id = %s AND parfum_id = %s'''
                mycursor.execute(sql, (id_client, parfum['id_parfum']))
                sql = '''UPDATE parfum SET stock = stock + %s WHERE id_parfum = %s'''
                mycursor.execute(sql, (quantite, parfum['id_parfum']))
            get_db().commit()
    return redirect('/client/parfum/show')





@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    client_id = session['id_user']
    sql = '''SELECT * FROM ligne_panier WHERE utilisateur_id = %s'''
    mycursor.execute(sql, (client_id))
    items_panier = mycursor.fetchall()
    print(items_panier, 51411165461616)
    for item in items_panier:
        sql = '''UPDATE parfum SET stock = stock + %s WHERE id_parfum = %s'''
        mycursor.execute(sql, (item['quantite'], item['parfum_id']))
        sql2 = '''DELETE FROM ligne_panier WHERE utilisateur_id = %s AND parfum_id = %s'''
        mycursor.execute(sql2, (client_id, item['parfum_id']))
        get_db().commit()
    return redirect('/client/parfum/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_parfum = request.form.get('id_parfum')
    print("parfum", id_parfum)

    sql = '''SELECT * FROM ligne_panier WHERE utilisateur_id = %s AND parfum_id = %s'''
    mycursor.execute(sql, (id_client, id_parfum))
    parfum_panier = mycursor.fetchone()
    print("panier article", parfum_panier)
    if parfum_panier != None:
        sql = '''UPDATE parfum SET stock = stock + %s WHERE id_parfum = %s'''
        mycursor.execute(sql, (parfum_panier['quantite'], id_parfum))
        sql2 = '''DELETE FROM ligne_panier WHERE utilisateur_id = %s AND parfum_id = %s'''
        mycursor.execute(sql2, (id_client, id_parfum))
        get_db().commit()
    return redirect('/client/parfum/show')


@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)
    if filter_word:
        session['filter_word'] = filter_word
    else:
        session.pop('filter_word', None)
    if filter_prix_min:
        session['filter_prix_min'] = filter_prix_min
    else:
        session.pop('filter_prix_min', None)
    if filter_prix_max:
        session['filter_prix_max'] = filter_prix_max
    else:
        session.pop('filter_prix_max', None)
    if filter_types:
        session['filter_types'] = filter_types
    else:
        session.pop('filter_types', None)

    return redirect('/client/parfum/show')


@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    if 'filter_word' in session:
        session.pop('filter_word', None)
    if 'filter_prix_min' in session:
        session.pop('filter_prix_min', None)
    if 'filter_prix_max' in session:
        session.pop('filter_prix_max', None)
    if 'filter_types' in session:
        session.pop('filter_types', None)
    return redirect('/client/parfum/show')