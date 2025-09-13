import streamlit as st
from openai import OpenAI

# -------------------
# Setup
# -------------------
st.set_page_config(page_title="Funding & Scholarship Finder", page_icon="💰", layout="wide")
st.title("💡 Startup Funding & Scholarship Finder")

# Instructions
st.write("""
Welcome to Operations Sync.
Enter your information below, and this tool will generate a report of possible **organizations, funds, and scholarships**  
available for startups and businesses in your city and country.
""")

# -------------------
# Input Form
# -------------------
with st.form("input_form"):
    name = st.text_input("Your Name (optional):")
    city = st.text_input("City you live in:")
    country = st.text_input("Country you live in:")
    business_type = st.selectbox("Business/Startup Type:", [
        "Technology",
        "Retail",
        "Education",
        "Healthcare",
        "Agriculture",
        "Other"
    ])
    stage = st.radio("Stage of your business:", ["Idea", "Early Stage", "Growth", "Established"])
    need = st.multiselect("What kind of support are you looking for?", [
        "Funding",
        "Scholarship",
        "Mentorship",
        "Incubation/Accelerator",
        "Government Grants"
    ])
    submitted = st.form_submit_button("🔍 Find Opportunities")

# -------------------
# Backend Processing
# -------------------
if submitted:
    if city and country and business_type:
        with st.spinner("Generating your report... Please wait ⏳"):
            # Connect to OpenAI
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

            # Build prompt
            prompt = f"""
            The user is located in {city}, {country}.
            Their business type is {business_type}, and stage is {stage}.
            They are looking for: {", ".join(need)}.
            
            Please generate a detailed report of possible:
            - Government grants
            - Private funds
            - Scholarships
            - Local organizations
            - International opportunities
            
            Focus only on relevant programs available in {country}, and preferably in {city}.
            Present the output in a structured, easy-to-read format with bullet points and sections.
            """

            # Call ChatGPT
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=700
            )

            result = response.choices[0].message.content

        # -------------------
        # Output Report
        # -------------------
        st.success("✅ Report Generated!")
        st.subheader("📑 Funding & Scholarship Opportunities Report")
        st.write(result)

        # Option to download report
        st.download_button(
            label="📥 Download Report",
            data=result,
            file_name=f"funding_report_{city}_{country}.txt",
            mime="text/plain"
        )
    else:
        st.error("❌ Please fill at least City, Country, and Business Type.")
