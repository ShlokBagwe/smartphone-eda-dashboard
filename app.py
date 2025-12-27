import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Smartphone Market Insights",
    page_icon="",
    layout="wide"
)

data_path = Path(__file__).parent / "smartphones.csv"

try:
    df = pd.read_csv(data_path)
except FileNotFoundError:
    st.error("smartphones.csv not found. Please place it next to app.py.")
    st.stop()

st.sidebar.title("Smartphone Market Insights")
st.sidebar.divider()

page = st.sidebar.radio(
    "Navigate",
    [
        "Market Overview",
        "Price Drivers",
        "Feature Myths",
        "Brand Positioning",
        "Compare Phones",
        "Raw Data"
    ]
)

if page == "Market Overview":

    st.title("Smartphone Market Overview")

    st.markdown("""
    This dashboard analyzes **981 smartphones** across major brands to explain  
    how the smartphone market is structured and priced.
    """)

    # Metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Phones", df.shape[0])
    c2.metric("Median Price", f"₹{int(df['price'].median()):,}")
    c3.metric("5G Adoption", f"{round(df['has_5g'].mean()*100, 1)}%")
    c4.metric("Median Rating", round(df['rating'].median(), 1))

    st.divider()

    st.subheader("Price Distribution")

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(df['price'], bins=40, kde=True, ax=ax)
    ax.set_xlabel("Price (INR)")
    ax.set_ylabel("Count")
    st.pyplot(fig)

    st.markdown("""
    **Key Insight**
    - The market is **right-skewed**
    - Most phones fall between **₹10,000 – ₹35,000**
    - A small number of flagships push prices above ₹100,000
    """)

    st.subheader("Market Segments")
    st.markdown("""
    - **Budget**: Below ₹15,000  
    - **Mid-range**: ₹15,000 – ₹35,000  
    - **Premium**: Above ₹35,000  

    The **mid-range segment dominates** the market.
    """)

elif page == "Price Drivers":

    st.title("What Drives Smartphone Prices?")

    st.markdown("""
    Not all specifications influence price equally.
    Below are the **strongest drivers of smartphone pricing**.
    """)

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.scatterplot(data=df, x='ram_capacity', y='price', ax=ax)
        ax.set_title("Price vs RAM")
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.scatterplot(data=df, x='storage_capacity', y='price', ax=ax)
        ax.set_title("Price vs Storage")
        st.pyplot(fig)

    col3, col4 = st.columns(2)

    with col3:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.scatterplot(data=df, x='processor_speed', y='price', ax=ax)
        ax.set_title("Price vs Processor Speed")
        st.pyplot(fig)

    with col4:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.boxplot(data=df, x='has_5g', y='price', ax=ax)
        ax.set_title("Price vs 5G Support")
        ax.set_xlabel("5G (0 = No, 1 = Yes)")
        st.pyplot(fig)

    st.markdown("""
    **Key Takeaways**
    - **RAM & Storage** are the strongest price drivers  
    - **Processor speed** moderately increases price  
    - **5G phones** are significantly more expensive  
    - Hardware matters more than cosmetic features
    """)

elif page == "Feature Myths":

    st.title("Smartphone Feature Myths")

    # Camera MP
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.scatterplot(data=df, x='max_rear_camera_MP', y='price', ax=ax)
    ax.set_title("Camera MP vs Price")
    st.pyplot(fig)

    st.markdown("""
    **Myth 1: More megapixels = higher price**

    False.  
    Most phones cluster around **48–64 MP**, yet prices vary widely.
    Camera quality depends on sensors and software — not MP alone.
    """)

    fig, ax = plt.subplots(figsize=(7, 4))
    sns.scatterplot(data=df, x='battery_capacity', y='price', ax=ax)
    ax.set_title("Battery Capacity vs Price")
    st.pyplot(fig)

    st.markdown("""
    **Myth 2: Bigger battery means premium phone**

    False.  
    Battery size shows **little relationship with price**.
    Large batteries are common in budget phones as well.
    """)

    fig, ax = plt.subplots(figsize=(7, 4))
    sns.scatterplot(data=df, x='rating', y='price', ax=ax)
    ax.set_title("Rating vs Price")
    st.pyplot(fig)

    st.markdown("""
    **Myth 3: Higher price = better rating**

    False.  
    Highly rated phones exist across all price ranges.
    Value matters more than price.
    """)

elif page == "Brand Positioning":

    st.title("Brand Positioning")

    brand_counts = df['brand_name'].value_counts()
    big_brands = brand_counts[brand_counts > 10].index
    brand_df = df[df['brand_name'].isin(big_brands)]

    median_price = (
        brand_df.groupby('brand_name')['price']
        .median()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=median_price.index, y=median_price.values, ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.set_title("Median Price by Brand")
    ax.set_ylabel("Price (INR)")
    st.pyplot(fig)

    st.markdown("""
    **Brand Strategy Insights**
    - **Apple** → Premium-only  
    - **Samsung / Xiaomi** → Full market coverage  
    - **Realme / Poco** → Budget & value focused
    """)

elif page == "Compare Phones":

    st.title("Compare Two Smartphones")

    models = sorted(df['model'].dropna().unique())

    c1, c2 = st.columns(2)
    phone_1 = c1.selectbox("Select Phone A", models)
    phone_2 = c2.selectbox("Select Phone B", [m for m in models if m != phone_1])

    p1 = df[df['model'] == phone_1].iloc[0]
    p2 = df[df['model'] == phone_2].iloc[0]

    compare_df = pd.DataFrame({
        phone_1: p1,
        phone_2: p2
    })

    compare_df = compare_df.loc[
        [
            'price',
            'rating',
            'ram_capacity',
            'storage_capacity',
            'processor_speed',
            'battery_capacity',
            'refresh_rate',
            'max_rear_camera_MP',
            'has_5g',
            'os'
        ]
    ]

    st.table(compare_df)

elif page == "Raw Data":

    st.title("Dataset Access")

    st.markdown("Download or explore the cleaned smartphone dataset.")

    st.download_button(
        "Download CSV",
        df.to_csv(index=False),
        file_name="cleaned_smartphones.csv",
        mime="text/csv"
    )

    st.dataframe(df)
