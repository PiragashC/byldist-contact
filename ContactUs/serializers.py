from rest_framework import serializers

from ContactUs.models import ContactSubmission


class ContactSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSubmission
        fields = [
            "id",
            "name",
            "email",
            "company",
            "role",
            "project_location",
            "project_type",
            "start_timeline",
            "project_brief",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate(self, attrs):
        # Ensure required fields are present; others may be blank but not missing.
        missing = [field for field in ["name", "email", "project_brief"] if not attrs.get(field)]
        if missing:
            raise serializers.ValidationError(
                {field: "This field is required." for field in missing}
            )
        return attrs

