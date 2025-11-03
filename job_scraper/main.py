import subprocess
import sys
import typer
from typing import Optional

from src.hoarder.utils.database import get_session
from src.hoarder.services.scrape_job_webpage import scrape_and_save_job_webpage
from src.hoarder.services.job_service import JobService

app = typer.Typer(help="Job Scraper - CLI and Web Application")


@app.command()
def main(
    url: Optional[str] = typer.Option(
        None, "--url", "-u", help="URL of the job posting to scrape"
    ),
    manual: bool = typer.Option(
        False, "--manual", "-m", help="Manually enter job posting information"
    ),
    start: bool = typer.Option(
        False,
        "--start",
        "-s",
        help="Start the Streamlit web application",
    ),
) -> None:
    """
    Job Scraper Application

    Use --start/-s to launch the Streamlit web interface
    Use --url/-u to scrape a job posting from a URL (CLI mode)
    Use --manual/-m to manually enter job information (CLI mode)

    Note: Run 'alembic upgrade head' to initialize the database before first use.
    """
    if start:
        typer.echo("Starting Streamlit application...")
        typer.echo("The app will open in your browser at http://localhost:8501")
        try:
            subprocess.run(
                [sys.executable, "-m", "streamlit", "run", "streamlit_app/app.py"],
                check=True,
            )
        except subprocess.CalledProcessError as e:
            typer.echo(f"Error starting Streamlit: {e}", err=True)
            raise typer.Exit(code=1)
        except KeyboardInterrupt:
            typer.echo("\nStreamlit application stopped")
            raise typer.Exit(code=0)

    elif url:
        typer.echo(f"Fetching job posting from: {url}")
        session = get_session()
        try:
            job_page = scrape_and_save_job_webpage(url, session)

            if job_page:
                typer.echo(
                    f"✓ Saved job page: {job_page.url} (Page ID: {job_page.page_id})"
                )
                typer.echo(f"  HTML length: {len(job_page.page_html)} characters")
            else:
                typer.echo("Failed to scrape and save job page from URL", err=True)
                raise typer.Exit(code=1)
        finally:
            session.close()

    elif manual:
        typer.echo("Enter job posting information:")
        company_name = typer.prompt("Company name")
        job_title = typer.prompt("Job title")
        job_description = typer.prompt("Job description")

        session = get_session()
        try:
            job_service = JobService(session)
            job_post = job_service.create_job_post(
                company_name=company_name,
                job_title=job_title,
                job_description=job_description,
            )

            typer.echo(
                f"✓ Saved job posting: '{job_post.title}' at {company_name} (ID: {job_post.id})"
            )
            typer.echo("  Job queued for processing")
        finally:
            session.close()

    else:
        typer.echo("Please specify --start, --url, or --manual flag")
        typer.echo("Use --help for more information")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
