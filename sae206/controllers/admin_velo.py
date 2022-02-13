#! /usr/bin/python
# -*- coding:utf-8 -*-
import os

from flask import Blueprint
from flask import request, render_template, redirect, url_for, flash

from connexion_db import get_db


admin_velo = Blueprint('admin_velo', __name__,
                        template_folder='templates')

@admin_velo.route('/admin/velo/show', methods=['GET','POST'])
def show_velo():
    mycursor = get_db().cursor()
    mycursor.execute("SELECT VELO.id_velo, nom_velo, CONCAT(TYPE_VELO.libelle_type_velo,' (',VELO.id_type_velo,')') AS type_velo, CONCAT(TAILLE.libelle_taille,' (',VELO.id_taille,')') AS taille, CONCAT(COULEUR.libelle_couleur,' (',VELO.id_couleur,')') AS couleur, CONCAT(FOURNISSEUR.nom_fournisseur,' (',FOURNISSEUR.id_fournisseur,')') AS fournisseur, prix_velo, stock, img_velo FROM VELO INNER JOIN TYPE_VELO ON VELO.id_type_velo = TYPE_VELO.id_type_velo INNER JOIN TAILLE ON VELO.id_taille = TAILLE.id_taille INNER JOIN COULEUR on VELO.id_couleur = COULEUR.id_couleur INNER JOIN fabrique ON VELO.id_velo = fabrique.id_velo INNER JOIN FOURNISSEUR ON fabrique.id_fournisseur = FOURNISSEUR.id_fournisseur ORDER BY id_velo;")
    velo = mycursor.fetchall()

    imagesList = os.listdir('static/images')
    imagesList = ['static/images/' + images for images in imagesList]
    return render_template('admin/velo/show_velo.html', velo=velo, imagesList=imagesList)

@admin_velo.route('/admin/velo/add', methods=['GET'])
def add_velo():
    mycursor = get_db().cursor()
    mycursor.execute("SELECT * FROM TYPE_VELO;")
    type_velo = mycursor.fetchall()

    mycursor.execute("SELECT * FROM TAILLE;")
    taille = mycursor.fetchall()

    mycursor.execute("SELECT * FROM COULEUR;")
    couleur = mycursor.fetchall()

    mycursor.execute("SELECT * FROM FOURNISSEUR;")
    fournisseur = mycursor.fetchall()
    return render_template('admin/velo/add_velo.html', type_velo=type_velo, taille=taille, couleur=couleur, fournisseur=fournisseur)

@admin_velo.route('/admin/velo/add', methods=['POST'])
def valid_add_velo():
    mycursor = get_db().cursor()
    nom_velo = request.form.get('nom_velo', '')
    id_type_velo = request.form.get('id_type_velo', '')
    id_taille = request.form.get('id_taille', '')
    id_couleur = request.form.get('id_couleur', '')
    prix_velo = request.form.get('prix_velo', '')
    stock = request.form.get('stock', '')
    img_velo = request.form.get('img_velo', '')

    if nom_velo == '' or id_type_velo == '' or id_taille == '' or id_couleur == '' or prix_velo == '' or stock == '' or img_velo == '':
        flash('Veuillez remplir toutes les informations !')
        return redirect(url_for('admin_velo.add_velo'))

    val = [nom_velo, id_type_velo, id_taille, id_couleur, prix_velo, stock, img_velo]
    mycursor.execute("INSERT INTO VELO(nom_velo, id_type_velo, id_taille, id_couleur, prix_velo, stock, img_velo) VALUES (%s,%s,%s,%s,%s,%s,%s);", val)
    get_db().commit()

    message = 'Vélo ajouté : Nom : ' + nom_velo + ' - Type de vélo : ' + id_type_velo + ' - Taille : ' + id_taille + ' - Couleur :' + id_couleur + ' - Prix : ' + prix_velo + ' €' + ' - Stock : ' +  stock + ' - Image : ' + img_velo
    flash(message)
    return redirect(url_for('admin_velo.show_velo'))

@admin_velo.route('/admin/velo/delete', methods=['GET'])
def delete_velo():
    mycursor = get_db().cursor()
    id_velo = request.args['id_velo']
    mycursor.execute("SELECT * FROM VELO WHERE id_velo=%s;", (id_velo))

    vel = mycursor.fetchone()
    nom_velo = str(vel['nom_velo'])
    mycursor.execute("DELETE FROM VELO WHERE id_velo=%s;", (id_velo))
    get_db().commit()

    flash('Vélo supprimé : - Nom : ' + nom_velo)
    return redirect(url_for('admin_velo.show_velo'))

@admin_velo.route('/admin/velo/edit/<int:id>', methods=['GET'])
def edit_velo(id):
    mycursor = get_db().cursor()
    id_velo = request.args['id_velo']
    mycursor.execute("SELECT * FROM VELO INNER JOIN TYPE_VELO ON VELO.id_type_velo = TYPE_VELO.id_type_velo INNER JOIN TAILLE ON VELO.id_taille = TAILLE.id_taille INNER JOIN COULEUR on VELO.id_couleur = COULEUR.id_couleur INNER JOIN fabrique ON VELO.id_velo = fabrique.id_velo INNER JOIN FOURNISSEUR ON fabrique.id_fournisseur = FOURNISSEUR.id_fournisseur WHERE VELO.id_velo = %s", (id_velo))
    vel = mycursor.fetchone()

    mycursor.execute("SELECT * FROM TYPE_VELO;")
    type_velo = mycursor.fetchall()

    mycursor.execute("SELECT * FROM TAILLE;")
    taille = mycursor.fetchall()

    mycursor.execute("SELECT * FROM COULEUR;")
    couleur = mycursor.fetchall()

    mycursor.execute("SELECT * FROM FOURNISSEUR;")
    fournisseur = mycursor.fetchall()
    return render_template('admin/velo/edit_velo.html', vel=vel, type_velo=type_velo, taille=taille, couleur=couleur, fournisseur=fournisseur, id_velo=id_velo)

@admin_velo.route('/admin/velo/edit', methods=['POST'])
def valid_edit_velo():
    mycursor = get_db().cursor()
    id_velo = request.args.get('id', '')
    nom_velo = request.form.get('nom_velo', '')
    id_type_velo = request.form.get('id_type_velo', '')
    id_taille = request.form.get('id_taille', '')
    id_couleur = request.form.get('id_couleur', '')
    prix_velo = request.form.get('prix_velo', '')
    stock = request.form.get('stock', '')
    img_velo = request.form.get('img_velo', '')

    if nom_velo == '' or id_type_velo == '' or id_taille == '' or id_couleur == '' or prix_velo == '' or stock == '' or img_velo == '':
        flash('Veuillez remplir toutes les informations !')
        return redirect(url_for('admin_velo.edit_velo'))

    mycursor.execute("UPDATE VELO SET nom_velo = %s, id_type_velo = %s, id_taille = %s, id_couleur = %s, prix_velo = %s, stock = %s, img_velo = %s WHERE id_velo = %s", (nom_velo, id_type_velo, id_taille, id_couleur, prix_velo, stock, img_velo, id_velo))
    get_db().commit()

    message = 'Vélo modifié : Nom : ' + nom_velo + ' - Type de vélo : ' + id_type_velo + ' - Taille : ' + id_taille + ' - Couleur : ' + id_couleur + ' - Prix : ' + prix_velo + ' € - Stock : '+  stock + ' - Image : ' + img_velo
    flash(message)
    return redirect(url_for('admin_velo.show_velo'))
