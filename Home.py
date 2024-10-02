import streamlit as st
import pandas as pd
from PIL import Image
import base64
from functions import read_inventory, read_evacuation_centers, \
    search_active_inventory, df


st.set_page_config(
    page_title="Evacuaid",
    page_icon="📦",
    layout="wide",
)


# Add CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def convert_image(filepath):
    with open(filepath, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode("utf-8")
        return image_base64


local_css("style.css")

# Banner Section

image = Image.open('images/evacuaid_banner.png')

st.image(image, width=900)

# Section with Buttons to other Pages

st.title('EvacuAid Hub')

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    image_map_path = "images/evac_btn.png"
    map_image_base64 = convert_image(image_map_path)

    html = f"<a href='#'><img src='data:image/png;base64," \
           f"{map_image_base64}' style='border-radius: 30px;'></a>"
    st.markdown(html, unsafe_allow_html=True)

    st.write("Want to donate or volunteer? Click here to see which sites need your help.")

with col2:
    image_chat_path = "images/chat_btn.png"
    chat_image_base64 = convert_image(image_chat_path)

    html = f"<a href='#'><img src='data:image/png;base64,{chat_image_base64}' style='border-radius: 30px;'></a>"
    st.markdown(html, unsafe_allow_html=True)

    st.write("Got questions? Give our Evacuaid assistant a try.")

with col3:
    image_login_path = "images/login_btn.png"
    login_image_base64 = convert_image(image_login_path)

    html = f"<a href='#'><img src='data:image/png;base64,{login_image_base64}'  style='border-radius: 30px;'></a>"
    st.markdown(html, unsafe_allow_html=True)

    st.write("Admin Login")


st.markdown("<br><br>", unsafe_allow_html=True)

# Section to search for active sites via dropdown

st.header('Search Evacuation Sites')

# For Dropdown

evac_sites_list = read_evacuation_centers()
evacuation_site = st.selectbox('Select Evacuation Site', evac_sites_list)

inventory = read_inventory()

active_inventory = search_active_inventory(evacuation_site)

site_row = df[df['CENTER_M'] == evacuation_site]

if not site_row.empty:
    location = site_row['LOCATION'].iloc[0]
    contact_person = site_row['CONTACT_PERSON'].iloc[0]
    contact_number = site_row['CONTACT_NUMBER'].iloc[0]

    if active_inventory:
        st.write(f"## {evacuation_site.title()} needs aid")

        with st.expander(f"{evacuation_site.title()} Inventory"):
            inventory_df = pd.DataFrame([
                {'Item': item.item.title(), 'Quantity': item.quantity}
                for item in active_inventory
            ])
            inventory_df["Inventory"] = inventory_df['Quantity']

            # Add Contacts
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
        st.info(f"{evacuation_site} is well-supported right now. "
                f"Consider redirecting aid to a location that could "
                f"benefit more from your generous donations. "
                f"Thank you for your support!")
