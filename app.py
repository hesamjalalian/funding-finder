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

organization_name = st.text_input("Tell Us About Your Organization")

primary_focus = st.selectbox(
    "Primary Focus",
    [
        "Agriculture: Cultivation, livestock farming, fishing, forestry",
        "Industry / Manufacturing: Production of goods, heavy and light manufacturing",
        "Services (General): Trade, logistics, transportation, consulting, business support, legal, accounting",
        "Governmental / Para-Governmental Organizations: Public administration, municipal/provincial/federal agencies, crown corporations",
        "Health Services: Hospitals, clinics, medical practices, mental health therapy, medical research",
        "Community & Social Services: Food banks, shelters, youth programs, senior support, social advocacy",
        "Education: Schools, universities, vocational training, adult learning",
        "IT and Technology: Software development, IT consulting, online platforms, telecommunications",
        "Finance: Banking, insurance, investment, FinTech",
        "Energy: Electricity, gas, oil, renewable energy",
        "Media and Communication: TV, radio, journalism, publishing, PR, advertising",
        "Arts & Culture: Museums, galleries, theaters, performing arts, heritage",
        "Tourism and Hospitality: Hotels, restaurants, travel agencies, event management",
        "Construction: Building construction, infrastructure development, real estate",
        "Retail: Sales of goods (clothing, groceries, electronics)",
        "Non-Governmental Organizations (NGOs): Humanitarian aid, development, environment, human rights",
        "Religious Organizations: Churches, mosques, temples, synagogues, faith-based initiatives",
        "Mission-Driven Startups / Innovative Businesses: Social/environmental impact + innovative models",
        "Social Enterprise: Businesses with a social/environmental mission reinvesting profits",
        "Sustainability / Environmental: Conservation, climate action, sustainable development, eco-advocacy",
        "Research & Development: Academic, corporate, or independent research institutions",
        "Other (please specify)"
    ]
)
minority_status = st.multiselect(
    "Serving Minority / Underrepresented Group Status",
    [
        "Indigenous Peoples / Aboriginal Peoples: First Nations, Inuit, or Métis (as per Canadian legal definitions of 'Aboriginal peoples')",
        "Persons with Disabilities: Individuals with long-term or recurring physical, mental, sensory, psychiatric, or learning impairments",
        "LGBTQ2+ Individuals: Lesbian, Gay, Bisexual, Transgender, Queer, Two-Spirit, or other diverse sexual orientations and gender identities",
        "Other (please specify)"
    ]
)
racialized_group = st.multiselect(
    "Racialized Group (select all that apply, or specify):",
    [
        "South Asian",
        "Chinese",
        "Black",
        "Filipino",
        "Arab",
        "Latin American",
        "Southeast Asian",
        "West Asian",
        "Korean",
        "Japanese",
        "Another racialized population group",
        "Women / Girls",
        "Youth (Ages 16-29)",
        "Seniors (Ages 65+)",
        "Low-Income / Economically Disadvantaged Individuals",
        "Newcomers / Immigrants / Refugees",
        "None of the above / Not applicable"
    ]
)
city = st.text_input("City")
country = st.text_input("Country")
age_company = st.number_input("Age of Organization / Year Founded or to be Launched)", min_value=0, max_value=200, step=1)
education = st.text_input("Educational background of founder(s)")
minority_status = st.selectbox("Minority / underrepresented group status?", ["Yes", "No", "Prefer not to say"])
business_registration = st.selectbox("Business registration status", ["Registered", "Not Registered"])
# num_employees = st.number_input("Number of employees", min_value=0, step=1)
st.subheader("Number of Team Members (including volunteers)")

team_size = st.slider(
    "Select the number of people in your organization:",
    min_value=1,
    max_value=100,
    value=1,
    step=1
)

# Map the numeric slider to categories
if team_size == 1:
    team_category = "Solo entrepreneur (self-employed / freelancer)"
elif 2 <= team_size <= 5:
    team_category = "2 to 5"
elif 6 <= team_size <= 10:
    team_category = "5 to 10"
elif 11 <= team_size <= 50:
    team_category = "10 to 50"
else:
    team_category = "More than 50"

st.write(f"**Selected Team Size:** {team_category}")
# annual_revenue = st.number_input("Annual revenue (USD)", min_value=0, step=1000)
st.subheader("Annual Revenue")

annual_revenue = st.multiselect(
    "Select your organization's approximate annual revenue:",
    [
        "$0 - $50k",
        "$50k - $250k",
        "$250k - $1M",
        "$1M+",
        "Other (please specify)"
    ]
)
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
