# Publish the dashboard

The repository is designed to run locally with Streamlit. For a public interactive demo:

1. Push this repository to GitHub.
2. Sign in to Streamlit Community Cloud and choose **Create app**.
3. Select this repository, the `main` branch, and `app.py` as the main file.
4. Deploy. On first launch the app builds the processed CSV from the included source data; it does not need secrets or an external service.

If data or assumptions change, run `python scripts/build_assets.py` locally to regenerate the Tableau-ready exports. The generated CSV/JSON files are excluded from Git; the app rebuilds them when it starts.

The dashboard is an educational aggregate analysis of fictional data. A public app should retain the source attribution and limitations shown in its **About this analysis** section.
