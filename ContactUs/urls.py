from django.urls import path

from ContactUs.views import ContactSubmissionCreateView

urlpatterns = [
    path("contact-submissions/", ContactSubmissionCreateView.as_view(), name="contact-submission-create"),
]

