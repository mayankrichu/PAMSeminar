import streamlit as st
import pandas as pd
from datetime import time

st.set_page_config(layout="wide", page_title="Co2 Emission")
# Set the title of the page

larger_text = "<span style='font-size: 24px;'>This is larger text.</span>"


st.write("<span style='font-size: 24px;'>Co2 Emission from different sectors  </span>", unsafe_allow_html=True)
def sector_change(percent_change, sector):
    germany_data = pd.read_excel('/Users/mayank/Documents/co2germany.xlsx', sheet_name='Sheet1')
    germany_data = germany_data[0:33]

    target_year = 2050
    current_year = 2022
    currrent_year_co2_emission = germany_data[germany_data['Year'] == 2022][f'{sector}'].values
    annual_reduction_rate = int(percent_change)
    total_number_years_needed = target_year - current_year
    year_df = []
    future_data = [currrent_year_co2_emission]
    for year in range(1, total_number_years_needed+1):
        currrent_year_co2_emission = currrent_year_co2_emission + (currrent_year_co2_emission * (annual_reduction_rate/100))
        year_df.append(current_year+year)
        future_data.append(int(currrent_year_co2_emission))
    future_data = pd.DataFrame({f'{sector}' : future_data[1:], 'Year':year_df}  )

    total_data = pd.concat([germany_data[['Year', f'{sector}']], future_data], ignore_index=True)
    return total_data

col1, col2, col3 = st.columns(3)




with col1:
    energy_percentage = st.slider('Energy industry co2 change', -50, 50, -5)
    transport_percentage = st.slider('Transport co2% change', -50, 50, -1)
    industry_percentage = st.slider('Industry co2% change', -50, 50, -2)
    buildings_percentage = st.slider('Buildings co2% change', -50, 50, -3)
    agriculture_percentage = st.slider('Agriculture co2% change', -50, 50, -4)
    ww_percentage = st.slider('Waste and Water co2% change', -50, 50, -1)
    forest_afforestation_percentage = st.slider('Forest area change', -50, 50, 1)

with col2:
    st.line_chart(data=sector_change(energy_percentage, "Energy Industry"), x = 'Year', y= 'Energy Industry')
    st.line_chart(data=sector_change(transport_percentage, "Transport"), x = 'Year', y= 'Transport')
    st.line_chart(data=sector_change(industry_percentage, "Industry"), x = 'Year', y= 'Industry')


with col3:
    st.line_chart(data=sector_change(agriculture_percentage, "Agriculture"), x='Year', y='Agriculture')
    st.line_chart(data=sector_change(ww_percentage, "Waste and Waste Water"), x='Year', y='Waste and Waste Water')
    st.line_chart(data=sector_change(buildings_percentage, "Buildings"), x='Year', y='Buildings')



energy_data = sector_change(energy_percentage, "Energy Industry")
transport_data = sector_change(transport_percentage, "Transport")
industry_data = sector_change(industry_percentage, "Industry")
buildings_data = sector_change(buildings_percentage, "Buildings")
agriculture_data = sector_change(buildings_percentage, "Agriculture")
ww_data = sector_change(ww_percentage, "Waste and Waste Water")

df_total_final = pd.concat([energy_data, transport_data, industry_data, buildings_data, agriculture_data, ww_data], axis=1)
df_total_final['GHG total'] = df_total_final['Waste and Waste Water'] + df_total_final['Agriculture']+df_total_final['Energy Industry'] + df_total_final['Transport'] + df_total_final['Buildings']
df_total_final = df_total_final.loc[:, ~df_total_final.columns.duplicated()]

### forest
forest_area = 11.4 #million hectares https://www.deutschland.de/en/topic/environment/how-large-are-germanys-forests-facts-and-figures#:~:text=How%20much%20forest%20is%20there,with%20over%2090%20billion%20trees.
per_hectare_carbon_absorbed = 12 #tonnes per year https://www.researchgate.net/publication/329074041_Global_carbon_dioxide_removal_rates_from_forest_landscape_restoration_activities
rate_afforestration = 0.31  # https://rainforests.mongabay.com/deforestation/forest-information-archive/Germany.htm#:~:text=31.7%25%20%E2%80%94or%20about%2011%2C076%2C000%20hectares,annual%20reforestation%20rate%20of%200.31%25.
forest_area_2050 = []

# from year 1990 - 2023
for i in range(2023, 1990, -1):
    forest_area -= forest_area * (forest_afforestation_percentage/100)
    forest_area_2050.append(forest_area)


#from year 2023 - 2050
for i in range(2022, 2050):
    forest_area += forest_area * (0.0031)
    forest_area_2050.append(forest_area)

total_carbon_absorbed = [x * per_hectare_carbon_absorbed for x in forest_area_2050]
total_carbon_absorbed = total_carbon_absorbed[::-1]

df_total_final['co2_absorption'] = total_carbon_absorbed

st.write("<span style='font-size: 20px;'>Total Co2 Emission from different sectors and Co2 Absorption</span>", unsafe_allow_html=True)

st.line_chart(df_total_final.set_index("Year")[["GHG total", "co2_absorption"]])