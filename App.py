from xml.dom.domreg import registered
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Unicorn Companies Dashboard",
                   page_icon=":chart_with_upwards_trend:",
                   layout="wide")

@st.cache
def get_data_from_excel():
    df = pd.read_excel('UnicornCompanies.xlsx')
    return df

df = get_data_from_excel()

df = df.dropna(subset=['Founding_Year'])
df['Founding_Year'] = df['Founding_Year'].astype(int)
df['Unicorn_Entry_Year'] = df['Unicorn_Entry_Year'].astype(int) 
df['Acquisitions'] = df['Acquisitions'].astype(int)

df.rename(columns={'Profit in 2021':'Profit_in_2021_(In_Millions_$)',
                    'Current Valuation':'Current_Valuation_(In_Billions_$)'}, inplace=True)


df['Profit_in_2021_(In_Millions_$)'] = df['Profit_in_2021_(In_Millions_$)'].str.replace(' Million','')
df['Current_Valuation_(In_Billions_$)'] = df['Current_Valuation_(In_Billions_$)'].str.replace(' Billion','')
df['Current_Valuation_(In_Billions_$)'] = df['Current_Valuation_(In_Billions_$)'].str.replace(' BIllion','')

df['Profit_in_2021_(In_Millions_$)'] = df['Profit_in_2021_(In_Millions_$)'].str.replace('$','')
df['Current_Valuation_(In_Billions_$)'] = df['Current_Valuation_(In_Billions_$)'].str.replace('$','')

df['Profit_in_2021_(In_Millions_$)'] = df['Profit_in_2021_(In_Millions_$)'].astype('float')
df['Current_Valuation_(In_Billions_$)'] = df['Current_Valuation_(In_Billions_$)'].astype('float')


# ----------------------------------------------------------------------------- SIDE BAR ------------------------------------------------------------------------------

st.sidebar.header("Dashboard Filters")
# year = st.sidebar.multiselect(
#     "Select the Founding Year:",
#     options=df['Founding_Year'].unique(),
#     # default=df['Founding_Year'].unique()
# )

# entry_year = st.sidebar.multiselect(
#     "Select the Unicorn Entry Year:",
#     options=df['Unicorn_Entry_Year'].unique(),
#     # default=df['Unicorn_Entry_Year'].unique()
# )

industry = st.sidebar.multiselect(
    "Select the Industry:",
    options=df['Industry_Aggregated'].unique(),
    default=df['Industry_Aggregated'].unique()
)

ipo_status = st.sidebar.multiselect(
    "Select the IPO Status:",
    options=df['IPO_Status'].unique(),
    default=df['IPO_Status'].unique()
)


df_selection = df.query(
    "Industry_Aggregated == @industry & IPO_Status == @ipo_status"
)

# ----------------------------------------------------------------------------- HOME PAGE ------------------------------------------------------------------------------

st.title(":chart_with_upwards_trend: Unicorn Companies Dashboard")
st.markdown("##")

# Total Unicorn Companies in 2021
total_companies = df_selection['Startup_Name'].nunique()
unlisted = df[df['IPO_Status']=='Unlisted']['Startup_Name'].nunique()
listed = df[df['IPO_Status']=='Listed']['Startup_Name'].nunique()
registered = df[df['IPO_Status']=='Registered']['Startup_Name'].nunique()


st.subheader("Unicorn Companies:")
st.subheader(f"{total_companies}")

st.markdown("------")

# left, middle, right = st.columns(3)
# with left:
#     st.subheader("Registered Unicorn Companies:")
#     st.subheader(f"{registered}")

# with middle:
#     st.subheader("Unlisted Unicorn Companies:")
#     st.subheader(f"{unlisted}")

# with right:
#     st.subheader("Listed Unicorn Companies:")
#     st.subheader(f"{listed}")

# st.markdown("------")


# ----------------------------------------------------------------------------- BAR CHART ------------------------------------------------------------------------------

valuation_by_industry = (
    df_selection.groupby(['Industry_Aggregated']).agg({'Current_Valuation_(In_Billions_$)':'sum'}).sort_values(by='Current_Valuation_(In_Billions_$)')
)

fig_valuation = px.bar(
    valuation_by_industry,
    x = 'Current_Valuation_(In_Billions_$)',
    y = valuation_by_industry.index,
    orientation="h",
    title="<b>Valuation by Industry</b>",
    color_discrete_sequence=["#0083B8"] * len(valuation_by_industry),
    template="plotly_white",
)

fig_valuation.update_layout(
    plot_bgcolor = "rgba(0,0,0,0)",
    xaxis = (dict(showgrid=False))
)

profit_by_industry = (
    df_selection.groupby('Industry_Aggregated').agg({'Profit_in_2021_(In_Millions_$)':'sum'}).sort_values(by='Profit_in_2021_(In_Millions_$)')
)

fig_profit = px.bar(
    profit_by_industry,
    x = 'Profit_in_2021_(In_Millions_$)',
    y = profit_by_industry.index,
    orientation="h",
    title="<b>Profit by Industry</b>",
    color_discrete_sequence=["#0083B8"] * len(profit_by_industry),
    template="plotly_white",
)

fig_profit.update_layout(
    plot_bgcolor = "rgba(0,0,0,0)",
    xaxis = (dict(showgrid=False))
)

left_col, right_col = st.columns(2)


left_col.plotly_chart(fig_valuation, use_container_width=True)
right_col.plotly_chart(fig_profit, use_container_width=True)


# ------------------------------------------------------------------------- HIDE STREAMLIT STYLE -----------------------------------------------------------------------

hide_st_style = """
    <style>
    #MainMenu {visibility: hiden;}
    footer {visibility: hidden}
    header {visibility: hidden}
    </style>
"""

st.markdown(hide_st_style, unsafe_allow_html=True)