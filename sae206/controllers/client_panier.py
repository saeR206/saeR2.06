#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

from datetime import datetime

client_panier = Blueprint('client_panier', __name__,
                        template_folder='templates')


@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    quantite = request.form.get("quantite")
    id_velo = request.form.get("id_velo")
    mycursor.execute("SELECT * FROM VELO WHERE id_velo=%s;", (id_velo))
    velo = mycursor.fetchone()

    mycursor.execute("SELECT * FROM PANIER WHERE id_velo=%s;", (id_velo))
    panier = mycursor.fetchone()

    if not panier :
        mycursor.execute("INSERT INTO PANIER (date_ajout, prix_unit, quantite, id_velo, id_user) VALUES (%s,%s,%s,%s,%s);", (datetime.now(), velo['prix_velo'], quantite, id_velo, session['user_id']));
    elif (str(quantite)[0] != "-") :
        mycursor.execute("UPDATE PANIER SET quantite = quantite + %s WHERE id_velo=%s;", (quantite, id_velo))

    get_db().commit()

    return redirect('/client/velo/show')


@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_velo = request.form.get("id_velo")
    mycursor.execute("SELECT * FROM PANIER WHERE id_velo=%s;", (id_velo))
    quantite = request.form.get("quantite")

    if int(quantite)<=1:
        sql = """DELETE FROM PANIER WHERE id_user=%s and id_velo=%s;"""
        tuple_delete = (session["user_id"], id_velo)
        mycursor.execute(sql, tuple_delete)
    else:
        mycursor.execute("UPDATE PANIER SET quantite=quantite-1 WHERE id_velo=%s;", (id_velo))

    get_db().commit()

    return redirect('/client/velo/show')


@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    mycursor.execute("SELECT * FROM PANIER WHERE id_user=%s", (session["user_id"]))
    mycursor.execute("DELETE FROM PANIER WHERE id_user=%s;", (session["user_id"]))
    get_db().commit()
    return redirect('/client/velo/show')
    #return redirect(url_for('client_index'))


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_velo = request.form.get('id_velo', '')
    mycursor.execute("SELECT * FROM PANIER WHERE id_velo=%s", (id_velo))
    mycursor.execute("DELETE FROM PANIER WHERE id_velo=%s;", (id_velo))
    get_db().commit()
    return redirect('/client/velo/show')
    #return redirect(url_for('client_index'))


@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    # SQL
    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)

    return redirect('/client/velo/show')
    #return redirect(url_for('client_index'))


@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    session.pop('filter_word', None)
    session.pop('filter_prix_min', None)
    session.pop('filter_prix_max', None)
    session.pop('filter_types', None)
    print("suppr filtre")
    return redirect('/client/velo/show')
    #return redirect(url_for('client_index'))