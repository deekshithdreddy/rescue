import streamlit as st
import pandas as pd
from datab_reports import Reports, Inventory, Session
from password_check import check_password
from functions import df


st.set_page_config(
    page_title="Evacuaid",
    page_icon="📦",
    layout="wide",
)


if check_password():
    st.header('Situation Report')

    @st.cache_data()
    def add_report(evac_site, date, time, situation, population,
                   displaced, response, preparer, releaser, activate, inventory_data):

        session = Session()

        date_str = str(date)
        time_str = str(time)

        new_report = Reports(evacuation_site=evac_site, date=date_str,
                             time=time_str, situation=situation,
                             affected_pop=population, displaced=displaced,
                             response=response, preparer=preparer,
                             releaser=releaser, activate=activate)

        # Link the new Reports entry to Inventory entries
        for index, item_data in inventory_data.iterrows():
            item = Inventory(
                item=item_data['Item'],
                quantity=item_data['Quantity'],
                is_available=item_data['is_available'] if 'is_available' in item_data else False
            )
            new_report.inventory.append(item)

        session.add(new_report)
        session.commit()
        session.close()

    evac_sites_list = [''] + list(df["CENTER_M"])
    evacuation_site = st.selectbox('##### Select Evacuation Site', evac_sites_list)

    date = st.date_input("##### Add date", value=None)

    time = st.time_input('##### Add time', value=None)

    situation = st.text_area('##### Give an overview of the situation')

    affected_population = st.text_area('##### Describe the status of affected areas and population')

    displaced = st.text_area('##### Describe the status of displaced population')

    response = st.text_area('##### Describe response actions and interventions, i.e.'
                             ' standby funds, food and nonfood items, other activities')

    preparer = st.text_input('##### Prepared by')

    releaser = st.text_input('##### Released by')

    # Add Table

    # Initialize empty DataFrame for the Inventory data
    item_enum_values = [getattr(Inventory.ItemEnum, attr) for attr in dir(Inventory.ItemEnum) if not callable(getattr(Inventory.ItemEnum, attr)) and not attr.startswith("__")]

    inventory_data = pd.DataFrame(columns=["Item", "Quantity"])
    inventory_data["Item"] = item_enum_values
    inventory_data["Item"] = inventory_data["Item"].apply(lambda x: x.title())
    inventory_data["Quantity"] = 0

    # Display Inventory table using st.data_editor
    edited_inventory_df = st.data_editor(
        inventory_data,
        column_config={"Item": st.column_config.TextColumn("Item", help="Item"),
                       "Quantity": st.column_config.NumberColumn("Quantity",
                                                                 help="in tons",
                                                                 min_value=0,
                                                                 max_value=100)},
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True)


    activate_aid = st.toggle('Activate Aid Request')


    if st.button("Save report"):
        # Retrieve user-modified Inventory data
        edited_inventory_data = edited_inventory_df.copy()

        add_report(evacuation_site, date, time, situation, affected_population,
                   displaced, response, preparer, releaser, activate_aid, edited_inventory_data)

        # Convert the edited_df to SQLite and save it
        conn = st.connection("local_db", type="sql", url="sqlite:///reports.db")

        Session().commit()

        # Close the session
        Session().close()


        st.success("Report added successfully!")