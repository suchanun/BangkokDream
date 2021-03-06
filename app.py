import streamlit as st
import pandas as pd
import json
import plotly.graph_objects as go
import config
import numpy as np

def main():


    data = load_data()
    config.bkk_coordinates = data['bkk_coordinates']  # boundaries of bangkok
    config.df_district_loc = data['df_district_loc']  # one point location of each district # modified

    config.df_budget = data['df_budget'] # mine
    config.df_subbudget = data['df_subbudget']  # mine
    config.df_budget_district = data['df_budget_district']#config.df_budget[pd.notnull(config.df_budget.lat)]
    config.df_item = data['df_item']
    st.title('ตรวจสอบงบประมาณสำนักงานเขต')
    districts = sorted([district for district in config.df_budget.budget.unique() if district.startswith('สำนักงานเขต')])
    district = st.selectbox('สำนักงานเขต', ['เลือกเขต']+districts, format_func=lambda dep: dep[11:] if dep != 'เลือกเขต' else dep)


    # plot main map
    bangkok_fig = get_fig_bangkok(district)
    st.plotly_chart(bangkok_fig)

    # choose subbudget of district

    # plot pie district
    if district != 'เลือกเขต':

        df_subbudget = config.df_subbudget  # [config.df_subbudget[]]
        print('district == ')
        print(district)
        df_subbudget = df_subbudget[df_subbudget.budget == district]
        print(df_subbudget.shape)


        # st.selectbox('แผนงาน', )

        st.header('งบ{}'.format(district))#องแผนงานต่างๆ
        subbudgets = df_subbudget.sub_budget
        subbudget = st.selectbox('ดูรายละเอียดแผนงาน', list(subbudgets))

        district_pie = get_pie_district(df_subbudget, subbudget)
        st.plotly_chart(district_pie)

        st.subheader('งบโครงการต่างๆใน{}'.format(subbudget))
        fig_items = get_bar_items(district, subbudget)
        fig_items.update_layout(
            xaxis=dict(
                # tickangle=90,
                title_text="จำนวนเงิน (บาท)",
                # title_font={"size": 20},
                # title_standoff=25
                )
            # yaxis=dict(
            #     title_text="Temperature",
            #     title_standoff=25)
            )
        st.plotly_chart(fig_items)



def get_bar_items(district, subbudget):
    fig = go.Figure()
    df_item = config.df_item
    df_item = df_item[(df_item.budget==district)&(df_item.sub_budget == subbudget) ]

    fig.add_trace(go.Bar(
        y=df_item.sub_items,
        x=df_item.amount,
        name='งบจัดสรรทั้งหมด',
        orientation='h',
        text=[f"฿{value:,.0f}" for value in df_item.amount],
        textposition='auto',
        width=0.30,
        marker=dict(
            #         color='rgba(246, 78, 139, 0.6)',
            color='rgba(92, 200, 154, 255)',
            line=dict(color='rgba(92, 200, 154, 255)', width=0.8)
            #         line=dict(color='rgba(246, 78, 139, 1.0)', width=3)
        )
    ))
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def get_pie_district(df_subbudget_of_district,subbudget=None):
   # df_subbudget = config.df_subbudget #[config.df_subbudget[]]
    df_subbudget = df_subbudget_of_district#df_subbudget[df_subbudget.budget==district]

    subbudgets = list(df_subbudget.sub_budget)
    labels = subbudgets
    values = df_subbudget.amount#[4500, 2500, 1053, 500]
    n_subbudget = len(values)
    pull=None

    if subbudget:
        target_idx = [i for i in range(n_subbudget) if subbudgets[i] == subbudget][0]
        pull = np.zeros(n_subbudget)
        pull[target_idx] = 0.2


    # pull is given as a fraction of the pie radius
    fig = go.Figure(data=[go.Pie(
                labels=labels, values=values,textinfo='label+percent',
                pull=pull,
                #insidetextorientation='radial'?????
    )])#, pull=[0, 0, 0.2, 0]


    fig.update_layout(showlegend=False)
    return fig

def get_fig_bangkok(district):
    if district == 'เลือกเขต':
        df_budget_district = config.df_budget_district
    else:
        df_budget_district = config.df_budget_district
        df_budget_district = df_budget_district[df_budget_district.budget==district]
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
        lon = df_budget_district['lon'],
        lat = df_budget_district['lat'],#%{y:$.2f}f"{value:,.0f}
        hovertemplate = [budget+"<br>"+"฿"+f"{value:,.0f}<extra></extra>" for budget,value in zip(config.df_budget_district['budget'],config.df_budget_district['amount'])],
        showlegend = False,

        marker = dict(
            size = 15,#df_sub['pop']/scale,
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
    data['df_item'] = pd.read_pickle('./data-nice/sub_entry.pkl')
    return data

if __name__ == "__main__":
    main()