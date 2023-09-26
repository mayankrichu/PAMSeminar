
import streamlit as st
import pandas as pd



st.set_page_config(layout="wide", page_title="Co2 Emission")
# Set the title of the page

st.write("<span style='font-size: 24px;'>Co2 Emission from different sectors  </span>", unsafe_allow_html=True)

def sector_change(percent_change, sector):
    germany_data = pd.read_excel('/Volumes/Mayank HDD/PAM/PAM/co2germany.xlsx', sheet_name='Sheet1')
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

col1, col2 = st.columns(2)






with col1:
    energy_percentage = st.slider('Energy industry co2 change', -10, 10, -5)
    transport_percentage = st.slider('Transport co2% change', -10, 10, -1)
    industry_percentage = st.slider('Industry co2% change', -10, 10, -2)
    buildings_percentage = st.slider('Buildings co2% change', -10, 10, -3)
    agriculture_percentage = st.slider('Agriculture co2% change', -10, 10, -4)
    ww_percentage = st.slider('Waste and Water co2% change', -10, 10, -1)
    forest_afforestation_percentage = st.slider('Forest area change', -10, 10, 1)


energy_data = sector_change(energy_percentage, "Energy Industry")
transport_data = sector_change(transport_percentage, "Transport")
industry_data = sector_change(industry_percentage, "Industry")
buildings_data = sector_change(buildings_percentage, "Buildings")
agriculture_data = sector_change(agriculture_percentage, "Agriculture")
ww_data = sector_change(ww_percentage, "Waste and Waste Water")

df_total_final = pd.concat([energy_data, transport_data, industry_data, buildings_data, agriculture_data, ww_data], axis=1)
df_total_final['GHG total'] = df_total_final['Waste and Waste Water'] + df_total_final['Agriculture']+df_total_final['Energy Industry'] + df_total_final['Transport'] + df_total_final['Buildings'] + df_total_final['Industry']
df_total_final = df_total_final.loc[:, ~df_total_final.columns.duplicated()]


### forest
forest_area = 11.4 #million hectares https://www.deutschland.de/en/topic/environment/how-large-are-germanys-forests-facts-and-figures#:~:text=How%20much%20forest%20is%20there,with%20over%2090%20billion%20trees.
per_hectare_carbon_absorbed = 12 #tonnes per year https://www.researchgate.net/publication/329074041_Global_carbon_dioxide_removal_rates_from_forest_landscape_restoration_activities
rate_afforestration = 0.31  # https://rainforests.mongabay.com/deforestation/forest-information-archive/Germany.htm#:~:text=31.7%25%20%E2%80%94or%20about%2011%2C076%2C000%20hectares,annual%20reforestation%20rate%20of%200.31%25.
forest_area_2050 = []

# from year 1990 - 2023
for i in range(2022, 1990, -1):
    forest_area -= forest_area * (0.31/100)
    forest_area_2050.append(forest_area)


#from year 2023 - 2050
for i in range(2022, 2051):
    forest_area += forest_area * (forest_afforestation_percentage/100)
    forest_area_2050.append(forest_area)

total_carbon_absorbed = [(x * per_hectare_carbon_absorbed) for x in forest_area_2050]


df_total_final['co2_absorption'] = total_carbon_absorbed

df_pivot = df_total_final.iloc[[32,60]]
with col2:
    st.write("<span style='font-size: 20px;'>X-axis represents Year and Y-axis represents Co2 Emission per year</span>", unsafe_allow_html=True)

    st.line_chart(df_total_final[0:30].set_index("Year")[
                      ["GHG total", "Energy Industry", "Transport", "Industry", "Waste and Waste Water",
                       "Buildings", "Agriculture"]], use_container_width=True)
    st.line_chart(df_total_final.set_index("Year")[["GHG total", "Energy Industry","Transport", "Industry","Waste and Waste Water",
                                                    "Buildings", "Agriculture"]])
    st.write("<span style='font-size: 20px;'>Total Co2 Emission from different sectors and Co2 Absorption</span>", unsafe_allow_html=True)

    st.line_chart(df_total_final.set_index("Year")[["GHG total", "co2_absorption"]])

    st.write((df_total_final['GHG total'] - df_total_final['co2_absorption']).iloc[-1])

    st.write(df_pivot)
