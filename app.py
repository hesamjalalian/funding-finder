import streamlit as st
import google.generativeai as genai
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import streamlit as st


st.markdown("<h5 style='text-align: center;'>O.S ©</h5>", unsafe_allow_html=True)

## logo
col1, col2, col3 = st.columns([1,3,1])  # middle column is bigger
with col2:
    st.image("logo.png", width=400)


###


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

st.caption("A complimentary tool from Operations.Sync — We help you Simplify & Accelerate Your Operations and Redeem your Time: automate what you can, humanize what you must.")

st.write("Our AI scans hundreds of funds and grants to find the perfect match for your mission. Answer a few questions below to get a personalized report in minutes, get a curated list of opportunities perfectly matched to your mission and get back to the work that matters.")

    
# Collect customer information
st.header("Tell Us About Your Organization")

organization_name = st.text_input("Enter your organization name")

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

# text input in the case of selecting other
if primary_focus == "Other (please specify)":
    primary_focus_other = st.text_input("Please specify your organization's primary focus")
    if primary_focus_other:
        primary_focus = primary_focus_other
        
minority_status = st.multiselect(
    "Serving Minority / Underrepresented Group Status (select all that apply)",
    [
        "Indigenous Peoples / Aboriginal Peoples: Individuals identifying as First Nations, Inuit, or Métis (as per Canadian legal definitions of 'Aboriginal peoples').",
        "Persons with Disabilities: Individuals with a long-term or recurring physical, mental, sensory, psychiatric, or learning impairment, including those whose functional limitations have been accommodated in their work or daily life.",
        "LGBTQ2+ Individuals: Persons identifying as Lesbian, Gay, Bisexual, Transgender, Queer, Two-Spirit, or other diverse sexual orientations and gender identities.",
        "Women / Girls",
        "Youth (Ages 16-29)",
        "Seniors (Ages 65+)",
        "Low-Income / Economically Disadvantaged Individuals",
        "Newcomers / Immigrants / Refugees",
        "None of the above / Not applicable"
    ]
)
racialized_group = st.multiselect(
    "Racialized Group (select all that apply)",
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
        "Another racialized population group"
    ]
)

# If user selects "Another racialized population group", show a text box
other_racialized = ""
if "Another racialized population group" in racialized_group:
    other_racialized = st.text_input("Please specify another racialized group:")

# Final formatted output
racialized_info = ", ".join(racialized_group)
if other_racialized:
    racialized_info += f" (Specified: {other_racialized})"
city = st.text_input("City")
province = st.text_input("Province / State")
country = st.text_input("Country")
age_company = st.number_input("Age of Organization / Year Founded or to be Launched)", min_value=0, max_value=200, step=1)
team_members = st.multiselect(
    "Number of Team Members (including volunteers)",
    [
        "Solo entrepreneur (self-employed / freelancer)",
        "2 to 5",
        "5 to 10",
        "10 to 50",
        "More than 50"
    ]
)

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
annual_budget = st.multiselect(
    "Annual Operating Budget",
    [
        "$0 - $50k",
        "$50k - $250k",
        "$250k - $1M",
        "$1M+"
    ]
)
business_status = st.multiselect(
    "Select your business registration status:",
    [
        "Not yet registered / Informal Group",
        "Sole Proprietorship / Auto-entreprise",
        "Partnership (General or Limited)",
        "Limited Liability Company (LLC) / Société à Responsabilité Limitée (SARL)",
        "For-Profit Corporation / Société par Actions",
        "Non-Profit Organization / Organisme à But Non Lucratif (OBNL)",
        "Registered Charity / Organisme de Bienfaisance Enregistré",
        "Cooperative / Coopérative",
        "Other (please specify)"
    ]
)
website = st.text_input("Organization Website (Optional)")

st.subheader("Describe Your Mission & Impact")


education = st.text_input("Educational background of founder(s)")
# minority_status = st.selectbox("Minority / underrepresented group status?", ["Yes", "No", "Prefer not to say"])
# st.subheader("Business Registration Status")
# num_employees = st.number_input("Number of employees", min_value=0, step=1)

primary_community = st.multiselect(
    "Primary Community You Serve",
    [
        "Youth & Young Adults",
        "Seniors",
        "Newcomers & Immigrants",
        "Low-Income Families",
        "Indigenous Communities",
        "General Public",
        "Other (please specify)"
    ]
)

funding_purpose = st.selectbox(
    "What will this funding primarily support?",
    [
        "Operational Costs (General Support)",
        "A Specific Program or Project",
        "Capacity Building (Hiring, Training)",
        "Capital Projects (Buildings, Equipment)"
    ]
)

primary_need = st.multiselect(
    "Primary Business Need",
    [
        "Grant Funding",
        "Operational Support",
        "Project-Specific Funding",
        "Networking",
        "Mentorship",
        "Other (please specify)"
    ]
)

# Show a text input if "Other" is selected
other_primary_need = ""
if "Other (please specify)" in primary_need:
    other_primary_need = st.text_input("Please specify your primary business need")



# Section: Upload supporting text (CV, Website content, etc.)
# st.header("Upload Supporting Text")
# uploaded_summary = ""
# uploaded_file = st.file_uploader("Upload a text file (CV, website content, etc.)", type=["txt"])

st.header("Upload Supporting Text")

st.write(
    "Upload a Business Plan, Business Model, or any relevant documentation "
    "about your organization such as a description from your 'About Us' page, "
    "a recent newsletter, or a project summary. The more detail, the better our AI "
    "can match you with the right funders. This is much easier and achieves the same goal."
)

uploaded_summary = ""
uploaded_file = st.file_uploader(
    "Upload a text file (CV, website content, etc.)", 
    type=["txt"]
)

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

st.header("Where should we send your report?")

# Contact information
your_name = st.text_input("Your Name")
your_email = st.text_input("Your Email")
your_phone = st.text_input("Your Phone Number")  # You can validate later for numbers
founder_name = st.text_input("Founder’s Name")

# Founder's education
founder_education = st.selectbox(
    "Founder's Education",
    [
        "High School",
        "Bachelor's Degree",
        "Master's Degree",
        "PhD",
        "Trade Certification"
    ]
)

# Consent checkbox
consent = st.checkbox("I agree to receive this report and occasional insights from Operations.Sync.")

# # Button to generate report
# if st.button("Generate Funding Report"):
#     if not city or not country:
#         st.error("Please provide at least city and country to continue.")
#     elif not consent:
#         st.error("You must agree to receive the report before generating it.")
#     else:
#         # Build the funding search prompt with all collected data
#         prompt = f"""
#         The startup is located in {city}, {country}.
#         Age of company: {age_company} years.
#         Educational background of founders: {education}.
#         Minority / underrepresented status: {', '.join(minority_status) if minority_status else 'N/A'}.
#         Racialized group / other: {', '.join(racialized_group) if racialized_group else 'N/A'}.
#         Business registration: {', '.join(business_status) if business_status else 'N/A'}.
#         Team size: {', '.join(team_members) if team_members else 'N/A'}.
#         Annual operating budget: {', '.join(annual_budget) if annual_budget else 'N/A'}.
#         Annual revenue: {', '.join(annual_revenue) if annual_revenue else 'N/A'}.
#         Primary business need: {', '.join(primary_need) if primary_need else 'N/A'}.
#         Type of business: {business_type}.
#         Website: {website if website else 'N/A'}.
#         Additional supporting details from uploaded text (if any): {uploaded_summary if uploaded_summary else 'N/A'}.

#         Task:
#         1. List at least 3 possible grants, scholarships, or funds available.
#         2. For each, provide:
#            - Name of the fund
#            - Direct link/URL to apply
#            - Why the company might be eligible
#            - Estimated probability (0–100%) of winning based on provided data
#            - Advice to improve chances
#         """

#         try:
#             # Show progress spinner while generating report
#             with st.spinner("Analyzing the data..."):
#                 response = model.generate_content(prompt)
#                 report_text = response.text

#             st.subheader("Funding Report")
#             st.write(report_text)

#             # Export to PDF
#             buffer = io.BytesIO()
#             pdf = canvas.Canvas(buffer, pagesize=letter)
#             pdf.setFont("Helvetica", 10)
#             text_object = pdf.beginText(40, 750)
#             for line in report_text.split("\n"):
#                 text_object.textLine(line)
#             pdf.drawText(text_object)
#             pdf.save()

#             buffer.seek(0)
#             st.download_button(
#                 label="Download Report as PDF",
#                 data=buffer,
#                 file_name="funding_report.pdf",
#                 mime="application/pdf"
#             )
#         except Exception as e:
#             st.error(f"Error generating report: {e}")

# # ---------------- Generate Report ----------------
# if st.button("Generate Funding Report"):
#     if not city or not country:
#         st.error("Please provide at least city and country to continue.")
#     elif not consent:
#         st.error("You must agree to receive the report before generating it.")
#     else:
#         # Build AI prompt
#         prompt = f"""
#         The startup is located in {city}, {country}.
#         Age of company: {age_company} years.
#         Educational background of founders: {education}.
#         Minority / underrepresented status: {', '.join(minority_status) if minority_status else 'N/A'}.
#         Racialized group / other: {', '.join(racialized_group) if racialized_group else 'N/A'}.
#         Business registration: {', '.join(business_status) if business_status else 'N/A'}.
#         Team size: {', '.join(team_members) if team_members else 'N/A'}.
#         Annual operating budget: {', '.join(annual_budget) if annual_budget else 'N/A'}.
#         Annual revenue: {', '.join(annual_revenue) if annual_revenue else 'N/A'}.
#         Primary business need: {', '.join(primary_need) if primary_need else 'N/A'}.
#         Type of business: {business_type}.
#         Website: {website if website else 'N/A'}.
#         Additional supporting details: {uploaded_summary if uploaded_summary else 'N/A'}.

#         Task:
#         1. Find and list 20 possible grants, scholarships, or funds available.
#         2. For each, provide:
#            - Name of the organization providing the fund
#            - Website link to apply
#            - Upcoming application deadline
#            - Estimated probability (0–100%) of winning
#         3. At the end of the report, summarize the Top 3 most promising funds.
#         """

#         try:
#             with st.spinner("Generating report..."):
#                 response = model.generate_content(prompt)
#                 report_text = response.text

#             # Append customer info at the end of report
#             customer_info = f"""
# -------------------------------
# Customer Information

# Name: {your_name}
# Email: {your_email}
# Phone: {your_phone}
# Organization: {organization_name}
# Founder: {founder_name}
# Founder's Education: {founder_education}
# City: {city}
# Country: {country}
# Age of Organization: {age_company} years
# Education: {education}
# Minority Status: {', '.join(minority_status) if minority_status else 'N/A'}
# Racialized Group: {', '.join(racialized_group) if racialized_group else 'N/A'}
# Business Registration: {', '.join(business_status) if business_status else 'N/A'}
# Team Members: {', '.join(team_members) if team_members else 'N/A'}
# Annual Operating Budget: {', '.join(annual_budget) if annual_budget else 'N/A'}
# Annual Revenue: {', '.join(annual_revenue) if annual_revenue else 'N/A'}
# Primary Business Need: {', '.join(primary_need) if primary_need else 'N/A'}
# Type of Business: {business_type}
# Website: {website if website else 'N/A'}
# """
#             full_report = report_text + "\n\n" + customer_info

#             # Display on Streamlit
#             st.subheader("Funding Report")
#             st.write(full_report)

#             # Export to PDF
#             buffer = io.BytesIO()
#             pdf = canvas.Canvas(buffer, pagesize=letter)
#             pdf.setFont("Helvetica", 10)
#             text_object = pdf.beginText(40, 750)
#             for line in full_report.split("\n"):
#                 text_object.textLine(line)
#             pdf.drawText(text_object)
#             pdf.save()
#             buffer.seek(0)

#             st.download_button(
#                 label="Download Full Report as PDF",
#                 data=buffer,
#                 file_name=f"{your_name}_funding_report.pdf",
#                 mime="application/pdf"
#             )

#         except Exception as e:
#             st.error(f"Error generating report: {e}")


# ---------------- Generate Report ----------------
if st.button("Generate Funding Report"):
    # Basic validation
    if not city or not country:
        st.error("Please provide at least city and country to continue.")
    elif not consent:
        st.error("You must agree to receive the report before generating it.")
    else:
        # Handle "Other" inputs
        if "Other (please specify)" in primary_need and other_primary_need:
            primary_need = [n for n in primary_need if n != "Other (please specify)"] + [other_primary_need]

        if "Another racialized population group" in racialized_group and other_racialized:
            racialized_info = ", ".join([r for r in racialized_group if r != "Another racialized population group"]) + f", {other_racialized}"
        else:
            racialized_info = ", ".join(racialized_group) if racialized_group else "N/A"

        if primary_focus == "Other (please specify)" and primary_focus_other:
            primary_focus_final = primary_focus_other
        else:
            primary_focus_final = primary_focus

        # Build AI prompt
        prompt = f"""
        The startup is located in {city}, {province}, {country}.
        Age of company: {age_company} years.
        Educational background of founders: {education}.
        Minority / underrepresented status: {', '.join(minority_status) if minority_status else 'N/A'}.
        Racialized group / other: {racialized_info}.
        Business registration: {', '.join(business_status) if business_status else 'N/A'}.
        Team size: {', '.join(team_members) if team_members else 'N/A'}.
        Annual operating budget: {', '.join(annual_budget) if annual_budget else 'N/A'}.
        Annual revenue: {', '.join(annual_revenue) if annual_revenue else 'N/A'}.
        Primary business need: {', '.join(primary_need) if primary_need else 'N/A'}.
        Type of business: {business_type if 'business_type' in locals() else 'N/A'}.
        Website: {website if website else 'N/A'}.
        Primary Focus: {primary_focus_final}.
        Additional supporting details: {uploaded_summary if uploaded_summary else 'N/A'}.

        Task:
        Provide 20 funding opportunities for this startup. 
        Format the response in 20 numbered paragraphs. 
        For each paragraph:
        1. Name of the organization providing the fund
        2. Link to the website
        3. Short explanation why this fund fits the startup
        """

        try:
            with st.spinner("Generating report..."):
                response = model.generate_content(prompt)
                report_text = response.text

            # Append customer info at the end
            customer_info = f"""


# if st.button("Generate Funding Report"):
#     if not city or not country:
#         st.error("Please provide at least city and country to continue.")
#     elif not consent:
#         st.error("You must agree to receive the report before generating it.")
#     else:
#         # Build AI prompt
#         prompt = f"""
#         The startup is located in {city}, {country}.
#         Age of company: {age_company} years.
#         Educational background of founders: {education}.
#         Minority / underrepresented status: {', '.join(minority_status) if minority_status else 'N/A'}.
#         Racialized group / other: {', '.join(racialized_group) if racialized_group else 'N/A'}.
#         Business registration: {', '.join(business_status) if business_status else 'N/A'}.
#         Team size: {', '.join(team_members) if team_members else 'N/A'}.
#         Annual operating budget: {', '.join(annual_budget) if annual_budget else 'N/A'}.
#         Annual revenue: {', '.join(annual_revenue) if annual_revenue else 'N/A'}.
#         Primary business need: {', '.join(primary_need) if primary_need else 'N/A'}.
#         Type of business: {business_type}.
#         Website: {website if website else 'N/A'}.
#         Additional supporting details: {uploaded_summary if uploaded_summary else 'N/A'}.

#         Task:
#         Provide 20 funding opportunities for this startup. 
#         Format the response in 20 numbered paragraphs. 
#         For each paragraph:
#         1. Name of the organization providing the fund
#         2. Link to the website
#         3. Short explanation why this fund fits the startup
#         """

#         try:
#             with st.spinner("Generating report..."):
#                 response = model.generate_content(prompt)
#                 report_text = response.text

#             # Append customer info at the end
#             customer_info = f"""
-------------------------------
Customer Information

Name: {your_name}
Email: {your_email}
Phone: {your_phone}
Organization: {organization_name}
Founder: {founder_name}
Founder's Education: {founder_education}
City: {city}
Country: {country}
Age of Organization: {age_company} years
Education: {education}
Minority Status: {', '.join(minority_status) if minority_status else 'N/A'}
Racialized Group: {', '.join(racialized_group) if racialized_group else 'N/A'}
Business Registration: {', '.join(business_status) if business_status else 'N/A'}
Team Members: {', '.join(team_members) if team_members else 'N/A'}
Annual Operating Budget: {', '.join(annual_budget) if annual_budget else 'N/A'}
Annual Revenue: {', '.join(annual_revenue) if annual_revenue else 'N/A'}
Primary Business Need: {', '.join(primary_need) if primary_need else 'N/A'}
Type of Business: {business_type}
Website: {website if website else 'N/A'}
"""
            full_report = report_text + "\n\n" + customer_info

            # Display on Streamlit
            st.subheader("Funding Report")
            # preserve line breaks for readability
            st.markdown(full_report.replace("\n", "  \n"))

            # Export to PDF
            buffer = io.BytesIO()
            pdf = canvas.Canvas(buffer, pagesize=letter)
            pdf.setFont("Helvetica", 10)
            text_object = pdf.beginText(40, 750)
            for line in full_report.split("\n"):
                # Add new page if text reaches bottom
                if text_object.getY() < 50:
                    pdf.drawText(text_object)
                    pdf.showPage()
                    text_object = pdf.beginText(40, 750)
                    text_object.setFont("Helvetica", 10)
                text_object.textLine(line)
            pdf.drawText(text_object)
            pdf.save()
            buffer.seek(0)

            st.download_button(
                label="Download Full Report as PDF",
                data=buffer,
                file_name=f"{your_name}_funding_report.pdf",
                mime="application/pdf"
            )

        except Exception as e:
            st.error(f"Error generating report: {e}")

