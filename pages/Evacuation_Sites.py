import streamlit as st
import pandas as pd
import pydeck as pdk
from pretty_notification_box import notification_box
from functions import search_active_inventory, \
    active_sites, df

# Top Section
st.set_page_config(
    page_title="Evacuaid",
    page_icon="📦",
    layout="wide",
)


st.title('EvacuAid Hub')

st.header('Cites Needing Aid')

lat = list(df["LAT"])
long = list(df["LONG"])
evacuation_site = list(df["CENTER_M"])

# Create colors for map

colors = []

for site in evacuation_site:
    if site in active_sites:
        colors.append((200, 30, 0, 160))  # Red for active sites
    else:
        colors.append((0, 0, 255, 160))  # Blue for non-active sites

# Add the 'is_active' column to the DataFrame
df['is_active'] = colors


# Map Section: Pydeck map

st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=14.467354,
        longitude=78.824133,
        zoom=13,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=df,
            get_position='[LONG, LAT]',
            get_color='is_active',
            # get_color='[200, 30, 0, 160]',
            get_radius=100,
            pickable=True,
            auto_highlight=True,
        ),
    ], tooltip={
        "text": "{CENTER_M}",
        "style": {
            "backgroundColor": "steelblue",
            "color": "white"
        },
    }
))


st.info("Red markers indicate sites in need of aid, while blue markers represent fully stocked sites.", icon="ℹ️")


# Inventory Section

st.write("## Sites needing aid")
for site in active_sites:
    active_inventory = search_active_inventory(site)

    # Find the corresponding row in the dataframe for the current active site
    site_row = df[df['CENTER_M'] == site]  #ADDED

    location = site_row['LOCATION'].iloc[0]
    contact_person = site_row['CONTACT_PERSON'].iloc[0]
    contact_number = site_row['CONTACT_NUMBER'].iloc[0]


    if active_inventory:
        with st.expander(f"{site.title()} Inventory"):
            inventory_df = pd.DataFrame([
                {'Item': item.item.title(), 'Quantity': item.quantity}
                for item in active_inventory
            ])
            inventory_df["Inventory"] = inventory_df['Quantity']

            #ADD CONTACTS
            st.write(f"**Address:** {location}")
            st.write(f"**Contact Person:** {contact_person}")
            st.write(f"**Contact Number:** {contact_number}")


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
        st.warning(f"No item found with name '{site.title()}'.")

# Notification box Section

styles = {'material-icons':{'color': 'red'},
          'title': {'font-weight':'bold'},
          'notification-content-container': {'':''},
          'title-text-url-container': {'',''},
          'notification-text-link-close-container': {'',''},
          'external-link': {'',''},
          'close-button': {'',''}}


st.markdown("<br><br><br><br>", unsafe_allow_html=True)

notice = "Please note that all data and information " \
         "presented herein are solely for demonstration purposes. " \
         "The contact numbers and individuals depicted are entirely fictional " \
         "and not representative of real entities. This submission serves as a " \
         "demonstration for the MLH Hackathon."

notification_box(icon='warning', title='Note', textDisplay=f'{notice}',
                 externalLink='', url='', styles=None, key='foo')

