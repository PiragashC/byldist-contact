from django.db import models


class ContactSubmission(models.Model):
    ROLE_ARCHITECT = "architect"
    ROLE_INTERIOR_DESIGNER = "interior_designer"
    ROLE_BRAND_MARKETING = "brand_marketing"
    ROLE_DEVELOPER = "developer"
    ROLE_OTHER = "other"

    ROLE_CHOICES = [
        (ROLE_ARCHITECT, "Architect"),
        (ROLE_INTERIOR_DESIGNER, "Interior Designer"),
        (ROLE_BRAND_MARKETING, "Brand/Marketing"),
        (ROLE_DEVELOPER, "Developer"),
        (ROLE_OTHER, "Other"),
    ]

    PROJECT_RETAIL = "retail_fit_out"
    PROJECT_FNB = "fnb_restaurant"
    PROJECT_OFFICE = "office_interior"
    PROJECT_RESIDENTIAL = "residential"
    PROJECT_HOSPITALITY = "hospitality"
    PROJECT_OTHER = "other"

    PROJECT_TYPE_CHOICES = [
        (PROJECT_RETAIL, "Retail fit-out"),
        (PROJECT_FNB, "F&B / Restaurant"),
        (PROJECT_OFFICE, "Office interior"),
        (PROJECT_RESIDENTIAL, "Residential"),
        (PROJECT_HOSPITALITY, "Hospitality"),
        (PROJECT_OTHER, "Other"),
    ]

    TIMELINE_IMMEDIATELY = "immediately"
    TIMELINE_ONE_MONTH = "within_1_month"
    TIMELINE_ONE_TO_THREE = "one_to_three_months"
    TIMELINE_THREE_TO_SIX = "three_to_six_months"
    TIMELINE_SIX_PLUS = "six_plus_months"
    TIMELINE_EXPLORING = "just_exploring"

    TIMELINE_CHOICES = [
        (TIMELINE_IMMEDIATELY, "Immediately"),
        (TIMELINE_ONE_MONTH, "Within 1 month"),
        (TIMELINE_ONE_TO_THREE, "1-3 months"),
        (TIMELINE_THREE_TO_SIX, "3-6 months"),
        (TIMELINE_SIX_PLUS, "6+ months"),
        (TIMELINE_EXPLORING, "Just exploring"),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField()
    company = models.CharField(max_length=255, blank=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, blank=True)
    project_location = models.CharField(max_length=255, blank=True)
    project_type = models.CharField(
        max_length=50, choices=PROJECT_TYPE_CHOICES, blank=True
    )
    start_timeline = models.CharField(
        max_length=50, choices=TIMELINE_CHOICES, blank=True
    )
    project_brief = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.name} - {self.email}"
