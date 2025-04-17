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

# Scripture rotation - gentle encouragement
import random
scriptures = [
    "I praise You because I am fearfully and wonderfully made. – Psalm 139:14",
    "The Lord is near to the brokenhearted and saves the crushed in spirit. – Psalm 34:18",
    "For I know the plans I have for you, declares the Lord. – Jeremiah 29:11",
    "Come to me, all who are weary and burdened, and I will give you rest. – Matthew 11:28",
    "When I am weak, then I am strong. – 2 Corinthians 12:10"
]
st.caption(random.choice(scriptures))

uploaded_file = st.file_uploader("Upload patient JSON file", type="json")
if uploaded_file:
    import io
    try:
        data = json.load(io.StringIO(uploaded_file.getvalue().decode("utf-8")))
    except Exception as e:
        st.error("There was a problem reading the file. Please upload a valid JSON.")
        st.stop()

    # Display patient info
    st.markdown("### 👤 Patient Profile")
    info = data["patient_info"]
    st.info(
        f"""
        **Name**: {info['Name']}  
        **Age**: {info['Age']}  
        **Sex**: {info['Sex']}  
        **Family History of ED**: {info['Family_History_ED']}  
        **Prior ED Diagnosis**: {info['Prior_ED_Diagnosis']}
        """,
        icon="👨‍👩‍👧"
    )

    # Show behavioral scores
    st.markdown("### 🧠 Behavioral Trait Summary")
    b_scores = data["behavioral_scores"]
    b_df = pd.DataFrame.from_dict(b_scores, orient='index', columns=['Score'])
    st.bar_chart(b_df)

    for trait, score in b_scores.items():
        st.success(f"**{trait}**: {score}", icon="🧩")

    # Genomic results
    st.markdown("### 🧬 Genomic Results")
    gene_df = pd.DataFrame(data["genomic_results"])
    st.dataframe(gene_df, use_container_width=True)

    # Highlight significant variants
    st.markdown("### 📌 Genes with Clinical Significance")
    sig_genes = gene_df[(gene_df['Genotype'].str.contains("T") | gene_df['Methylation_Status'] != "-")]['Gene'].unique().tolist()
    if sig_genes:
        for gene in sig_genes:
            st.markdown(f"✅ **{gene}**", unsafe_allow_html=True)
    else:
        st.info("No clinically significant variants detected.")

    # Download section (placeholder)
    if st.button("📤 Share with your clinician or download"):
        st.markdown("Coming soon: Export to PDF or email integration.")
   
