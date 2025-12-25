import streamlit as st
from module_extractor import run_extractor

st.set_page_config(
    page_title="Pulse – Module Extraction AI Agent",
    layout="wide"
)

st.title("Pulse – Module Extraction AI Agent")
st.write("Extract product modules and submodules from documentation URLs.")

urls_input = st.text_area(
    "Enter documentation URLs (comma-separated)",
    value="https://wordpress.org/documentation/",
    height=120
)

if st.button("Extract Modules"):
    urls = [u.strip() for u in urls_input.split(",") if u.strip()]

    if not urls:
        st.warning("Please enter at least one valid URL.")
    else:
        with st.spinner("Analyzing documentation..."):
            result = run_extractor(urls)

        if not result:
            st.warning("No modules could be extracted from the provided URLs.")
        else:
            st.success("Extraction completed successfully!")
            st.json(result)
