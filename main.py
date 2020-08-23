from datetime import datetime, timedelta
from typing import Dict
from requests import Response
from requests import get as get_request
from flask import Flask, render_template
import pandas as pd

import gcs

app = Flask(__name__)

BASE_URL: str = 'https://api.exchangeratesapi.io'
LATEST_ENDPOINT: str = '/latest'
HISTORY_ENDPOINT:str='history'
BUCKET_NAME:str = 'data_2020-08-23-11-41'

def get_data():
    execution_date = datetime.today().strftime('%Y-%m-%d')
    execution_date_minus_30 = (datetime.strptime(execution_date, '%Y-%m-%d') - timedelta(days=30)).strftime('%Y-%m-%d')
    dates = [(datetime.strptime(execution_date, '%Y-%m-%d') - timedelta(days=day)).strftime('%Y-%m-%d') for day in range(30)]
    response: Response = get_request(f'{BASE_URL}/{HISTORY_ENDPOINT}?start_at={execution_date_minus_30}&end_at={execution_date}')
    rates: Dict = response.json().get('rates')
    return rates

def get_df():
    rates: Dict = get_data()
    table: list = [[day, cur, rates[day][cur]] for day in rates for cur in rates[day]]
    df = pd.DataFrame(table, columns=['day','currency','value'])
    return df

@app.route('/')
def root():
    df = get_df()
    gcs.save_df(df, BUCKET_NAME)
    return render_template('index.html', tables=[df.to_html(classes='data')], titles=df.columns.values)


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
