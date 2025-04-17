try:
    import streamlit as st
    import json
    import pandas as pd
    import matplotlib.pyplot as plt
except ModuleNotFoundError as e:
    print("This script requires the 'streamlit' module. Please install it using 'pip install streamlit' and run it locally.")
    raise e

# Load patient data
st.set_page_config(page_title="Nature & Nurture: Genomic Wellness Report", layout="wide")
st.markdown("""
    <style>
    .block-container {
        background-color: #f4f9f4;
        background-image: url('https://images.unsplash.com/photo-1508780709619-79562169bc64?auto=format&fit=crop&w=1350&q=80');
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        color: #2f4f4f;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌳 Nature & Nurture: Genomic Wellness Report")

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

    tabs = st.tabs(["👤 Profile", "🧠 Behavior", "🧬 Genomics", "📌 Summary"])

    with tabs[0]:
        st.header("Patient Profile")
        info = data["patient_info"]
        st.markdown("""
            #### How to talk about this with your child:
            This test helps us understand how your child’s brain and body work — not to label them, but to love them better. 
            You might say, *“We’re learning what your body might need to feel better and be strong — just like a map to help us understand what works best for you.”*
        """)
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

    with tabs[1]:
        st.header("Behavioral Trait Summary")
        b_scores = data["behavioral_scores"]
        b_df = pd.DataFrame.from_dict(b_scores, orient='index', columns=['Score'])
        st.bar_chart(b_df)

        for trait, score in b_scores.items():
            st.success(f"**{trait}**: {score}", icon="🧩")

    with tabs[2]:
        st.header("Genomic Results")
        gene_df = pd.DataFrame(data["genomic_results"])
        st.dataframe(gene_df, use_container_width=True)

    with tabs[3]:
        st.header("Genes with Clinical Significance")
        sig_genes = gene_df[(gene_df['Genotype'].str.contains("T") | gene_df['Methylation_Status'] != "-")]['Gene'].unique().tolist()
        if sig_genes:
            st.markdown("#### The following genes may play a role in emotional or nutritional resilience:")
            for gene in sig_genes:
                st.markdown(f"✅ **{gene}**", unsafe_allow_html=True)
        else:
            st.info("No clinically significant variants detected.")

        st.markdown("---")
        st.markdown("This information is intended to guide personalized care, not to diagnose. Always consult a licensed provider for interpretation and planning.")

        if st.button("📤 Share with your clinician or download"):
            st.markdown("Coming soon: Export to PDF or email integration.")
