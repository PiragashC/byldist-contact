import os
from typing import Dict

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from ContactUs.models import ContactSubmission
from ContactUs.serializers import ContactSubmissionSerializer


class ContactSubmissionCreateView(GenericAPIView):
    serializer_class = ContactSubmissionSerializer
    permission_classes = []  # public endpoint
    authentication_classes = []  # public endpoint

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create an unsaved instance to leverage helper methods like get_role_display()
        submission = ContactSubmission(**serializer.validated_data)

        try:
            self._send_email_notification(submission)
            return Response(
                {"message": "Contact request submitted successfully."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            # Log the error in a real app
            return Response(
                {"detail": "Failed to send email.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _send_email_notification(self, submission: ContactSubmission) -> None:
        recipient = getattr(settings, "CONTACT_US_RECIPIENT", None) or os.getenv(
            "CONTACT_US_RECIPIENT"
        )
        if not recipient:
            raise ValueError("CONTACT_US_RECIPIENT env var is not configured.")

        subject = f"New contact request from {submission.name}"
        context: Dict[str, str] = {
            "name": submission.name,
            "email": submission.email,
            "company": submission.company or "N/A",
            "role": submission.get_role_display() or "N/A",
            "project_location": submission.project_location or "N/A",
            "project_type": submission.get_project_type_display() or "N/A",
            "timeline": submission.get_start_timeline_display() or "N/A",
            "project_brief": submission.project_brief,
        }

        # Choose template based on request data if available (defaults to dark)
        theme = self.request.data.get('theme', 'dark').lower()
        if theme == 'light':
            template_name = "contact_us/email_light.html"
        else:
            template_name = "contact_us/email_dark.html"

        text_body = render_to_string("contact_us/email.txt", context)
        html_body = render_to_string(template_name, context)

        msg = "Sending email via {}:{} | TLS={} | SSL={} | User={}".format(
            getattr(settings, 'EMAIL_HOST', 'unknown'),
            getattr(settings, 'EMAIL_PORT', 'unknown'),
            getattr(settings, 'EMAIL_USE_TLS', 'unknown'),
            getattr(settings, 'EMAIL_USE_SSL', 'unknown'),
            getattr(settings, 'EMAIL_HOST_USER', '')[:3] + '***'  # Masked
        )
        print(msg) # Printing to stdout for Render logs

        message = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
            to=[recipient],
            reply_to=[submission.email],  # lets the owner reply directly to visitor
        )
        message.attach_alternative(html_body, "text/html")
        message.send(fail_silently=False)



@api_view(['GET'])
def health_check(request):
    print("Health check ping received")
    return Response({"status": "ok"}, status=status.HTTP_200_OK)
