import streamlit as st

# Configure the page
st.set_page_config(
    page_title="Job Scraper",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main() -> None:
    """Main Streamlit application"""
    st.sidebar.title("Job Scraper")
    st.sidebar.write("Navigate through the pages using the menu below")

    # Navigation
    page = st.sidebar.radio(
        "Select a page",
        ["Manual Entry", "Scrape URL", "View Jobs"],
        index=0,
    )

    if page == "Manual Entry":
        from streamlit_app.pages import manual_entry

        manual_entry.show()
    elif page == "Scrape URL":
        st.title("Scrape URL")
        st.write("URL scraping feature - Coming soon!")
        st.info("Use the CLI with `--url` flag for now")
    elif page == "View Jobs":
        st.title("View Jobs")
        st.write("Job viewing feature - Coming soon!")


if __name__ == "__main__":
    main()
