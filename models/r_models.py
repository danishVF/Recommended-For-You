import os
import turicreate as tc
import numpy as np
import pandas as pd

def load_model(model_type):
    cwd = os.getcwd()
    if model_type == "model1":
        path = cwd + "/Recommend_Flask2/turi_cos_model/turi_cos_model"
    elif model_type == "model2":
        path = cwd + "/Recommend_Flask2/turi_cos_full/turi_cos_full"
    model = tc.load_model(path)
    return model

def create_output(model, users_to_recommend, n_rec, print_csv=True):
    recomendation = model.recommend(users=users_to_recommend, k=n_rec)
    df_rec = recomendation.to_dataframe()
    df_rec['recommendedProducts'] = df_rec.groupby(['dummy_id'])['productId'] \
        .transform(lambda x: '|'.join(x.astype(str)))
    df_output = df_rec[['dummy_id', 'recommendedProducts']].drop_duplicates() \
        .sort_values('dummy_id').set_index('dummy_id')
    return df_output

def customer_recommendation(df_output, customer_id, model_type):
    """
    A function returing the recommended ids, recommended item names, and bought item names of a customer
    given the customer ID exists based on the model type
    """
    if customer_id not in df_output.index:
        print('Customer not found.')
        return ['', '', '']
    list_return = []
    bought_df = pd.read_csv(os.getcwd() + "/data/bought.csv")
    if model_type == "model1":
        recommend_names_df = pd.read_csv(os.getcwd() + "/data/recommend_names.csv")
    elif model_type == "model2":
        recommend_names_df = pd.read_csv(os.getcwd() + "/data/recommend_names_full.csv")
    list_return.append(df_output.loc[customer_id].to_list()[0].replace('|', ', ')) # string of recommended ids
    list_return.append(recommend_names_df.loc[recommend_names_df.id == customer_id].name.to_list()[0]) # name of recommended ids
    list_return.append(bought_df.loc[bought_df.id == customer_id].bought.to_list()[0]) # name of item bought
    
    return list_return