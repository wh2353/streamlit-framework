import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import seaborn as sns


import requests
import os
from dotenv import load_dotenv

from bokeh.plotting import figure, output_file, show

from bokeh.palettes import Spectral4

from bokeh.models import Legend

import streamlit.components.v1 as components



st.title("Stock Price in the past 6 months")
with st.form("my_form"):
	ticker = st.text_input("Ticker symbol", placeholder='IBM')
	cp = st.checkbox('Closing price')
	acp = st.checkbox('Adjusted closing price')
	op = st.checkbox('Opening price')
	aop = st.checkbox('Adjusted opening price')
	submitted = st.form_submit_button("Submit")
	


print(f"ticker={ticker}, cp={cp}, op={op}, aop={aop}, submitted={submitted}")




	







if submitted:

	# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
	load_dotenv()
	API_KEY = os.getenv('API_key')
	

	if len(ticker) == 0:
		ticker = 'IBM'


	#get the from and to date
	from_date = date.today() + relativedelta(months=-6)

	to_date = date.today()

	url=f"https://api.tiingo.com/tiingo/daily/{ticker}/prices?startDate={from_date}&endDate={to_date}&token={API_KEY}"

	r = requests.get(url)
	data = r.json()



	



	final_data = pd.DataFrame.from_records(data, index=range(len(data)))

	#convert datetime str to YYYY-mm-dd format

	st.write(final_data.head())

	final_data['date'] = [datetime.fromisoformat(time[:-1]).strftime('%Y-%m-%d') for time in final_data.date.tolist()]

	#get the dataset on open, close price and adjusted open and close price
	plot_data = final_data[['close', 'adjClose', 'open', 'adjOpen']]

	#get selected columns only
	plot_data = plot_data.loc[:,[cp, acp, op, aop]]

	plot_data['date'] = pd.to_datetime(final_data['date'])

	


	all_var = list(plot_data.columns[:-1])

	numlines=len(all_var)
	mypalette=Spectral4[0:numlines]





	p = figure(width=800, height=450, x_axis_type="datetime")
	p.title.text = f'{ticker} in the past 6 months'
	p.title.align = "center"
	p.title.text_font_size = "25px"
	p.xaxis[0].axis_label = 'Date'
	p.yaxis[0].axis_label = 'Price'
	

	for name, color in zip(all_var, Spectral4):


		p.line(plot_data['date'], plot_data[name], line_width=2, color=color, alpha=0.8, legend_label=name)


	p.add_layout(Legend(), 'right')

	output_file("interactive_legend.html", title="interactive_legend.py example")

	show(p)

	st.bokeh_chart(p, use_container_width=True)

	

	
