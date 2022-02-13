#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import render_template

from connexion_db import get_db

client_velo = Blueprint('client_velo', __name__,
                        template_folder='templates')

@client_velo.route('/client/index')
@client_velo.route('/client/velo/show')      # remplace /client
def client_velo_show():                                 # remplace client_inde
    mycursor = get_db().cursor()
    mycursor.execute("SELECT * FROM VELO;")
    velos = mycursor.fetchall()

    mycursor.execute("SELECT * FROM TYPE_VELO;")
    types_velos = mycursor.fetchall()

    mycursor.execute("SELECT * FROM TAILLE;")
    tailles = mycursor.fetchall()

    mycursor.execute("SELECT * FROM COULEUR;")
    couleurs = mycursor.fetchall()

    mycursor.execute("SELECT * FROM PANIER INNER JOIN VELO ON PANIER.id_velo = VELO.id_velo")
    velos_panier = mycursor.fetchall()

    print(velos)
    print("---")
    print(velos_panier)
    prix_total = None
    return render_template('client/boutique/panier_velo.html', velos=velos, velosPanier=velos_panier, prix_total=prix_total, itemsFiltre=types_velos, tailles=tailles, couleurs=couleurs)

@client_velo.route('/client/velo/details/<int:id>', methods=['GET'])
def client_velo_details(id):
    mycursor = get_db().cursor()
    velo = None
    commentaires = None
    commandes_velos = None
    return render_template('client/boutique/velo_details.html', velo=velo, commentaires=commentaires, commandes_velos=commandes_velos)