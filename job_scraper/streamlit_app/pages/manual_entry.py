import streamlit as st
from src.hoarder.utils.database import get_session
from src.hoarder.services.job_service import JobService


def show() -> None:
    """Display the manual job entry page"""
    st.title("Manual Job Entry")
    st.write("Enter job posting information manually")

    with st.form("manual_entry_form", clear_on_submit=True):
        company_name = st.text_input(
            "Company Name",
            placeholder="e.g., Acme Corp",
            help="Enter the company name",
        )

        job_title = st.text_input(
            "Job Title",
            placeholder="e.g., Software Engineer",
            help="Enter the job title",
        )

        job_url = st.text_input(
            "Job URL (Optional)",
            placeholder="e.g., https://company.com/careers/job-123",
            help="Enter the URL to the job posting",
        )

        job_description = st.text_area(
            "Job Description",
            placeholder="Enter the full job description here...",
            help="Paste or type the complete job description",
            height=300,
        )

        industry = st.text_input(
            "Industry (Optional)",
            placeholder="e.g., Technology, Finance",
            help="Optionally specify the company's industry",
        )

        submitted = st.form_submit_button("Submit Job Posting")

        if submitted:
            # Validate inputs
            if not company_name:
                st.error("Company name is required")
                return

            if not job_title:
                st.error("Job title is required")
                return

            if not job_description:
                st.error("Job description is required")
                return

            # Save to database
            session = get_session()
            try:
                job_service = JobService(session)
                job_post = job_service.create_job_post(
                    company_name=company_name,
                    job_title=job_title,
                    job_description=job_description,
                    job_url=job_url if job_url else None,
                    industry=industry if industry else None,
                )

                st.success(
                    f"✓ Successfully saved job posting: '{job_post.title}' at {company_name} (ID: {job_post.id})"
                )

            except Exception as e:
                st.error(f"Error saving job posting: {str(e)}")
            finally:
                session.close()


if __name__ == "__main__":
    show()
