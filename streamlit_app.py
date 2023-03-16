import pandas as pd
import streamlit as st
from streamlit_vizzu import Config, Data, Style, VizzuChart

st.set_page_config(page_title="SF Airport Data Analysis Streamlit", page_icon=":rocket:", layout="wide")


# sysmenu = '''
# <style>
# #MainMenu {visibility:hidden;}
# footer {visibility:hidden;}
# '''
#st.markdown(sysmenu,unsafe_allow_html=True)

# Remove whitespace from the top of the page and sidebar
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


data_frame = pd.read_csv("https://data.sfgov.org/resource/rkru-6vcg.csv")
#print(data_frame.head())
data = Data()
data.add_data_frame(data_frame)

chart = VizzuChart(width='100%')
#orientation = st.session_state.get("orientation", "Horizontal")

chart.animate(data)
chart.feature("tooltip", True)

items: list[str] = st.multiselect(
    "geo_region",
    ['Australia / Oceania', 'Asia', 'Europe', 'Mexico', 'US','Central America', 'Canada', 'Middle East'],
    ['Australia / Oceania', 'Asia', 'Europe', 'Mexico', 'US','Central America', 'Canada', 'Middle East'],
)


col1, col2, col3, col4, col5 = st.columns(5)

measure: str = "passenger_count"
show_count: str = col1.radio("Passenger Count", ["Total Passenger Count", "By Region", "By Airlines", "By Region and Airlines"])  # type: ignore
compare_by = col2.radio("Compare by", ["Both", "Price Category", "Regional/International"])
coords = col3.radio("Coordinate system", ["Cartesian (desktop)", "Polar (mobile)"])
order = col4.radio("Order items", ["Alphabetically", "By value"])
bg_color = col5.color_picker("Background color", "#fff")

style = Style({"plot": {"backgroundColor": bg_color}})
angle = "0.0"
xAxisLabelColor = "#999999FF"
yAxisLabelColor = "#999999FF"
plotPaddingLeft = "7.5em"
plotPaddingBottom = ".6em"

filter = " || ".join([f"record['geo_region'] == '{item}'" for item in items])
#print(filter)
#title = f"{measure} of " + ", ".join(items)
title = f"Comparing flights"

def switch(x):
  show_count = {
    "Total Passenger Count": None,
    "By Region": "geo_region",
     "By Airlines": "operating_airline",
     "By Region and Airlines":["geo_region", "operating_airline"]
  }
  return show_count.get(x, "Incorrect")

show_count = switch(show_count)

if compare_by == "Both":
    #x = ["price_category_code"]
    print(show_count)
    x = show_count
    y = "passenger_count" 
    color = show_count
        
        
    if show_count == "operating_airline":
        angle = "-90"
        plotPaddingBottom = "5em"
    #elif show_count == ["geo_region", "operating_airline"]:
    #    color = show_count[0]
    
    

elif compare_by == "Regional/International":
    x = show_count.append("geo_summary")
    y = "passenger_count" 
    color = "geo_summary"
        
        
    if show_count == "operating_airline":
        angle = "-90"
        plotPaddingBottom = "5em"
    #elif show_count == ["geo_region", "operating_airline"]:
    #    color = show_count[0]

else:
    y = ["price_category_code"]
    x = [measure, "geo_summary"]
    color = ["geo_summary"]

if compare_by == "Both" and show_count == "operating_airline":
    label = None
    color = None
elif compare_by == "Both" and show_count == ["geo_region", "operating_airline"]:
    label = None
    color = show_count[0]
    angle = "-75"
    plotPaddingBottom = "5em"  
elif compare_by == "Regional/International" and show_count == ["geo_region", "operating_airline"]:
    label = None
    color = "geo_summary"
    angle = "-75"
    plotPaddingBottom = "5em" 
else:
    label = measure
    
config = {
    "title": title,
    "y": y,
    "label": label,
    "x": x,
    "color": color,
    "sort" : "none",
    "reverse" : True,
}

if coords == "Polar (mobile)":
    config["coordSystem"] = "polar"
else:
    config["coordSystem"] = "cartesian"

if order == "Alphabetically":
    config["sort"] = "none"
    config["reverse"] = True
else:
    config["sort"] = "byValue"
    config["reverse"] = True

#config["channels"] = {"label": {"set": None}}
    
style = Style({
    "plot": {
        "xAxis": {
            "label": {
                "angle": angle,
                "color": xAxisLabelColor,
                "fontSize": "0.9em",
                'numberFormat': 'prefixed',
                'numberScale': 'shortScaleSymbolUS'
            }
        },
        "yAxis": {
            "label": {
                "color": yAxisLabelColor,
                'numberFormat': 'prefixed',
                'numberScale': 'shortScaleSymbolUS'
            }
        },
        "marker": {
            "colorPalette": "#b74c20FF #c47f58FF #1c9761FF #ea4549FF #875792FF #3562b6FF #ee7c34FF #efae3aFF",
            'label': {
                'numberFormat': 'prefixed',
                'maxFractionDigits': '1',
                'numberScale': 'shortScaleSymbolUS'
            }
        },
        "paddingLeft": plotPaddingLeft,
        "paddingBottom": plotPaddingBottom
    },
    "legend": {
        "paddingRight": "-4em"
    },
    "logo": {
        "paddingBottom": "1.5em"
    }
})

chart.animate(Data.filter(), Config(config), style, delay=.1)
#chart.animate(Data.filter(filter), Config(config), style, delay=3)
output = chart.show()

#col6 , col7 = st.columns(2)
#orientation = col6.radio("Bar Orientation", ["Horizontal", "Vertical"], horizontal=True)

st.write("Try clicking on the graph to see the data!")

st.write(output)

