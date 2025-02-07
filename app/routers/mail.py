from fastapi import APIRouter, Request, Response, status
from jinja2 import Environment, select_autoescape, PackageLoader
from pydantic import Json
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from app.config.config import settings


router = APIRouter(prefix="/mail", tags=["Mail management"])

jinja2_env = Environment(
    loader=PackageLoader("app"), autoescape=select_autoescape(["html", "xml"])
)


@router.post("/submit", status_code=status.HTTP_201_CREATED)
async def submit_form(request: Request):
    form_data = await request.json()  # Parse the incoming JSON data
    print(type(form_data))
    print(form_data)
    sg_client = SendGridAPIClient(settings.SENDGRID_API_KEY)
    template = jinja2_env.get_template("mail.html")
    html = template.render(name="Made for More", form=form_data)

    mail = Mail(
        from_email=settings.SENDER_EMAIL,
        to_emails=settings.RECEIPIENT_EMAIL,
        subject="Re: contact form",
        html_content=html,
    )

    try:
        response = sg_client.send(mail)
        print("hi")
    except Exception as e:
        print(f"Error sending mail: {e}")
    return Response(content=html, media_type="text/html")
