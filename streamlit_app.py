import streamlit as st
import subprocess
from pathlib import Path
import numpy as np
import pandas as pd

st.set_page_config(page_title="FreelanceScripts Toolkit", layout="wide")


st.title("🛠️ FreelanceScripts - Python Starter Toolkit")
st.markdown("Use the sidebar to select a tool and run it with a user-friendly interface.")

# Sidebar options
tool = st.sidebar.selectbox("Select a Tool", [
    "Home",
    "CSV ⇄ JSON Converter",
    "Simple Web Scraper",
    "Portfolio Generator",
    "Watch Automation",
    "Executioner & Packaging"
])

# Tool logic
if tool == "Home":
    st.markdown("Welcome to the FreelanceScripts GUI! \n\n"
                "This is a user-friendly interface for the Python starter toolkit designed for freelancers. \n\n"
                "You can run various tools directly from this app without needing to use the terminal. \n\n"
                "Each tool is designed to help you automate common tasks, manage your projects, and streamline your workflow. \n\n"
                "### Available Tools:\n")

# This app provides an interface to several freelance-ready Python tools.")
    st.markdown("- Convert CSV/JSON")
    st.markdown("- Scrape web content")
    st.markdown("- Auto-generate portfolio content")
    st.markdown("- Package scripts")
    st.markdown("- Monitor directories for changes")

elif tool == "CSV ⇄ JSON Converter":
    st.header("📄 CSV ⇄ JSON Converter")
    conversion = st.radio("Select conversion direction:", ("CSV to JSON", "JSON to CSV"))
    uploaded_file = st.file_uploader("Upload your file", type=["csv", "json"])
    if uploaded_file and st.button("Convert"):
        path = Path("uploads")
        path.mkdir(exist_ok=True)
        input_path = path / uploaded_file.name
        input_path.write_bytes(uploaded_file.read())
        command = f"python3 csv_json_converter/csv_json_converter_tool.py {'c2j' if conversion == 'CSV to JSON' else 'j2c'} {input_path}"
        st.code(command)
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        st.text(result.stdout)
        if result.stderr:
            st.error(result.stderr)

elif tool == "Simple Web Scraper":
    st.header("🌐 Simple Web Scraper")
    url = st.text_input("Enter URL", "https://news.ycombinator.com/")
    selector = st.text_input("CSS Selector", "span.titleline a")
    if st.button("Scrape"):
        command = f"python3 scraper/simple_scraper_tool.py {url} --selector '{selector}'"
        st.code(command)
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        st.text(result.stdout)
        if result.stderr:
            st.error(result.stderr)
        # Show preview of output file if it exists
        output_path = Path(f"output/{url.split('//')[-1].replace('/', '_').replace('.', '_')}.json")
        if output_path.exists():
            st.markdown("**Scraper Output Preview:**")
            with open(output_path, "r") as f:
                st.json(f.read())

elif tool == "Portfolio Generator":
    st.header("📝 Portfolio Generator")
    user_name = st.text_input("Github Username")
    # description = st.text_area("Project Description")
    # features = st.text_area("List of Features (comma-separated)")
    url = f"https://www.github.com/{user_name}"
    if st.button("Generate"):
        command = f"python portfolio_generator/portfolio_generator_tool.py {url}   "
        st.code(command)
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        st.text(result.stdout)
        if result.stderr:
            st.error(result.stderr)
        # Show preview of portfolio.md if it exists
        portfolio_path = Path("portfolio.md")
        if portfolio_path.exists():
            st.markdown("**Portfolio Preview:**")
            with open(portfolio_path, "r") as f:
                st.markdown(f.read())

elif tool == "Watch Automation":
    st.header("🔁 Watch Automation (Simulated)")
    st.warning("Watch automation tools are better suited for terminal use. GUI simulation coming soon.")

elif tool == "Executioner & Packaging":
    st.header("📦 Executioner & Packaging")
    if st.button("Make all tools executable"):
        command = "python3 executioner/executioner_tool.py"
        st.code(command)
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        st.text(result.stdout)
        if result.stderr:
            st.error(result.stderr)
