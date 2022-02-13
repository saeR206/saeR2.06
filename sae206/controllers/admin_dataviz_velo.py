#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db
import matplotlib.pyplot as plt
admin_dataviz_velo = Blueprint('admin_dataviz_velo', __name__,
                        template_folder='templates')

@admin_dataviz_velo.route('/admin/type-velo/bilan-stock')
def show_type_velo_stock():
    mycursor = get_db().cursor()
    mycursor.execute("SELECT TYPE_VELO.id_type_velo, libelle_type_velo, SUM(prix_velo) AS cout_type_velo FROM VELO INNER JOIN TYPE_VELO ON VELO.id_type_velo = TYPE_VELO.id_type_velo GROUP BY VELO.id_type_velo;")
    types_velos_cout = mycursor.fetchall()

    labels = []
    values = []
    # plt.bar(types_velos_cout['libelle_type_velo'], types_velos_cout['cout_type_velo'])
    # plt.ylabel("Coût (en €)")
    # plt.show()

    cout_total = 0
    return render_template('admin/dataviz/etat_type_velo_stock.html',
                           types_velos_cout=types_velos_cout, cout_total=cout_total
                           , labels=labels, values=values)


@admin_dataviz_velo.route('/admin/velo/bilan')
def show_velo_bilan():
    mycursor = get_db().cursor()

    types_velos_cout = []
    labels = []
    values = []
    cout_total = 0
    return render_template('admin/dataviz/etat_velo_vente.html',
                           types_velos_cout=types_velos_cout, cout_total=cout_total
                           , labels=labels, values=values)
