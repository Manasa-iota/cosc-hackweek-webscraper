import streamlit as st
from scraper import GitHubTrendingScraper

st.title("Web Scraping Safari")

if st.button("get top 5 trending github repositories"):
    scraper = GitHubTrendingScraper()
    html = scraper.fetch_html()
    repos = scraper.parse_repositories(html)
    scraper.export_to_csv(repos)

    st.success("Scraping completed. Top trending repositories:")
    for name, url in repos:
        st.markdown(f"- [{name}]({url})")
