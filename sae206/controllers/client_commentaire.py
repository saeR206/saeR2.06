#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

client_commentaire = Blueprint('client_commentaire', __name__,
                        template_folder='templates')

@client_commentaire.route('/client/comment/add', methods=['POST'])
def client_comment_add():
    mycursor = get_db().cursor()
    id_velo = request.form.get('id_velo', None)

    return redirect('/client/velo/details/'+id_velo)
    #return redirect(url_for('client_velo_details', id=int(id_velo)))

@client_commentaire.route('/client/comment/delete', methods=['POST'])
def client_comment_detete():
    mycursor = get_db().cursor()
    id_velo = request.form.get('id_velo', None)

    return redirect('/client/velo/details/'+id_velo)
    #return redirect(url_for('client_velo_details', id=int(id_velo)))