from fastapi import APIRouter, Request, Response, status, HTTPException
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
    form_data = await request.json()
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
        print(response.status_code)
    except Exception as e:
        print(f"Error sending mail: {e}")
        raise HTTPException(status_code=500, detail="Error sending mail")
    return Response(
        content=html, media_type="text/html", status_code=status.HTTP_201_CREATED
    )
