import streamlit as st
from password_check import check_password
from functions import read_inventory, search_inventory_by_site, \
    read_reports, search_report_by_site, read_evacuation_centers
import pandas as pd

st.set_page_config(
    page_title="Evacuaid",
    page_icon="📦",
    layout="wide",
)

if check_password():

    reports = read_reports()
    inventory = read_inventory()

    # Search functionality
    st.header('Search Report by Evacuation Site')

    # Dropdown
    evac_sites_list = read_evacuation_centers()
    evacuation_site = st.selectbox('Select Evacuation Site', evac_sites_list)

    # Text input for search bar
    search_name = st.text_input('Enter Evacuation Site name:', key='original_search').strip()

    # Use the chosen input method for searching
    if st.button('Search'):
        if evacuation_site:
            # Search based on the dropdown selection
            found_report = search_report_by_site(evacuation_site)
            found_inventory = search_inventory_by_site(evacuation_site)
            search_method = f"{evacuation_site}"
        elif search_name:
            # Search based on the text input
            found_report = search_report_by_site(search_name)
            found_inventory = search_inventory_by_site(search_name)
            search_method = f"{search_name}"
        else:
            st.warning("Please enter a site name or select an evacuation site.")


        st.write(f"### {search_method.title()}")
        if found_report:
            st.write(f'Total Reports Found: {len(found_report)}')
            for index, report in enumerate(found_report):
                with st.expander(f"Evacuation Site Report {index + 1}: {report.evacuation_site}"):
                    st.write(f"### Evacuation Site: {report.evacuation_site}")
                    st.write(f"Date: {report.date}")
                    st.write(f"Time: {report.time}")
                    st.write('### I. Situation Overview')
                    st.write(f"{report.situation}")
                    st.write('### II. Status of Affected Areas and Population')
                    st.write(f"{report.affected_pop}")
                    st.write('### III. Status of Displaced Population')
                    st.write(f"{report.displaced}")
                    st.write('### IV. Response Actions and Interventions')
                    st.write(f"{report.response}")
                    st.write(f"Prepared by: {report.preparer}")
                    st.write(f"Released by: {report.releaser}")
        else:
            st.warning(f"No available reports for '{search_method.title()}'.")

        if found_inventory:
            st.write(f'### {search_method.title()} Inventory')
            with st.expander(f"{search_method.title()} Inventory"):
                inventory_df = pd.DataFrame([
                    {'Item': item.item.title(), 'Quantity': item.quantity}
                    for item in found_inventory
                ])
                inventory_df["Inventory"] = inventory_df['Quantity']

                st.dataframe(inventory_df,
                             width=500,
                             height=420,
                             column_config={
                                 "Inventory": st.column_config.ProgressColumn(
                                     "Inventory",
                                     help="Volume in tons",
                                     min_value=0,
                                     max_value=100)},
                             hide_index=True,
                             use_container_width=True
                             )
        else:
            st.warning(f"No inventory for '{search_method.title()}'.")

