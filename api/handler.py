import pickle
import pandas as pd
from flask import Flask, request, Response
from rossmann.Rossmann import Rossmann
import requests
import json

#carrega modelo
model = pickle.load(open('/Users/Rodrigo/Repos/Rossmann-store-sales-project/model/model_rossmann.pkl', 'rb'))

app = Flask( __name__ )

@app.route( '/rossmann/predict', methods=['POST'])
def rossmann_predict():
    test_json = request.get_json()
    
    if test_json: #tem dados
        if isinstance(test_json, dict): #unico exemplo
            test_raw = pd.DataFrame( test_json, index=[0])
            
        else: #varios exemplos
            test_raw = pd.DataFrame( test_json, columns=test_json[0].keys())
            
        #instanciar a classe rossmann
        pipeline = Rossmann()

        # limpeza dos datos
        df1 = pipeline.data_cleaning( test_raw )

        #feature engineering
        df2 = pipeline.feature_engineering( df1 )

        #preparação dos dados
        df3 = pipeline.data_preparation(df2)

        #prediction
        df_response = pipeline.get_prediction( model, test_raw, df3)
        
        return df_response
    
    else: #não tem dados
        return Response('{}', status=200, mimetype='application/json')


if __name__ == '__main__':
    app.run('0.0.0.0')