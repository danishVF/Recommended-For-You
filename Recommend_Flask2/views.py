"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, flash, redirect, url_for
from Recommend_Flask2 import app
import os

from models import r_models


app.secret_key = "secret key"
allowed_model_types = ["model1", "model2"]

model_to_predict_cos = r_models.load_model("model1")
model_to_predict_cos_full = r_models.load_model("model2")
list_users = []
for i in range(0, 18204):
    list_users.append(i)
user_id = 'dummy_id'
item_id = 'productId'
recommendations_cos = r_models.create_output(model_to_predict_cos, list_users, 10, print_csv=True)
recommendations_cos_full = r_models.create_output(model_to_predict_cos_full, list_users, 10, print_csv=True)

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text1'] # is the dummy id
    text2 = request.form['text2'].lower() # is the model
    if text == '' or text2 == '':
        flash("no text was entered in one of the boxes")
        return redirect(request.url)
    if text.isdigit() and text2 in allowed_model_types:
        id = int(text)
        if text2 == "model1":
            list_items = r_models.customer_recommendation(recommendations_cos, id, text2)
        else:
            list_items = r_models.customer_recommendation(recommendations_cos_full, id, text2)
        string_id = list_items[0]
        recommend_names = list_items[1]
        bought_names = list_items[2]
        # string_id = list_string_ids[0].replace('|', ', ')
        # list_ids = list_string_ids[0].split('|')
        return render_template("index.html", prediction=string_id, names=recommend_names, bought=bought_names)
    else:
        flash("Please enter the valid credentials according to the description")
        return redirect(request.url)
   
