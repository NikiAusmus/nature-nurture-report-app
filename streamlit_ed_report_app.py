# This script is intended to be run using Streamlit locally or in Streamlit Cloud.
# To run locally: save as `streamlit_ed_report_app.py` and execute `streamlit run streamlit_ed_report_app.py`

try:
    import streamlit as st
    import json
    import pandas as pd
    import matplotlib.pyplot as plt
except ModuleNotFoundError as e:
    print("This script requires the 'streamlit' module. Please install it using 'pip install streamlit' and run it locally.")
    raise e

# Load patient data
st.set_page_config(page_title="Nature & Nurture: Patient Report", layout="centered")
st.title("🧬 Personalized Genomic & Behavioral Report")

uploaded_file = st.file_uploader("Upload patient JSON file", type="json")
if uploaded_file:
    import io
    try:
        data = json.load(io.StringIO(uploaded_file.getvalue().decode("utf-8")))
    except Exception as e:
        st.error("There was a problem reading the file. Please upload a valid JSON.")
        st.stop()

    # Display patient info
    st.subheader("Patient Summary")
    info = data["patient_info"]
    st.markdown(f"**Name:** {info['Name']}  ")
    st.markdown(f"**Age:** {info['Age']}  |  **Sex:** {info['Sex']}")
    st.markdown(f"**Family History of ED:** {info['Family_History_ED']}  |  **Prior ED Diagnosis:** {info['Prior_ED_Diagnosis']}")

    # Show behavioral scores
    st.subheader("🧠 Behavioral Disposition")
    b_scores = data["behavioral_scores"]
    b_df = pd.DataFrame.from_dict(b_scores, orient='index', columns=['Score'])
    st.bar_chart(b_df)

    # Genomic results
    st.subheader("🧬 Genomic Markers")
    gene_df = pd.DataFrame(data["genomic_results"])
    st.dataframe(gene_df, use_container_width=True)

    # Highlight significant variants
    sig_genes = gene_df[(gene_df['Genotype'].str.contains("T") | gene_df['Methylation_Status'] != "-")]['Gene'].unique().tolist()
    if sig_genes:
        st.markdown("### 📌 Genes with Clinical Significance:")
        st.write(", ".join(sig_genes))
    else:
        st.info("No clinically
