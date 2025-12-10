import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

df = pd.read_csv("smartphones.csv")

st.sidebar.header("Smarphones Insights", divider='grey')
options = st.sidebar.selectbox("Options", ['Overview', 'Brand Explorer', 'Feature Explorer', 'Compare Phones', 'EDA / Raw Data'])


if options == 'Overview':

    st.markdown("## 📊 Smartphone Market Overview")

    st.divider()
    
    st.markdown("""
    This smartphone dashboard presents a comprehensive analysis of **981 smartphones** from leading brands like **Samsung, Xiaomi, Apple, OnePlus, Realme, POCO, iQOO**, and more.

    We analyze phones across multiple dimensions, including:

    -  **Price distribution** across segments — from ultra-budget to flagship
    -  **Customer ratings** — which specs correlate with user satisfaction
    -  **Brand strategies** — which brands dominate which price tiers
    -  **Feature coverage** — RAM, storage, battery, display, and camera insights
    -  **Connectivity adoption** — how widespread are 5G, NFC, IR blaster, and SD cards

    Use the **sidebar filters** to slice the dataset by brand, price range, RAM capacity, and more. 

    ---

    ###  How to Use This Dashboard

    - Use the **filters on the left** to narrow down by brand or specs
    - Scroll through the **charts below** to see how pricing, ratings, and features vary
    - Navigate to **other sections** for deeper insights:
    -  *Brand Explorer* — Analyze individual brand strategies
    -  *Feature Explorer* — Understand how specs affect price and ratings
    -  *Compare Phones* — View two models side-by-side

    ---

    This dashboard is built using **Python + Streamlit**, with static visualizations from **Seaborn and Matplotlib** 

    Enjoy exploring!    
    """)


if options == 'Brand Explorer':
    if 'brand_name' in df.columns:
        brands = sorted(df['brand_name'].unique().tolist())
        selected_brand = st.sidebar.selectbox("Select Brand", brands)

        # price range
        price_min, price_max = int(df['price'].min()), int(df['price'].max())
        price_range = st.sidebar.slider("Select Price Range", price_min, price_max, (0, price_max), step=10000)

        #ram range
        ram_min, ram_max = int(df['ram_capacity'].min()), int(df['ram_capacity'].max())
        ram_range = st.sidebar.slider("RAM (GB)", ram_min, ram_max, (ram_min, ram_max),step=1)

        # storage range (discrete steps)
        storage_values = [4, 8, 16, 32, 64, 128, 256, 512]
        storage_range = st.sidebar.select_slider("Storage (GB)", options=storage_values, value=(storage_values[0], storage_values[-1]))

        filtered_df = df[
        (df['price'] >= price_range[0]) & 
        (df['price'] <= price_range[1]) &
        (df['ram_capacity'] >= ram_range[0]) &
        (df['ram_capacity'] <= ram_range[1]) &
        (df['storage_capacity'] >= storage_range[0]) &
        (df['storage_capacity'] <= storage_range[1])
        ]


        filtered_df = filtered_df[filtered_df['brand_name'] == selected_brand]  

        st.title(f"**{selected_brand}**")
        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Total Models", len(filtered_df))
        c2.metric("Avg. Price", f"₹{round((filtered_df['price'].mean()),0):,}")
        c3.metric("Median Rating", round(filtered_df['rating'].median(), 1))
        c4.metric("5G Adoption", f"{round(filtered_df['has_5g'].mean() * 100, 1)}%")

        fig,ax = plt.subplots(figsize = (8,4))
        sns.histplot(filtered_df['price'], kde=True, bins=30, ax=ax)
        ax.set_title("Price Distribution")
        ax.set_xlabel("Price (INR)")
        st.pyplot(fig)

        fig,ax = plt.subplots(figsize = (8,4))
        sns.histplot(filtered_df['rating'].dropna(), kde=True, bins=20, ax=ax, color='orange')
        ax.set_title("Rating Distribution")
        ax.set_xlabel("Rating (0–100)")
        st.pyplot(fig)
            
        df_display = filtered_df[['model','price','rating','ram_capacity','storage_capacity','battery_capacity','refresh_rate','max_rear_camera_MP','os']].reset_index(drop=True).replace(np.nan,'N/A')
        df_display.index = df_display.index + 1

        st.dataframe(df_display)
    else:
        st.sidebar.error("Column 'brand_name' not found in data.")

if options == 'Feature Explorer':
    st.sidebar.title("Feature Explorer")

    num_cols = ['price', 'rating', 'ram_capacity', 'storage_capacity',
            'processor_speed', 'battery_capacity', 'fast_charging',
            'display_size', 'refresh_rate', 'max_rear_camera_MP', 'max_front_camera_MP']
    
    st.sidebar.subheader("Select 2 Features to compare")
    
    x_var = st.sidebar.selectbox("Select First Feature",num_cols,index=0)
    y_var = st.sidebar.selectbox("Select Second Feature",[f for f in num_cols if f!=x_var],index=1)

    st.title(f"Comparing {x_var} & {y_var}",width="stretch")

    col1,col2 = st.columns(2)

    with col1:
        st.header("Scatterplot")
    with col2:
        corr = df[x_var].corr(df[y_var])
        st.metric(label="**Correlation Value (%)**", value=round(corr, 3)*100)

    fig,ax = plt.subplots(figsize = (8,5))
    sns.scatterplot(data=df,x= x_var,y = y_var)
    ax.set_xlabel(x_var.replace("_"," ").title())    
    ax.set_ylabel(y_var.replace("_"," ").title())
    st.pyplot(fig)

if options == 'Compare Phones':

    st.sidebar.title("Compare Phones")
    models = df['model'].dropna().unique()
    phone_1 = st.sidebar.selectbox("Select 1st Phone",sorted(models))
    phone_2 = st.sidebar.selectbox("Select 2nd Phone",sorted([m for m in models if m != phone_1]))
    

    phoneA = df[df['model'] == phone_1].iloc[0]
    phoneB = df[df['model'] == phone_2].iloc[0]

    st.markdown(f"### Comparing **{phone_1}** vs **{phone_2}**")

    specs = {
    "Brand": [phoneA['brand_name'], phoneB['brand_name']],
    "Price (₹)": [int(phoneA['price']), int(phoneB['price'])],
    "Rating": [phoneA['rating'], phoneB['rating']],
    "RAM (GB)": [phoneA['ram_capacity'], phoneB['ram_capacity']],
    "Storage (GB)": [phoneA['storage_capacity'], phoneB['storage_capacity']],
    "Processor Speed (GHz)": [phoneA['processor_speed'], phoneB['processor_speed']],
    "Battery (mAh)": [phoneA['battery_capacity'], phoneB['battery_capacity']],
    "Refresh Rate (Hz)": [phoneA['refresh_rate'], phoneB['refresh_rate']],
    "Max Rear Camera (MP)": [phoneA['max_rear_camera_MP'], phoneB['max_rear_camera_MP']],
    "Max Front Camera (MP)": [phoneA['max_front_camera_MP'], phoneB['max_front_camera_MP']],
    "5G Support": ['Yes' if phoneA['has_5g'] else 'No', 'Yes' if phoneB['has_5g'] else 'No'],
    "NFC": ['Yes' if phoneA['has_nfc'] else 'No', 'Yes' if phoneB['has_nfc'] else 'No'],
    "IR Blaster": ['Yes' if phoneA['has_ir_blaster'] else 'No', 'Yes' if phoneB['has_ir_blaster'] else 'No'],
    "SD Card Support": ['Yes' if phoneA['card_supported'] else 'No', 'Yes' if phoneB['card_supported'] else 'No'],
    "Operating System": [phoneA['os'], phoneB['os']],
    "SIM Type": [phoneA['sim_type'], phoneB['sim_type']]
    }  

    comp_table = pd.DataFrame(specs, index=[phone_1, phone_2]).T
    comp_table = comp_table.replace(np.nan, "N/A")
    st.table(comp_table)

    st.markdown("### Other Features")
    cat_cols = ['has_5g', 'has_nfc', 'has_ir_blaster', 'card_supported', 'os', 'sim_type']
    cat_labels = {
        'has_5g': '5G Support',
        'has_nfc': 'NFC',
        'has_ir_blaster': 'IR Blaster',
        'card_supported': 'SD Card',
        'os': 'Operating System',
        'sim_type': 'SIM Type'
    }

    comp_data = {
        'Feature': [cat_labels[col] for col in cat_cols],
        phone_1: [phoneA[col] for col in cat_cols],
        phone_2: [phoneB[col] for col in cat_cols],
    }

    comp_df = pd.DataFrame(comp_data)

    comp_df.index = comp_df.index + 1

    st.table(comp_df)

    features = ['ram_capacity', 'storage_capacity', 'processor_speed', 'refresh_rate']
    labels = ['RAM (GB)', 'Storage (GB)', 'Processor (GHz)', 'Refresh Rate (Hz)']
    valuesA = [phoneA[feat] for feat in features]
    valuesB = [phoneB[feat] for feat in features]


    fig, ax = plt.subplots(figsize=(8, 4))

    x = np.arange(len(features))
    width = 0.4
    ax.bar(x - width/2, valuesA, width=width, label=str(phone_1))
    ax.bar(x + width/2, valuesB, width=width, label=str(phone_2))
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=0)
    # ax.set_ylim((0,100))
    ax.set_ylabel("Value")
    ax.set_title("Spec Comparison")
    ax.minorticks_on()
    ax.grid(which='major', linestyle='-', linewidth=0.8)
    ax.grid(which='minor', linestyle=':', linewidth=0.5)
    st.pyplot(fig)


if options == 'EDA / Raw Data':

    columns_to_show = [
    'brand_name', 'model', 'price', 'rating',
    'ram_capacity', 'storage_capacity', 'battery_capacity', 'processor_speed',
    'refresh_rate', 'display_size',
    'has_5g', 'has_nfc', 'has_ir_blaster', 'card_supported',
    'max_rear_camera_MP', 'max_front_camera_MP',
    'os', 'sim_type'
    ]

    st.markdown("## Filtered Smartphone Dataset")

    col1,col2 = st.columns(2)

    with col1:

        csv_data = df.to_csv(index=False)

        st.download_button(
        label="Download Cleaned Data as CSV",
        data=csv_data,
        file_name="Cleaned_smartphones.csv",
        mime="text/csv"
        )

        with open('SmartPhone_EDA (2).ipynb', "rb") as f:
            eda_byte = f.read()

    with col2:

        st.download_button(
            label="Download Smartphone EDA file (.ipynb)",
            data=eda_byte,
            file_name="SmartPhone_EDA.ipynb",  # <-- required for correct filename
            mime="application/x-ipynb+json"
        )
    st.space()
    st.markdown(f"#### Showing **{df.shape[0]}** phones with selected filters.")

    df.index = df.index+1
    
    st.dataframe(df[columns_to_show])





