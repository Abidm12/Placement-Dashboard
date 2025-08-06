import streamlit as st
import pandas as pd
import altair as alt

# Load dataset
df = pd.read_excel("all_placed_data.xlsx", engine="openpyxl")

df.columns = df.columns.str.strip()
df['Package'] = pd.to_numeric(df['Package'], errors='coerce')
# Page config
st.set_page_config(page_title="Placement Overview", layout="wide")

# Sidebar filters
st.sidebar.header("🔎 Filter Data")
years = sorted(df['Year'].dropna().unique())
branches = sorted(df['Branch'].dropna().unique())
selected_year = st.sidebar.selectbox("Select Year", options=["All"] + list(years))
selected_branch = st.sidebar.selectbox("Select Branch", options=["All"] + list(branches))
# Sidebar QR and Download section
with st.sidebar.expander("📥 Download Report"):
    

    # Display actual QR code image
    st.image("QR_link.png", caption="Scan to open the report", use_container_width=True)

# Apply filters
filtered_df = df.copy()
if selected_year != "All":
    filtered_df = filtered_df[filtered_df['Year'] == selected_year]
if selected_branch != "All":
    filtered_df = filtered_df[filtered_df['Branch'] == selected_branch]

# Total students placed
total_placed = filtered_df[filtered_df['Package'].notnull()]['Name'].nunique()


# Title and Description
st.markdown("<h2 style='text-align: center;'>📈 Placement Overview</h2>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; font-size: 16px;'>
Explore key placement statistics including top hiring companies and package trends.
</div>
""", unsafe_allow_html=True)
st.markdown("---")



st.markdown("<h3 style='text-align:center;'>📊 Trends Over the Years</h3>", unsafe_allow_html=True)

# 1. Total Placements per Year
st.markdown("##### 📈 Total Students Placed Per Year")
yearly_placements = df[df['Package'].notnull()].groupby('Year')['Name'].nunique().reset_index()
yearly_placements.columns = ['Year', 'Placed']

chart1 = alt.Chart(yearly_placements).mark_line(point=True).encode(
    x=alt.X('Year:O'),
    y=alt.Y('Placed:Q', title='No. of Students Placed'),
    tooltip=['Year', 'Placed']
).properties(width=600, height=300)

col1, col2 = st.columns([2, 1])
with col1:
    st.altair_chart(chart1, use_container_width=True)
with col2:
    st.markdown("""
    This line chart shows the number of students placed each year, allowing you to track the overall placement performance of the institute over time.
    """)

# 2. Average Package per Year
st.markdown("##### 💹 Average Package Per Year")
avg_package_year = df[df['Package'].notnull()].groupby('Year')['Package'].mean().reset_index()
avg_package_year.columns = ['Year', 'Average_Package']

chart2 = alt.Chart(avg_package_year).mark_line(point=True, color='green').encode(
    x=alt.X('Year:O'),
    y=alt.Y('Average_Package:Q', title='Avg Package (LPA)'),
    tooltip=['Year', alt.Tooltip('Average_Package:Q', format=".2f")]
).properties(width=600, height=300)

col3, col4 = st.columns([2, 1])
with col3:
    st.altair_chart(chart2, use_container_width=True)
with col4:
    st.markdown("""
    This graph reflects how the average salary packages have evolved over the years, indicating the demand and compensation trends across all branches.
    """)


# --- Section 1: Top Hiring Companies (Graph Left, Info Right) ---
st.markdown("<h4 style='text-align: center;'>🏢 Top Hiring Companies</h4>", unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    top_companies = filtered_df['Company'].value_counts().head(7).reset_index()
    top_companies.columns = ['Company', 'Count']
    chart1 = alt.Chart(top_companies).mark_bar(color='steelblue').encode(
        x=alt.X('Count:Q', title='No. of Students'),
        y=alt.Y('Company:N', sort='-x')
    ).properties(width=500, height=250)
    st.altair_chart(chart1, use_container_width=True)
with col2:
    st.markdown("This chart displays the **top companies** that hired the most students. It helps identify the most active recruiters on campus.")

# --- Section  3: Average Package or Distribution (Zigzag: Graph Left, Info Right) ---
if selected_branch == "All":
    st.markdown("<h4 style='text-align: center;'>💰Branchwise Average Package</h4>", unsafe_allow_html=True)
    col5, col6 = st.columns([1, 1])
    with col5:
        avg_package = filtered_df.groupby("Branch")["Package"].mean().sort_values(ascending=False).reset_index()
        avg_package.columns = ['Branch', 'Average_Package']
        chart3 = alt.Chart(avg_package).mark_bar(color='aliceblue').encode(
            x=alt.X('Average_Package:Q', title='Avg Package (LPA)'),
            y=alt.Y('Branch:N', sort='-x')
        ).properties(width=500, height=250)
        st.altair_chart(chart3, use_container_width=True)
    with col6:
        st.markdown("This bar chart illustrates the **average salary** received by students in each branch, highlighting departments with the highest compensation.")
else:
    st.markdown("<h4 style='text-align: center;'>📈 Package Distribution</h4>", unsafe_allow_html=True)
    col5, col6 = st.columns([1, 1])
    with col5:
        pkg_distribution = filtered_df[['Name', 'Package']].dropna()
        chart4 = alt.Chart(pkg_distribution).mark_bar().encode(
            x=alt.X('Package:Q', bin=alt.Bin(maxbins=10), title="Package (LPA)"),
            y=alt.Y('count()', title='No. of Students')
        ).properties(width=500, height=250)
        st.altair_chart(chart4, use_container_width=True)
    with col6:
        st.markdown("This histogram shows how packages are **distributed among students** in the selected branch, giving a sense of range and concentration.")
            # --- Branch Summary moved here ---
    st.markdown("<h4 style='text-align: center;'>📊 Branch Summary</h4>", unsafe_allow_html=True)
    col_summary_left, col_summary_right = st.columns([1, 1])
    with col_summary_left:
        st.markdown("This section summarizes the **key statistics** for the selected branch, helping students and parents quickly understand the placement performance.")
    with col_summary_right:
        avg_pkg = filtered_df['Package'].mean()
        max_pkg = filtered_df['Package'].max()
        min_pkg = filtered_df['Package'].min()
        top_recruiters = filtered_df['Company'].value_counts().head(3).index.tolist()
        st.markdown(f"""
        - **Branch:** `{selected_branch}`  
        - **Average Package:** `{avg_pkg:.2f} LPA`  
        - **Highest Package:** `{max_pkg:.2f} LPA`  
        - **Lowest Package:** `{min_pkg:.2f} LPA`  
        - **Top Recruiters:** `{", ".join(top_recruiters)}`  
        """)


# --- Dashboard Summary (Only for 'All') ---
if selected_branch == "All":
    st.markdown("---")
    st.markdown("<h4 style='text-align: center;'>🔍 Dashboard Summary</h4>", unsafe_allow_html=True)
    st.markdown(f"""
    - **Year:** `{selected_year}`  
    - **Branch:** `{selected_branch}`  
    - **Students Placed:** `{total_placed}`  
    - **Top Companies:** Visualized in hiring chart  
    - **Placement by Branch:** Shown via pie chart  
    """)

st.markdown("<h4 style='text-align: center;'>🧮 Branchwise Placement Distribution</h4>", unsafe_allow_html=True)

# Load external Excel file for pie charts
pie_data = pd.read_excel("all_report_data.xlsx", engine="openpyxl")
pie_data.columns = pie_data.columns.str.strip()
pie_data['Branch'] = pie_data['Branch'].astype(str).str.strip()

# Show pie chart for selected branch, or loop through all if "All"
branches_to_plot = [selected_branch] if selected_branch != "All" else sorted(pie_data['Branch'].unique())

for branch in branches_to_plot:
    branch_df = pie_data[pie_data['Branch'] == branch]
    
    if branch_df.empty:
        continue  # Skip if no data

    eligible = int(branch_df['Eligible_Students'].values[0])
    placed = int(branch_df['Placed_Students'].values[0])
    unplaced = max(eligible - placed, 0)

    pie_chart_data = pd.DataFrame({
        'Status': ['Placed', 'Unplaced'],
        'Count': [placed, unplaced]
    })

    col_left, col_right = st.columns([1, 1])
    with col_left:
        st.markdown(f"### 📘 {branch} Branch Summary")
        st.markdown(f"""
        - **Eligible Students:** `{eligible}`  
        - **Placed Students:** `{placed}`  
        - **Unplaced Students:** `{unplaced}`  
        """)
    with col_right:
        chart = alt.Chart(pie_chart_data).mark_arc(innerRadius=50).encode(
            theta=alt.Theta(field="Count", type="quantitative"),
            color=alt.Color(field="Status", type="nominal", scale=alt.Scale(scheme='tableau10')),
            tooltip=['Status', 'Count']
        ).properties(width=400, height=250)
        st.altair_chart(chart, use_container_width=True)




    












