import streamlit as st
import google.generativeai as genai
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

## logo
col1, col2, col3 = st.columns([1,3,1])
with col2:
    st.image("logo.png", width=400)

# Configure Gemini API
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

st.title("The Mission Funding Accelerator")

st.markdown(
    """
    <h3 style="text-align: center;">
        <b>Stop Searching, Start Impacting. Unlock Your Next Funding Opportunity.</b>
    </h3>
    """,
    unsafe_allow_html=True
)

st.caption("A complimentary tool from Operations.Sync — We help you Simplify & Accelerate Your Operations and Redeem your Time: automate what you can, humanize what you must.")

st.write("Our AI scans hundreds of funds and grants to find the perfect match for your mission. Answer a few questions below to get a personalized report in minutes.")

# ---------------- Collect Customer Info ----------------
st.header("Customer & Startup Information")
organization_name = st.text_input("Tell Us About Your Organization")
primary_focus = st.selectbox("Primary Focus", [...])  # same as your previous list
minority_status = st.multiselect("Serving Minority / Underrepresented Group Status", [...])
racialized_group = st.multiselect("Racialized Group", [...])
city = st.text_input("City")
country = st.text_input("Country")
age_company = st.number_input("Age of Organization / Year Founded or to be Launched", min_value=0, max_value=200, step=1)
education = st.text_input("Educational background of founder(s)")
business_status = st.multiselect("Business Registration Status", [...])
team_members = st.multiselect("Number of Team Members (including volunteers)", [...])
annual_budget = st.multiselect("Annual Operating Budget", [...])
annual_revenue = st.multiselect("Annual Revenue", [...])
primary_need = st.multiselect("Primary Business Need", [...])
business_type = st.selectbox("Type of business", ["Tech-based", "Research-based", "Traditional"])
website = st.text_input("Company Website (optional)")

st.header("Upload Supporting Text")
uploaded_summary = ""
uploaded_file = st.file_uploader("Upload a text file (CV, website content, etc.)", type=["txt"])
if uploaded_file is not None:
    text_content = uploaded_file.read().decode("utf-8")
    prompt_extract = f"Analyze the following text and extract the 10 most important points:\n{text_content}"
    try:
        response_extract = model.generate_content(prompt_extract)
        uploaded_summary = response_extract.text
        st.subheader("Extracted 10 Key Points from Uploaded Text")
        st.write(uploaded_summary)
    except Exception as e:
        st.error(f"Error extracting information: {e}")

st.header("Where should we send your report?")
your_name = st.text_input("Your Name")
your_email = st.text_input("Your Email")
your_phone = st.text_input("Your Phone Number")
founder_name = st.text_input("Founder’s Name")
founder_education = st.selectbox("Founder's Education", ["High School", "Bachelor's Degree", "Master's Degree", "PhD", "Trade Certification"])
consent = st.checkbox("I agree to receive this report and occasional insights from Operations.Sync.")

# ---------------- Generate Report ----------------
if st.button("Generate Funding Report"):
    if not city or not country:
        st.error("Please provide at least city and country to continue.")
    elif not consent:
        st.error("You must agree to receive the report before generating it.")
    else:
        # Build AI prompt
        prompt = f"""
        The startup is located in {city}, {country}.
        Age of company: {age_company} years.
        Educational background of founders: {education}.
        Minority / underrepresented status: {', '.join(minority_status) if minority_status else 'N/A'}.
        Racialized group / other: {', '.join(racialized_group) if racialized_group else 'N/A'}.
        Business registration: {', '.join(business_status) if business_status else 'N/A'}.
        Team size: {', '.join(team_members) if team_members else 'N/A'}.
        Annual operating budget: {', '.join(annual_budget) if annual_budget else 'N/A'}.
        Annual revenue: {', '.join(annual_revenue) if annual_revenue else 'N/A'}.
        Primary business need: {', '.join(primary_need) if primary_need else 'N/A'}.
        Type of business: {business_type}.
        Website: {website if website else 'N/A'}.
        Additional supporting details: {uploaded_summary if uploaded_summary else 'N/A'}.

        Task:
        1. Find and list 20 possible grants, scholarships, or funds available.
        2. For each, provide:
           - Name of the organization providing the fund
           - Website link to apply
           - Upcoming application deadline
           - Estimated probability (0–100%) of winning
        3. At the end of the report, summarize the Top 3 most promising funds.
        """

        try:
            with st.spinner("Generating report..."):
                response = model.generate_content(prompt)
                report_text = response.text

            # Append customer info at the end of report
            customer_info = f"""
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
            st.write(full_report)

            # Export to PDF
            buffer = io.BytesIO()
            pdf = canvas.Canvas(buffer, pagesize=letter)
            pdf.setFont("Helvetica", 10)
            text_object = pdf.beginText(40, 750)
            for line in full_report.split("\n"):
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
