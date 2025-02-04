import streamlit as st
import pandas as pd
from helpers import *

# Load custom CSS for responsiveness
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("styles.css")

# Inject custom CSS for dynamic subheader styling & sidebar gradients
st.markdown("""
    <style>
        /* Subheader styling */
        .summer-header { color: lightyellow !important; font-size: 22px; font-weight: bold; }
        .winter-header { color: powderblue !important; font-size: 22px; font-weight: bold; }

        /* Sidebar gradient text styling */
        .sidebar-radio-title {
            font-size: 18px;
            font-weight: bold;
            background: linear-gradient(to right, #ff6ec4, #7873f5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: block;
            text-align: center;
        }
        
        .sidebar-radio-analysis {
            font-size: 18px;
            font-weight: bold;
            background: linear-gradient(to right, #8e2de2, #ff0844);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: block;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Preprocess Data
summer, winter = data_preprocessor()
summer, winter = duplicate_rows_remover(summer, winter)

summer.dropna(subset=["region"], inplace=True)
winter.dropna(subset=["region"], inplace=True)

# Sidebar Menu
st.sidebar.markdown(
    """
    <div style="text-align: center;">
        <h1 style='color: powderblue;'>Olympic Medal Analysis</h1><br>
    </div>
    """, 
    unsafe_allow_html=True
)


st.sidebar.image("medal.jpg", use_container_width=True)  # Olympic logo
st.sidebar.markdown("<hr style='border:2px solid white'>", unsafe_allow_html=True)

st.sidebar.markdown("<h1 style='color:red;'> NAVIGATION BAR : -</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<br>", unsafe_allow_html=True)

# Custom styled sidebar headers

st.sidebar.markdown(
    "<div style='text-align: left; font-size: 18px; font-weight: bold; color: #2AFADF;'>🌍 Select Olympic Season:</div>", 
    unsafe_allow_html=True
)
season = st.sidebar.radio("", ("Summer", "Winter"))
st.sidebar.markdown("<br>", unsafe_allow_html=True)

st.sidebar.markdown(
    "<div style='text-align: left; font-size: 18px; font-weight: bold; color: #D946EF;'>📶 Select Analysis Type:</div>", 
    unsafe_allow_html=True
)
options = st.sidebar.radio("", ("Medal-Tally", "Country-Wise", "Year-Wise", "Year-Wise Progress"))
st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.markdown("<hr style='border:2px solid white'>", unsafe_allow_html=True)
st.sidebar.markdown(
    "<h3 style='color:rgb(251, 80, 188);'>🏅 Select a Country whose first medal related information you want:</h3>", 
    unsafe_allow_html=True
)
country = st.sidebar.selectbox("", ["India", "Russia", "America"])





# Dynamic main title with styling
st.markdown(
    f"<h1 style='text-align: center;'>🏆 {season} Olympics - {options} Analysis</h1>",
    unsafe_allow_html=True
)

# Function to dynamically create styled subheaders
def styled_subheader(text):
    color_class = "summer-header" if season == "Summer" else "winter-header"
    st.markdown(f'<h3 class="{color_class}">{text}</h3>', unsafe_allow_html=True)

# Medal Tally Analysis
if options == "Medal-Tally":
    styled_subheader(f"🏅 {season} Olympics Medal Tally")
    medal_pivot = medal_tally_calculator(summer if season == "Summer" else winter)
    medal_pivot = medal_pivot.sort_values(by=["Gold", "Silver", "Bronze"], ascending=False)
    st.dataframe(medal_pivot, use_container_width=True)

# Country-Wise Analysis
elif options == "Country-Wise":
    styled_subheader(f"🌍 {season} Country-Wise Analysis")
    medal_pivot = medal_tally_calculator(summer if season == "Summer" else winter)
    noc = st.selectbox("Select NOC:", medal_pivot.index.tolist())
    details = country_wise_search(noc, medal_pivot)
    table = pd.DataFrame.from_dict(details, orient="index", columns=["Value"])
    st.dataframe(table, use_container_width=True)

# Year-Wise Analysis
elif options == "Year-Wise":
    styled_subheader(f"📅 {season} Year-Wise Analysis")
    dataset = summer if season == "Summer" else winter
    years = sorted(dataset["Year"].unique())
    selected_year = st.selectbox("Select Year", years)
    countries = sorted(dataset[dataset["Year"] == selected_year]["region"].unique())
    selected_country = st.selectbox("Select Country:", countries)
    plot_medals(selected_year, selected_country, dataset)

# Year-Wise Progress Analysis
elif options == "Year-Wise Progress":
    styled_subheader(f"📈 Year-Wise Progress ({season})")
    dataset = summer if season == "Summer" else winter
    countries = sorted(dataset["region"].unique())
    selected_country = st.selectbox("Choose Country:", countries)
    year_analysis(selected_country, dataset)

st.markdown("<hr style='border:2px solid powderblue'>", unsafe_allow_html=True)

# Function to display India's first gold medal details
def india_first_gold():
    st.markdown("## IND-India's First Olympic Gold Medal")
    st.markdown("**🏑 Sport:** Field Hockey")
    st.markdown("**🏆 Event:** Men's Hockey")
    st.markdown("**📅 Year:** 1928")
    st.markdown("**🎖️ Captain:** Jaipal Singh Munda")
    st.markdown("**⭐ Star Player:** Dhyan Chand (scored 14 goals in the tournament)")
    
    st.markdown("### 🔹 Biography of Dhyan Chand:")
    st.markdown("""
    1. Dhyan Chand was an Indian field hockey player, widely regarded as one of the greatest hockey players of all time.
    2. He won three Olympic gold medals (1928, 1932, 1936) and played a crucial role in India's dominance in hockey.
    3. Known as the **"Hockey Wizard,"** his ball control and goal-scoring ability were legendary.
    4. He was awarded **India's Padma Bhushan** in 1956 for his contributions to sports.
    5. His birthday, **August 29**, is celebrated as **National Sports Day** in India. 🚀🏑""")

# Function to display Russia's first gold medal details
def russia_first_gold():
    st.markdown("## RUS-Russia's First Olympic Gold Medal")
    st.markdown("**🔹 Athlete:** Nikolai Panin-Kolomenkin")
    st.markdown("**⛸️ Sport:** Figure Skating")
    st.markdown("**🏆 Event:** Men’s Special Figures")
    st.markdown("**📅 Year:** 1908 London Olympics")
    st.markdown("**🎖️ Achievement:** He became Russia's first-ever Olympic gold medalist, winning in figure skating.")
    st.markdown("### 🔹 Biography of Nikolai Panin-Kolomenkin:")
    st.markdown("""
     1. Nikolai Panin-Kolomenkin (born January 12, 1872 - died January 19, 1956) was a Russian figure skater and the first-ever Olympic gold medalist for Russia.
     2. His legacy remains in Russian sports history as a pioneer of figure skating, inspiring future generations of skaters.
     """)

# Function to display USA's first gold medal details
def usa_first_gold():
    st.markdown("## USA - America's First Olympic Gold Medal")
    st.markdown("**🔹 Athlete:** James Brendan Connolly")
    st.markdown("**🏃 Sport:** Athletics (Track & Field)")
    st.markdown("**🏆 Event:** Triple Jump")
    st.markdown("**📅 Year:** 1896 Athens Olympics")
    st.markdown("**🎖️ Achievement:** He became the first-ever Olympic champion of the modern Olympic Games by winning gold in the triple jump.")
    st.markdown("### 🔹Biography of James Brendan Connolly:")
    st.markdown("""
    1. James Brendan Connolly (born October 28, 1868 - died January 20, 1957) was an American track and field athlete, best known for winning the first-ever Olympic gold medal of the modern Olympic Games in 1896.
    2.  He won gold in the triple jump at the 1896 Athens Olympics, becoming the first Olympic champion in over 1,500 years.

    3.Connolly also competed in the long jump and high jump, securing a silver medal in the long jump
    """)

# Display content based on selected country
if country == "India":
    india_first_gold()
elif country == "Russia":
    russia_first_gold()
elif country == "America":
    usa_first_gold()













    
   


# Footer
st.markdown("<footer>Made with ❤️ using Streamlit</footer>", unsafe_allow_html=True)
