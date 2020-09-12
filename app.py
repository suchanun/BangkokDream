import streamlit as st
import pandas as pd
import json
import plotly.graph_objects as go
import config

def main():
    st.sidebar.selectbox('mode',['hi','hello'])
    data = load_data()
    config.bkk_coordinates = data['bkk_coordinates']  # boundaries of bangkok
    config.df_district_loc = data['df_district_loc']  # one point location of each district # modified

    config.df_budget = data['df_budget'] # mine
    config.df_subbudget = data['df_subbudget']  # mine
    config.df_budget_district = data['df_budget_district']#config.df_budget[pd.notnull(config.df_budget.lat)]

    bangkok_fig = get_fig_bangkok()
    st.plotly_chart(bangkok_fig)


def get_fig_bangkok():
    data = list()
    data.append(go.Scattermapbox(
                showlegend = False,
                lon = [cor[0] for cor in config.bkk_coordinates],
                lat = [cor[1] for cor in config.bkk_coordinates],
                mode="lines",
                line=dict(width=3.5, color='rgba(209, 144, 21,0.9)'),#"#47544f"),
                hoverinfo='none',
                fill='toself',
                fillcolor='rgba(255, 211, 128,0.2)'
            ))


    data.append(go.Scattermapbox(
        lon = config.df_budget_district['lon'],
        lat = config.df_budget_district['lat'],#%{y:$.2f}f"{value:,.0f}
        hovertemplate = [budget+"<br>"+"฿"+f"{value:,.0f}<extra></extra>" for budget,value in zip(config.df_budget_district['budget'],config.df_budget_district['amount'])],
        showlegend = False,

        marker = dict(
            size = 20,#df_sub['pop']/scale,
            color = config.df_budget_district['amount'],
            showscale=True,
            colorscale='Oranges',
        ),

    )
                 )

    fig = go.Figure(data=data)
    fig.update_layout(
        showlegend=False,
        margin={"r":0,"t":0,"l":0,"b":0},
        mapbox=go.layout.Mapbox(
            style='stamen-terrain',#'open-street-map',#'stamen-watercolor',#'carto-positron',#'open-street-map',#"stamen-terrain",
            zoom=10,
            center_lat = 13.726316,
            center_lon =100.591507,
        )
    )
    return fig

@st.cache(allow_output_mutation=True)
def load_data():
    data = dict()
    with open('./data-nice/bangkok_coordinates.json') as json_file:
        data['bkk_coordinates'] = json.load(json_file)  # boundaries of bangkok
    data['df_district_loc'] = pd.read_csv('./data-nice/bkk_district_map.csv', index_col=0)  # one point location of each district # modified

    data['df_budget'] = pd.read_pickle('./data-nice/df_budget.pkl')  # mine
    data['df_subbudget'] = pd.read_pickle('./data-nice/sub_budget.pkl')  # mine
    data['df_budget_district'] = data['df_budget'][pd.notnull(data['df_budget'].lat)]
    return data

if __name__ == "__main__":
    main()