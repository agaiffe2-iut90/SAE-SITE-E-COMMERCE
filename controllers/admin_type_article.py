#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_type_article = Blueprint('admin_type_article', __name__,
                        template_folder='templates')

@admin_type_article.route('/admin/type-article/show')
def show_type_article():
    mycursor = get_db().cursor()
    sql = '''SELECT genre.id_genre AS id_type_article,
            genre.nom_genre AS libelle,
            COUNT(parfum.id_parfum) AS nbr_articles
            FROM genre
            LEFT JOIN parfum ON genre.id_genre = parfum.type_parfum_id
            GROUP BY genre.id_genre, genre.nom_genre;
'''
    mycursor.execute(sql)
    types_article = mycursor.fetchall()
    return render_template('admin/type_article/show_type_article.html', types_article=types_article)

@admin_type_article.route('/admin/type-article/add', methods=['GET'])
def add_type_article():
    return render_template('admin/type_article/add_type_article.html')

@admin_type_article.route('/admin/type-article/add', methods=['POST'])
def valid_add_type_article():
    print('''ajout d'un parfum dans le tableau''')
    mycursor = get_db().cursor()
    libelle = request.form.get('libelle', '')
    tuple_insert = (libelle)
    print(tuple_insert)
    sql = "INSERT INTO genre(id_genre, nom_genre) VALUES (NULL, %s);"
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    message = u'type ajouté , libellé :'+libelle
    flash(message, 'alert-success')
    return redirect('/admin/type-article/show')

@admin_type_article.route('/admin/type-article/delete', methods=['GET'])
def delete_type_article():
    print('''suppression d'un type de parfum''')
    id_type_article = request.args.get('id_type_article', '')
    print(id_type_article)
    mycursor = get_db().cursor()
    tuple_param = id_type_article
    query = "SELECT COUNT(*) AS signe FROM parfum WHERE type_parfum_id=%s "  # compter AS SIGN
    mycursor.execute(query, tuple_param)
    sign = mycursor.fetchone().get("signe")
    print(sign)
    if sign != 0:
        message = u'Suppression impossible ! (car contrainte clé étrangère)'
        print(message)
        flash(message, 'warning-success')
    else:
        sql = "DELETE FROM genre WHERE id_genre=%s;;"
        mycursor.execute(sql, tuple_param)
        get_db().commit()
        print(request.args)
        print(request.args.get('id_type_article'))
        id_type_article = request.args.get('id_type_article', 0)
        message = u'un type de parfum supprimé, id : ' + id_type_article
        flash(message, 'alert-warning')
    return redirect('/admin/type-article/show')

@admin_type_article.route('/admin/type-article/edit', methods=['GET'])
def edit_type_article():
    id_type_article = request.args.get('id_type_article', '')
    mycursor = get_db().cursor()
    sql = '''SELECT id_genre AS id_type_article, nom_genre AS libelle
             FROM genre WHERE id_genre=%s;'''
    mycursor.execute(sql, (id_type_article,))
    type_article = mycursor.fetchone()
    return render_template('admin/type_article/edit_type_article.html', type_article=type_article)

@admin_type_article.route('/admin/type-article/edit', methods=['POST'])
def valid_edit_type_article():
    libelle = request.form['libelle']
    id_type_article = request.form.get('id_type_article', '')
    tuple_update = (libelle, id_type_article)
    print(tuple_update)
    mycursor = get_db().cursor()
    sql = '''UPDATE genre SET nom_genre=%s WHERE id_genre=%s;'''
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    flash(u'type parfum modifié, id: ' + id_type_article + " libelle : " + libelle, 'alert-success')
    return redirect('/admin/type-article/show')








