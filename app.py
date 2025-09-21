import streamlit as st
import google.generativeai as genai
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import streamlit as st

## logo
col1, col2, col3 = st.columns([1,3,1])  # middle column is bigger
with col2:
    st.image("logo.png", width=400)





# Configure Gemini API
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

st.title("The Mission Funding Accelerator")
# st.markdown("**Stop Searching, Start Impacting. Unlock Your Next Funding Opportunity.**")

st.markdown(
    """
    <h3 style="text-align: center;">
        <b>Stop Searching, Start Impacting. Unlock Your Next Funding Opportunity.</b>
    </h3>
    """,
    unsafe_allow_html=True
)

st.caption("A complimentary tool from Operations.Sync — We helpyou Simplify & Accelerate Your Operations and Redeem your Time: automatewhat you can, humanize what you must.")

st.write("Our AI scans hundreds of funds and grants to find the perfect match for your mission. Answer a few questions below to get a personalized report in minutes, get a curated list of opportunities perfectly matched to your mission and get back to the workthat matters.")

    
# Collect customer information
st.header("Customer & Startup Information")

city = st.text_input("City")
country = st.text_input("Country")
age_company = st.number_input("Age of the company (in years)", min_value=0, max_value=200, step=1)
education = st.text_input("Educational background of founder(s)")
minority_status = st.selectbox("Minority / underrepresented group status?", ["Yes", "No", "Prefer not to say"])
business_registration = st.selectbox("Business registration status", ["Registered", "Not Registered"])
num_employees = st.number_input("Number of employees", min_value=0, step=1)
annual_revenue = st.number_input("Annual revenue (USD)", min_value=0, step=1000)
primary_need = st.text_area("Primary business need (funding, networking, research, etc.)")
business_type = st.selectbox("Type of business", ["Tech-based", "Research-based", "Traditional"])
website = st.text_input("Company Website (optional)")

# Section: Upload supporting text (CV, Website content, etc.)
st.header("Upload Supporting Text")
uploaded_summary = ""
uploaded_file = st.file_uploader("Upload a text file (CV, website content, etc.)", type=["txt"])

if uploaded_file is not None:
    text_content = uploaded_file.read().decode("utf-8")

    prompt_extract = f"""
    Analyze the following text and extract the 10 most important points 
    (skills, achievements, business strengths, unique advantages, etc.):

    {text_content}
    """

    try:
        response_extract = model.generate_content(prompt_extract)
        uploaded_summary = response_extract.text
        st.subheader("Extracted 10 Key Points from Uploaded Text")
        st.write(uploaded_summary)
    except Exception as e:
        st.error(f"Error extracting information: {e}")

# Button to generate report
if st.button("Generate Funding Report"):
    if not city or not country:
        st.error("Please provide at least city and country to continue.")
    else:
        # Build the funding search prompt
        prompt = f"""
        The startup is located in {city}, {country}.
        Age of company: {age_company} years.
        Educational background of founders: {education}.
        Minority / underrepresented status: {minority_status}.
        Business registration: {business_registration}.
        Employees: {num_employees}.
        Annual revenue: {annual_revenue} USD.
        Primary business need: {primary_need}.
        Type of business: {business_type}.
        Website: {website if website else "N/A"}.

        Additional supporting details from uploaded text (if any): {uploaded_summary}

        Task:
        1. List at least 3 possible grants, scholarships, or funds available.
        2. For each, describe why the company might be eligible.
        3. Estimate the probability (0–100%) of winning each grant based on provided data.
        4. Provide advice to improve chances.
        """

        try:
            response = model.generate_content(prompt)
            report_text = response.text
            st.subheader("Funding Report")
            st.write(report_text)

            # Export to PDF
            buffer = io.BytesIO()
            pdf = canvas.Canvas(buffer, pagesize=letter)
            pdf.setFont("Helvetica", 10)
            text_object = pdf.beginText(40, 750)
            for line in report_text.split("\n"):
                text_object.textLine(line)
            pdf.drawText(text_object)
            pdf.save()

            buffer.seek(0)
            st.download_button(
                label="Download Report as PDF",
                data=buffer,
                file_name="funding_report.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Error generating report: {e}")
