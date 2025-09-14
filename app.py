import streamlit as st
import google.generativeai as genai
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

# Configure Gemini API
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Select Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# Streamlit app
st.set_page_config(page_title="Startup Funding Finder", page_icon="💡", layout="centered")

st.title("💡 Startup Funding Finder")
st.write("Enter customer details to find **funds, organizations, and scholarships** available in their city and country.")

# Input form
with st.form("customer_info"):
    name = st.text_input("Customer Name")
    age = st.number_input("Age of Founder(s)", min_value=18, max_value=100, step=1)
    education = st.text_input("Educational Background")
    minority = st.checkbox("Are you part of a minority/underrepresented group?")
    city = st.text_input("City")
    country = st.text_input("Country")
    business_type = st.text_input("Business Type / Industry")
    stage = st.selectbox("Business Stage", ["Idea", "Prototype", "Early Startup", "Growth", "Established"])
    registered = st.selectbox("Business Registration Status", ["Not registered", "Sole proprietorship", "Incorporated"])
    employees = st.number_input("Number of Employees", min_value=0, step=1)
    revenue = st.text_input("Annual Revenue (if any)")
    need = st.text_area("Primary Business Need (e.g., R&D, hiring, equipment)")
    innovation = st.selectbox("Business Type", ["Traditional", "Tech-based", "Research-based"])
    
    submit = st.form_submit_button("Find Opportunities 🚀")

# Process input
if submit:
    if not (city and country and business_type):
        st.warning("⚠️ Please fill in at least city, country, and business type.")
    else:
        with st.spinner("🔎 Searching for opportunities..."):
            # Build prompt
            prompt = f"""
            A customer named {name if name else "N/A"} is based in {city}, {country}.
            They are {age} years old with an educational background in {education}.
            Minority/underrepresented group status: {"Yes" if minority else "No"}.

            Business details:
            - Industry: {business_type}
            - Stage: {stage}
            - Registration: {registered}
            - Employees: {employees}
            - Annual Revenue: {revenue if revenue else "N/A"}
            - Primary Need: {need if need else "N/A"}
            - Innovation Type: {innovation}

            Task:
            1. Provide at least **3 funding opportunities** (local, national, or international).
            2. For each funding opportunity, include:
               - Name and short description
               - Eligibility requirements
               - Amount available
               - Application deadline
               - **Probability of winning based on official website criteria**
               - **Probability of winning based on this customer’s profile**
            3. At the end, provide actionable next steps for the customer.
            Format output clearly with sections and bullet points.
            """

            # Generate response
            response = model.generate_content(prompt)
            funding_report = response.text

            # Display result
            st.subheader("📑 Funding & Support Report")
            st.write(funding_report)

            # ---- Generate PDF ----
            pdf_buffer = io.BytesIO()
            pdf = canvas.Canvas(pdf_buffer, pagesize=letter)
            width, height = letter

            text = pdf.beginText(40, height - 50)
            text.setFont("Helvetica", 10)

            for line in funding_report.split("\n"):
                text.textLine(line)
            pdf.drawText(text)
            pdf.showPage()
            pdf.save()
            pdf_buffer.seek(0)

            # Provide download
            st.download_button(
                label="📥 Download Report as PDF",
                data=pdf_buffer,
                file_name="funding_report.pdf",
                mime="application/pdf",
            )
