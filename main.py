import streamlit as st
import requests
import pandas as pd
from streamlit_lottie import st_lottie
import datetime
import pygsheets
import os

st.set_page_config(initial_sidebar_state="collapsed",page_title="HackOn", page_icon="📧",layout="wide")

# Initialize pygsheets and wks object outside the main block
service_file = os.environ.get("service_account_file", "haclathons-c80937c3ef59.json")


gc = pygsheets.authorize(service_file=service_file)
sheetname = "hackon"
sh = gc.open(sheetname)
wks = sh.worksheet_by_title("Sheet1")
hackathon_list = []


def load_anime(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error loading animation: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")
        return None


def handle_email_subscription():
    inputted_email = st.text_input("Enter your email address:")
    submit = st.button("Subscribe")

    if submit:
        inputted_email = inputted_email.strip()
        if not inputted_email:
            st.error("Please enter a valid email address.")
            return

        # Append email to spreadsheet using wks object
        wks.append_table([inputted_email])

        # Send confirmation message
        st.success("Thank you for subscribing to our hackathon newsletter!")
        st.divider()
    else:
        st.info("Stay ahead: Subscribe for Hackathon Updates")
        st.divider()


def fetch_hackathons():
    id = "1wSUVUO2eTGVVe0UVlR5_0P6N3SNFwnMEEX0S535jqS8"
    name = "Hackathons"
    url = f"https://docs.google.com/spreadsheets/d/{id}/gviz/tq?tqx=out:csv&sheet={name}"

    try:
        hackathons_data = pd.read_csv(url)
        return hackathons_data
    except Exception as e:
        print(f"Error fetching hackathon data: {e}")
        return None


if __name__ == "__main__":
    # Load Lottie animation
    animation = load_anime("https://lottie.host/33364c89-21fa-4fe8-a3c9-8fe46d87d797/s5zqAOz8yX.json")

    # Display main content
    with st.container():
        # Top section
        st.title("HackOn")
        st.subheader("Curated List Of Live Online Hackathons")
        st.divider()

        try:
            st_lottie(animation, height=300)
        except:
            print("Error Loading Animation")

        handle_email_subscription()

    # Fetch and display hackathon data
    hackathons_data = fetch_hackathons()

    if hackathons_data is not None:
        with st.container():
            st.subheader(datetime.datetime.now().strftime("%A, %B %d, %Y"))
            st.divider()

            for index, row in hackathons_data.iterrows():
                hackathon_name = row["Hacakthons"]
                hackathon_link = row["Links"]

                hackathon_info = {
                    "name": hackathon_name,
                    "link": hackathon_link,
                }

                hackathon_list.append(hackathon_info)

            hackathon_list.sort(key=lambda x: x["name"])

            for hackathon in hackathon_list:
                with st.expander(f"**{hackathon['name']}**"):
                    st.write(f"**Link:** {hackathon['link']}")

            st.divider()

    # Display footer message
    with st.container():
        st.markdown("###### Made with :heart: by @muhammedashharps")


