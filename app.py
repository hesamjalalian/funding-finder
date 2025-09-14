import streamlit as st
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Select Gemini model (flash = free & fast)
model = genai.GenerativeModel("gemini-1.5-flash")

# Streamlit app
st.set_page_config(page_title="Startup Funding Finder", page_icon="💡", layout="centered")

st.title("💡 Startup Funding Finder")
st.write("Enter customer details to find **funds, organizations, and scholarships** available in their city and country.")

# Input form
with st.form("customer_info"):
    name = st.text_input("Customer Name")
    city = st.text_input("City")
    country = st.text_input("Country")
    business_type = st.text_input("Business Type / Industry")
    stage = st.selectbox("Business Stage", ["Idea", "Prototype", "Early Startup", "Growth", "Established"])
    submit = st.form_submit_button("Find Opportunities 🚀")

# Process input
if submit:
    if not (city and country and business_type):
        st.warning("⚠️ Please fill in at least city, country, and business type.")
    else:
        with st.spinner("🔎 Searching for opportunities..."):
            # Prompt for Gemini
            prompt = f"""
            A customer named {name if name else "N/A"} is based in {city}, {country}.
            They are working in the {business_type} sector and their business stage is {stage}.
            
            Provide a structured report with:
            1. Local organizations that support startups in {city}, {country}.
            2. National and international funds/grants they might be eligible for.
            3. Scholarships or government support programs for entrepreneurs.
            4. Practical next steps they should take.

            Make the response clear, professional, and actionable.
            """

            # Generate response
            response = model.generate_content(prompt)

            # Display result
            st.subheader("📑 Funding & Support Report")
            st.write(response.text)
