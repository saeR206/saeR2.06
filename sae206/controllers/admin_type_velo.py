#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint, url_for
from flask import request, render_template, redirect, flash

from connexion_db import get_db

admin_type_velo = Blueprint('admin_type_velo', __name__,
                        template_folder='templates')

@admin_type_velo.route('/admin/type-velo/show')
def show_type_velo():
    mycursor = get_db().cursor()
    mycursor.execute("SELECT libelle_type_velo, TYPE_VELO.id_type_velo, COUNT(VELO.id_velo) AS nb_velos FROM TYPE_VELO INNER JOIN VELO ON TYPE_VELO.id_type_velo = VELO.id_type_velo GROUP BY id_type_velo;")

    type_velo = mycursor.fetchall()
    return render_template('admin/type_velo/show_type_velo.html', type_velo=type_velo)

@admin_type_velo.route('/admin/type-velo/add', methods=['GET'])
def add_type_velo():
    return render_template('admin/type_velo/add_type_velo.html')

@admin_type_velo.route('/admin/type-velo/add', methods=['POST'])
def valid_add_type_velo():
    mycursor = get_db().cursor()
    libelle_type_velo = request.form.get('libelle_type_velo')

    if libelle_type_velo == '':
        flash('Veuillez remplir le libellé !')
        return redirect(url_for('admin_type_velo.add_type_velo'))

    mycursor.execute("INSERT INTO TYPE_VELO(libelle_type_velo) VALUES (%s);", (libelle_type_velo))
    get_db().commit()

    flash('Type de vélo ajouté : ' + libelle_type_velo)
    return redirect(url_for('admin_type_velo.show_type_velo'))

@admin_type_velo.route('/admin/type-velo/delete/<int:id>', methods=['GET'])
def delete_type_velo(id):
    mycursor = get_db().cursor()
    id_type_velo = request.args['id_type_velo']
    mycursor.execute("SELECT libelle_type_velo FROM TYPE_VELO WHERE id_type_velo=%s;", (id_type_velo))

    libelle_type_velo = mycursor.fetchone()
    mycursor.execute("SELECT TYPE_VELO.id_type_velo, COUNT(VELO.nom_velo) AS nb FROM VELO INNER JOIN TYPE_VELO ON VELO.id_type_velo = TYPE_VELO.id_type_velo WHERE TYPE_VELO.id_type_velo=%s GROUP BY (TYPE_VELO.id_type_velo)", (id_type_velo))

    verif_type = mycursor.fetchone()
    if verif_type['nb'] == 0 :
        mycursor.execute("SELECT * FROM TYPE_VELO WHERE id_type_velo = %s;", (id_type_velo))
        type_velo = mycursor.fetchone()
        type_delete = str(type_velo['libelle_type_velo'])
        mycursor.execute("DELETE FROM TYPE_VELO WHERE id_type_velo = %s;", (id_type_velo))
        get_db().commit()

        flash('Type de vélo supprimé : ' + type_delete)
        return redirect(url_for('admin_type_velo.show_type_velo'))

    elif verif_type['nb'] > 0 :
        mycursor.execute("SELECT * FROM VELO INNER JOIN TYPE_VELO ON VELO.id_type_velo = TYPE_VELO.id_type_velo WHERE TYPE_VELO.id_type_velo=%s ORDER BY VELO.nom_velo;", (id_type_velo))
        velo = mycursor.fetchall()

        mycursor.execute("SELECT TYPE_VELO.id_type_velo, COUNT(VELO.nom_velo) AS nb FROM VELO INNER JOIN TYPE_VELO ON VELO.id_type_velo = TYPE_VELO.id_type_velo WHERE TYPE_VELO.id_type_velo=%s ORDER BY VELO.nom_velo;",(id_type_velo))
        nombre = mycursor.fetchone()
        type_delete = nombre['nb']

        return render_template('admin/type_velo/delete_type_velo.html', velo=velo, type_delete=type_delete, libelle_type_velo=libelle_type_velo)

@admin_type_velo.route('/admin/type-velo/delete', methods=['GET'])
def delete_velo_types():
    mycursor = get_db().cursor()
    id_type_velo = request.args['id']
    id_velo = request.args['id_velo']
    mycursor.execute("SELECT * FROM VELO WHERE id_velo=%s;", (id_velo))
    vel = mycursor.fetchone()

    nom_velo = str(vel['nom_velo'])
    id_taille = str(vel['id_taille'])
    id_couleur = str(vel['id_couleur'])
    prix_velo = str(vel['prix_velo'])
    stock = str(vel['stock'])
    img_velo = str(vel['img_velo'])

    message = 'Vélo supprimé : Nom : ' + nom_velo + ' - Type de vélo : ' + id_type_velo + ' - Taille : ' + id_taille + ' - Couleur :' + id_couleur + ' - Prix : ' + prix_velo + ' - Stock : ' + stock + ' - Image : ' + img_velo
    flash(message)
    mycursor.execute("DELETE FROM VELO WHERE id_velo=%s;", (id_velo))
    get_db().commit()
    return redirect(url_for('admin_type_velo.delete_type_velo', id=id_type_velo, id_type_velo=id_type_velo, id_velo=id_velo))

@admin_type_velo.route('/admin/type-velo/edit/<int:id>', methods=['GET'])
def edit_type_velo(id):
    mycursor = get_db().cursor()
    id_type_velo = request.args['id_type_velo']

    mycursor.execute("SELECT * FROM TYPE_VELO WHERE id_type_velo = %s;", (id_type_velo))
    type = mycursor.fetchone()
    return render_template('admin/type_velo/edit_type_velo.html', type=type)

@admin_type_velo.route('/admin/type-velo/edit', methods=['POST'])
def valid_edit_type_velo():
    mycursor = get_db().cursor()
    id_type_velo = request.form.get('id','')
    libelle_type_velo = request.form['libelle_type_velo']

    if libelle_type_velo == '' :
        flash('Veuillez remplir le libellé !')
        return redirect(url_for('admin_type_velo.edit_type_velo'))

    mycursor.execute("UPDATE TYPE_VELO SET libelle_type_velo = %s WHERE id_type_velo = %s;", (libelle_type_velo, id_type_velo))
    get_db().commit()
    flash('Type de vélo modifié : ' + libelle_type_velo)
    return redirect(url_for('admin_type_velo.show_type_velo'))






