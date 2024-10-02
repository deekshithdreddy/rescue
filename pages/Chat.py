import streamlit as st
import pandas as pd
from functions import find_active_site_inventory, active_sites, df

st.set_page_config(
    page_title="Evacuaid",
    page_icon="📦",
    layout="wide",
)


contact = 'Find a contact for an Evacuation Site'
evacuation_site = 'Find an Evacuation Site in need of aid'
inventory = 'Find the inventory of an active site'


st.title("EvacuAid Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

with st.chat_message("assistant"):
    st.write("Hello!")
    option = st.selectbox(
        'Which of the following can I help you with today?',
        ('',
         contact,
         evacuation_site,
         inventory,))


# React to user input
if prompt := option:
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)

    response = "Please choose an option from the dropdown."

    if option == contact:
        evacuation_site = st.selectbox('Select Evacuation Site',
                                       options=[''] + list(df['CENTER_M']))

        if evacuation_site:
            site_row = df[df['CENTER_M'] == evacuation_site]

            if not site_row.empty:
                contact_person = site_row['CONTACT_PERSON'].iloc[0]
                contact_number = site_row['CONTACT_NUMBER'].iloc[0]

                response = f"Here are the contacts for {evacuation_site}"
                with st.expander(f"{evacuation_site.title()} Contacts"):
                    st.write(f"**Contact Person:** {contact_person}")
                    st.write(f"**Contact Number:** {contact_number}")
            else:
                response = f"No contact information found for {evacuation_site}"

    elif option == evacuation_site:
        response = "The sites currently looking for aid are:\n" +\
                   "\n".join([f"- {site}" for site in active_sites])

    elif option == inventory:
        inventories = find_active_site_inventory()
        response = "These are the current inventories of active sites 🔼"

        for site, inventory_df in inventories:
            with st.expander(f"{site.title()} Inventory"):
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
                             use_container_width=True)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)