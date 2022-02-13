#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

admin_commande = Blueprint('admin_commande', __name__,
                        template_folder='templates')

@admin_commande.route('/admin/commande/index')
def admin_index():
    return render_template('admin/layout_admin.html')


@admin_commande.route('/admin/commande/show', methods=['GET','POST'])
def admin_commande_show():
    mycursor = get_db().cursor()
    mycursor.execute("SELECT id_commande, date_achat, libelle_etat FROM COMMANDE INNER JOIN ETAT on COMMANDE.id_etat = ETAT.id_etat INNER JOIN UTILISATEUR on COMMANDE.id_user = UTILISATEUR.id_user;")
    commandes = mycursor.fetchall()

    mycursor.execute("SELECT nom_velo, quantite, prix_unit, quantite*prix_unit AS prix_ligne FROM VELO INNER JOIN PANIER on VELO.id_velo = PANIER.id_velo;")
    velos_commande = mycursor.fetchall()
    get_db().commit()
    return render_template('admin/commandes/show.html', commandes=commandes, velos_commande=velos_commande)


@admin_commande.route('/admin/commande/valider', methods=['GET','POST'])
def admin_commande_valider():
    mycursor = get_db().cursor()
    id_commande = request.form.get('id_commande','')

    mycursor.execute("UPDATE COMMANDE SET id_etat = 2 WHERE id_commande=%s", (id_commande))
    get_db().commit()
    flash('Commande n°' + id_commande + 'expédiée !')
    return redirect('/admin/commande/show')

@admin_commande.route('/admin/commande/show-client')
def admin_show_client():
    mycursor = get_db().cursor()
    mycursor.execute("SELECT * FROM UTILISATEUR WHERE role='ROLE_client';")
    clients = mycursor.fetchall()
    get_db().commit()
    return render_template('admin/commandes/show_clients.html', clients=clients)
