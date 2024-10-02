from datab_reports import Reports, Session, Inventory
import streamlit as st
import pandas as pd


def read_inventory():
    session = Session()
    all_inventory = session.query(Inventory).all()
    session.close()
    return all_inventory


def search_inventory_by_site(site):
    session = Session()
    check_site = site.title()
    relevant_inventory = session.query(Inventory).filter(Inventory.evacuation_site == check_site).all()
    session.close()
    return relevant_inventory


def read_reports():
    session = Session()
    all_reports = session.query(Reports).all()
    session.close()
    return all_reports


def search_report_by_site(site):
    session = Session()
    check_site = site.title()
    relevant_report = session.query(Reports).filter(Reports.evacuation_site == check_site).all()
    session.close()
    return relevant_report


def read_evacuation_centers():
    df = pd.read_csv('marikina_evacuation_centers.csv', usecols=['CENTER_M'])
    evac_sites_list = [''] + list(df["CENTER_M"])
    return evac_sites_list


def read_active_sites():
    session = Session()
    try:
        # Read names of active evacuation sites
        active_sites = session.query(Reports.evacuation_site).filter(
            Reports.activate == True).all()
        return list(set(site[0] for site in active_sites))
    finally:
        session.close()


def search_active_inventory(site):
    selected_site = site

    session = Session()
    try:
        # Search inventory for the specified site if it is activated
        inventory_items = session.query(Inventory).join(Reports).filter(
            Reports.evacuation_site == selected_site,
            Reports.activate == True
        ).all()

        return inventory_items
    finally:
        session.close()


# Functions for Chat
active_sites = read_active_sites()


def find_active_site_inventory():
    inventories = []
    for site in active_sites:
        active_inventory = search_active_inventory(site)
        if active_inventory:
            inventory_df = pd.DataFrame([
                {'Item': item.item.title(), 'Quantity': item.quantity}
                for item in active_inventory
            ])
            inventory_df["Inventory"] = inventory_df['Quantity']
            inventories.append((site, inventory_df))
        else:
            st.warning(f"No item found with name '{site.title()}'.")

    return inventories

# Read CSV
df = pd.read_csv('marikina_evacuation_centers.csv',
                  usecols=['CENTER_M', 'LAT', 'LONG', 'LOCATION',
                           'CONTACT_PERSON', 'CONTACT_NUMBER'])

