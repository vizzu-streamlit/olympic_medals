import pandas as pd
import streamlit as st
import numpy as np
from typing import List

from streamlit_vizzu import Config, Data, Style, VizzuChart

st.set_page_config(layout="wide")

st.title("I'll be around if you have questions or you can visit [ipyvizzu.com](https://ipyvizzu.com) for more info")
st.title("Check out this app at [olympic-medals.streamlit.app](https://olympic-medals.streamlit.app)")

data_frame = pd.read_csv("data/Data Olympics.csv", dtype={"game_year": str})
data = Data()
data.add_df(data_frame)

chart = VizzuChart(use_container_width=True)

chart.animate(data)
chart.feature("tooltip", True)

# Set the style of the Vizzu chart in the app

style = Style(
    {
#        'legend' : {'label' : { 'fontSize' : '1.6em'}, 'width': '12em'},
        'plot': {
            'marker' :{ 'colorPalette' : '#3364B3 #DDDB2F #CC0000 #445C97 #517DFF #FF0000 #8F8745 #D46C29 #5D8866 #D0A3A3 #A2A2B2'},
            'yAxis': {
                'label': {
                    'fontSize': '1em',
                },
                'title': {'color': '#ffffff00'},
            },
        },
    }
)

#set timeframe
year1, year2 = st.select_slider(
	"Time range", options=map(str, np.arange(1896, 2021)), value=("1946", "2010")
)
filter_year = f"record['game_year'] >= {year1} && record['game_year'] <= {year2}"

col1, col2, col3 = st.columns(3)

compare_by = col1.radio("Aggregate", ["by Country", "by Year", "by Discipline"])
event = col2.radio("Event type", ["Both", "Summer", "Winter"])

if event != "Both":
	filter_event = f"record.game_season == '{event}'"
else:
	filter_event = None

medals = col3.radio("Medals", ["ALL", "GOLD", "SILVER", "BRONZE"])

if medals != "ALL":
	filter_medals = f"record.medal_type == '{medals}'"
else:
	filter_medals = None



top = st.empty()
bottom = st.empty()
with bottom.container():

	#select countries
	top10countries = ['USA', 'Germany', 'Soviet Union', 'Great Britain', 'France', 'China', 'Italy', 'Australia', 'Hungary', 'Japan']

	selected_countries: List[str] = st.multiselect('Countries',options=data_frame.sort_values(by="country_name").country_name.unique(),default=top10countries)

	filter_countries = (
		"(" + " || ".join([f"record['country_name'] == '{item}'" for item in selected_countries]) + ")"
	)

	# -- concat filters --
	filters_used = [f for f in [filter_countries, filter_year, filter_event, filter_medals] if f is not None]
	filter = " && ".join(filters_used)

	if compare_by == "by Country":
		y = ["country_name"]
		x = ["Count"]
		color = ["country_name"]
		sort = "byValue"

	elif compare_by == "by Year":
		y = ["Count"]
		x = ["game_year"]
		color = None
		sort = "none"

	else:
		y = ["discipline_title"]
		x = ["Count"]
		color = ["discipline_title"]
		sort = "byValue"


config = {
   # "title": title,
    "y": y,
    "label": "Count",
    "x": x,
    "color": color,
	"sort": sort,
}

chart.animate(Data.filter(filter), Config(config), style, delay=0)
with top.container():
	output = chart.show()

st.write("Click on the chart to check the underlying data")

st.write(output)
