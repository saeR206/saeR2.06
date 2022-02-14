#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime
from connexion_db import get_db

from datetime import datetime

client_commande = Blueprint('client_commande', __name__,
                        template_folder='templates')


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()
    id_user = session['user_id']
    mycursor.execute("SELECT * FROM PANIER WHERE id_user = %s;",(id_user))
    items_panier = mycursor.fetchall()

    if items_panier is None or len(items_panier) < 1 :
        flash('Aucun article dans le panier')
        return redirect('/client/velo/show')

    date_commande = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    mycursor.execute("SELECT SUM(prix_unit*quantite) AS prix_t FROM PANIER")
    prix_total = mycursor.fetchone()
    prix_total = prix_total["prix_t"]

    mycursor.execute("SELECT SUM(quantite) AS nombre FROM PANIER")
    nombre_velo = mycursor.fetchone()
    nombre_velo = nombre_velo["nombre"]

    mycursor.execute("INSERT INTO COMMANDE(date_achat, id_user, id_etat, prix_total, nombre_velo) VALUES (%s,%s,%s,%s,%s)", (date_commande, id_user,'1', prix_total, nombre_velo))
    mycursor.execute("SELECT last_insert_id() AS last_insert_id;")
    id_commande = mycursor.fetchone()

    for item in items_panier :
        mycursor.execute("DELETE FROM PANIER WHERE id_user = %s AND id_velo = %s;", (id_user, item['id_velo']))
        mycursor.execute("SELECT prix_velo FROM VELO WHERE id_velo = %s;", item['id_velo'])
        prix = mycursor.fetchone()

        mycursor.execute("INSERT INTO ligne_commande(id_commande, id_velo, prix_unit, quantite) VALUES (%s,%s,%s,%s)", (id_commande['last_insert_id'], item['id_velo'], prix['prix_velo'], item['quantite']))

    get_db().commit()
    flash('Commande ajoutée')
    return redirect('/client/velo/show')
    #return redirect(url_for('client_index')

@client_commande.route('/client/commande/show', methods=['GET','POST'])
def client_commande_show():
    mycursor = get_db().cursor()

    id_commande = request.form.get("id_commande", "")

    mycursor.execute("SELECT * FROM COMMANDE INNER JOIN ETAT on COMMANDE.id_etat = ETAT.id_etat INNER JOIN UTILISATEUR on COMMANDE.id_user = UTILISATEUR.id_user WHERE COMMANDE.id_user=%s;", (session["user_id"]))
    commandes = mycursor.fetchall()

    # mycursor.execute("SELECT nom_velo, quantite, prix_unit, quantite*prix_unit AS prix_ligne FROM VELO INNER JOIN PANIER on VELO.id_velo = PANIER.id_velo;")
    # velos_commande = mycursor.fetchall()

    if id_commande != None:
        mycursor.execute("SELECT * FROM ligne_commande INNER JOIN VELO ON ligne_commande.id_velo = VELO.id_velo WHERE id_commande=%s", (id_commande))
        ligne_commande = mycursor.fetchall()
        return render_template('client/commandes/show.html', commandes=commandes, ligne_commande=ligne_commande)

    return render_template('client/commandes/show.html', commandes=commandes, velos_commande=velos_commande)