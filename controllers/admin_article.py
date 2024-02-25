#! /usr/bin/python
# -*- coding:utf-8 -*-
import math
import os.path
from random import random

from flask import Blueprint
from flask import request, render_template, redirect, flash
#from werkzeug.utils import secure_filename

from connexion_db import get_db

admin_article = Blueprint('admin_article', __name__,
                          template_folder='templates')


@admin_article.route('/admin/article/show')
def show_article():
    mycursor = get_db().cursor()
    sql = '''  SELECT parfum.id_parfum AS id_article,
                parfum.image AS image
                , parfum.type_parfum_id
                , parfum.nom_parfum AS nom
                , parfum.prix_parfum AS prix
                , stock 
                FROM parfum
                ORDER BY parfum.nom_parfum;'''
    mycursor.execute(sql)
    parfums = mycursor.fetchall()
    sql = '''  SELECT * FROM genre;'''
    mycursor.execute(sql)
    type_parfum = mycursor.fetchall()
    return render_template('admin/article/show_article.html', parfums=parfums, type_parfum=type_parfum)


@admin_article.route('/admin/article/add', methods=['GET'])
def add_article():
    mycursor = get_db().cursor()
    sql = '''SELECT * FROM genre;'''
    mycursor.execute(sql)
    genre = mycursor.fetchall()
    sql = '''SELECT * FROM volume;'''
    mycursor.execute(sql)
    volume= mycursor.fetchall()
    return render_template('admin/article/add_article.html', genres=genre, volume=volume)


@admin_article.route('/admin/article/add', methods=['POST'])
def valid_add_article():
    mycursor = get_db().cursor()

    nom = request.form.get('nom', '')
    type_parfum_id = request.form.get('type_parfum_id', '')
    prix = request.form.get('prix', '')
    description = request.form.get('description', '')
    image = request.files.get('image', '')
    volume_id = request.form.get('volume_id', '')
    conditionnement = request.form.get('conditionnement', '')
    fournisseur = request.form.get('fournisseur', '')
    marque = request.form.get('marque', '')
    stock = request.form.get('stock', '')


    if image:
        filename = 'img_upload'+ str(int(2147483647 * random())) + '.png'
        image.save(os.path.join('static/images/', filename))
    else:
        print("erreur")
        filename=None

    sql = '''INSERT INTO parfum(id_parfum, nom_parfum, prix_parfum, volume_id, type_parfum_id, conditionnement, description, fournisseur, marque, stock, image) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

    tuple_add = (nom, prix, volume_id, type_parfum_id, conditionnement, description, fournisseur, marque, stock, filename)
    print(tuple_add)
    mycursor.execute(sql, tuple_add)
    get_db().commit()

    print(u'article ajouté , nom: ', nom, ' - type_article:', type_parfum_id, ' - prix:', prix,
          ' - description:', description, ' - image:', image)
    message = u'article ajouté , nom:' + nom + '- type_article:' + type_parfum_id + ' - prix:' + prix + ' - description:' + description + ' - image:' + str(
        image)
    flash(message, 'alert-success')
    return redirect('/admin/article/show')


@admin_article.route('/admin/article/delete', methods=['GET'])
def delete_article():
    id_article=request.args.get('id_article')
    mycursor = get_db().cursor()
    sql = ''' requête admin_article_3 '''
    mycursor.execute(sql, id_article)
    nb_declinaison = mycursor.fetchone()
    if nb_declinaison['nb_declinaison'] > 0:
        message= u'il y a des declinaisons dans cet article : vous ne pouvez pas le supprimer'
        flash(message, 'alert-warning')
    else:
        sql = ''' requête admin_article_4 '''
        mycursor.execute(sql, id_article)
        article = mycursor.fetchone()
        print(article)
        image = article['image']

        sql = ''' requête admin_article_5  '''
        mycursor.execute(sql, id_article)
        get_db().commit()
        if image != None:
            os.remove('static/images/' + image)

        print("un article supprimé, id :", id_article)
        message = u'un article supprimé, id : ' + id_article
        flash(message, 'alert-success')

    return redirect('/admin/article/show')


@admin_article.route('/admin/article/edit', methods=['GET'])
def edit_article():
    id_article=request.args.get('id_article')
    print(id_article)
    mycursor = get_db().cursor()
    sql = '''
    SELECT parfum.id_parfum AS id_article,
        parfum.image AS image
        , parfum.nom_parfum AS nom
        , parfum.prix_parfum AS prix
        , parfum.description AS description
        , conditionnement, fournisseur, stock
        , marque, volume_id, type_parfum_id AS id_type_article
        FROM parfum
        WHERE parfum.id_parfum = %s 
    '''
    mycursor.execute(sql, id_article)
    parfum = mycursor.fetchone()
    sql = '''
    SELECT id_genre as id_type_article , nom_genre AS libelle  FROM genre'''
    mycursor.execute(sql)
    types_article = mycursor.fetchall()
    sql = '''SELECT * FROM volume;'''
    mycursor.execute(sql)
    volume = mycursor.fetchall()

    return render_template('admin/article/edit_article.html'
                            ,parfum=parfum
                            ,types_article=types_article
                           , volume=volume
                           )


@admin_article.route('/admin/article/edit', methods=['POST'])
def valid_edit_article():
    mycursor = get_db().cursor()
    nom = request.form.get('nom')
    id_article = request.form.get('id_article')
    image = request.files.get('image', '')
    id_type_article = request.form.get('id_type_article', '')
    prix = request.form.get('prix', '')
    description = request.form.get('description')
    volume_id = request.form.get('volume_id', '')
    conditionnement = request.form.get('conditionnement', '')
    fournisseur = request.form.get('fournisseur', '')
    marque = request.form.get('marque', '')
    stock = request.form.get('stock', '')
    sql = ''' SELECT image from parfum WHERE id_parfum=%s '''
    mycursor.execute(sql, id_article)
    image_nom = mycursor.fetchone()
    image_nom = image_nom['image']
    if image:
        if image_nom != "" and image_nom is not None and os.path.exists(
                os.path.join(os.getcwd() + "/static/images/", image_nom)):
            os.remove(os.path.join(os.getcwd() + "/static/images/", image_nom))
        # filename = secure_filename(image.filename)
        if image:
            filename = 'img_upload_' + str(int(2147483647 * random())) + '.png'
            image.save(os.path.join('static/images/', filename))
            image_nom = filename

    print(nom, prix, volume_id, id_type_article, conditionnement, description, fournisseur, marque, stock,image_nom, id_article)
    sql = '''UPDATE parfum SET nom_parfum = %s , prix_parfum = %s ,
            volume_id=%s, type_parfum_id=%s, conditionnement=%s,
            description =%s, fournisseur=%s, marque=%s, stock=%s, image=%s WHERE id_parfum=%s; '''
    mycursor.execute(sql, (nom, prix, volume_id, id_type_article, conditionnement, description, fournisseur, marque, stock,image_nom, id_article))

    get_db().commit()
    if image_nom is None:
        image_nom = ''

    message = u'parfum modifié , nom:' + nom + '- type_article :' + id_type_article + '- volume -' + volume_id +' - prix:' + prix  + ' - image:' + image_nom + ' - description: ' + description +'- conditionnement -' + conditionnement + '- fournisseur -' + fournisseur + 'marque' + marque + 'stock' + stock
    flash(message, 'alert-success')
    return redirect('/admin/article/show')







@admin_article.route('/admin/article/avis/<int:id>', methods=['GET'])
def admin_avis(id):
    mycursor = get_db().cursor()
    article=[]
    commentaires = {}
    return render_template('admin/article/show_avis.html'
                           , article=article
                           , commentaires=commentaires
                           )


@admin_article.route('/admin/comment/delete', methods=['POST'])
def admin_avis_delete():
    mycursor = get_db().cursor()
    article_id = request.form.get('idArticle', None)
    userId = request.form.get('idUser', None)

    return admin_avis(article_id)
