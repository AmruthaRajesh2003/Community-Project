from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from community_appilication.alert import send_community_health_email


class UserProfile(AbstractUser):
    ROLE_CHOICES = [
        ('health_worker', 'Health Worker'),
        ('citizen', 'Citizen'),
    ]
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='citizen')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    aadhar_number = models.CharField(max_length=12, unique=True, null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True, null=True)
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"
    def is_health_worker(self):
        return self.role == 'health_worker'
    
    def is_citizen(self):
        return self.role == 'citizen'

class PatientRecord(models.Model):
    """
    Model for patient health records
    Corresponds to the patient records form in user-dashboard.html
    """
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('U', 'Unknown'),
    ]

    created_by = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='patient_records',
        verbose_name="Created By"
    )
    citizen = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='citizen_patient_records',
        verbose_name="Citizen",
        limit_choices_to={'role': 'citizen'}
    )
    name = models.CharField(max_length=100, verbose_name="Patient Name")
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(120)],
        verbose_name="Age"
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default='U',
        verbose_name="Gender"
    )
    contact_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name="Contact Number"
    )
    address = models.TextField(blank=True, null=True, verbose_name="Address")
    condition = models.CharField(max_length=255, verbose_name="Medical Condition")
    diagnosis_date = models.DateField(
        default=timezone.now,
        verbose_name="Diagnosis Date"
    )
    treatment_plan = models.TextField(verbose_name="Treatment Plan")
    medications = models.TextField(blank=True, null=True, verbose_name="Medications")
    allergies = models.TextField(blank=True, null=True, verbose_name="Allergies")
    emergency_contact = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Emergency Contact"
    )
    emergency_phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name="Emergency Phone"
    )
    notes = models.TextField(blank=True, null=True, verbose_name="Additional Notes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Patient Record"
        verbose_name_plural = "Patient Records"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} (Age: {self.age}, Condition: {self.condition})"

    def get_age_group(self):
        """Helper method to categorize patient by age group"""
        if self.age < 18:
            return "Child"
        elif self.age < 65:
            return "Adult"
        else:
            return "Senior"

class DiseaseReport(models.Model):
    """
    Model for disease outbreak reporting
    Corresponds to the disease reporting form in user-dashboard.html
    """
    DISEASE_CHOICES = [
        ('flu', 'Influenza (Flu)'),
        ('covid', 'COVID-19'),
        ('dengue', 'Dengue'),
        ('malaria', 'Malaria'),
        ('cholera', 'Cholera'),
        ('tuberculosis', 'Tuberculosis'),
        ('measles', 'Measles'),
        ('hepatitis', 'Hepatitis'),
        ('other', 'Other'),
    ]

    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    created_by = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='disease_reports',
        verbose_name="Created By"
    )
    disease_type = models.CharField(
        max_length=50,
        choices=DISEASE_CHOICES,
        verbose_name="Disease Type"
    )
    affected_area = models.CharField(
        max_length=255,
        verbose_name="Affected Area"
    )
    cases_reported = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Number of Cases"
    )
    severity_level = models.CharField(
        max_length=10,
        choices=SEVERITY_CHOICES,
        default='medium',
        verbose_name="Severity Level"
    )
    outbreak_start_date = models.DateField(
        default=timezone.now,
        verbose_name="Outbreak Start Date"
    )
    additional_info = models.TextField(
        blank=True,
        null=True,
        verbose_name="Additional Information"
    )
    reporter_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Reporter Name"
    )
    reporter_contact = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name="Reporter Contact"
    )
    is_confirmed = models.BooleanField(
        default=False,
        verbose_name="Confirmed Outbreak"
    )
    email_notification_sent = models.BooleanField(
        default=False,
        verbose_name="Email Notification Sent"
    )
    action_taken = models.TextField(
        blank=True,
        null=True,
        verbose_name="Action Taken"
    )
    reported_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Workflow fields
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('verified', 'Verified'), ('approved', 'Approved'), ('rejected', 'Rejected')],
        default='pending',
        verbose_name="Workflow Status"
    )
    verifier = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_reports',
        verbose_name="Verifier"
    )
    approver = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_reports',
        verbose_name="Approver"
    )
    verifier_comment = models.TextField(blank=True, null=True, verbose_name="Verifier Comment")
    approver_comment = models.TextField(blank=True, null=True, verbose_name="Approver Comment")
    verified_date = models.DateTimeField(null=True, blank=True, verbose_name="Verified Date")
    approved_date = models.DateTimeField(null=True, blank=True, verbose_name="Approved Date")

    class Meta:
        verbose_name = "Disease Report"
        verbose_name_plural = "Disease Reports"
        ordering = ['-reported_at']

    def __str__(self):
        return f"{self.get_disease_type_display()} in {self.affected_area} ({self.cases_reported} cases)"

    def get_severity_display(self):
        """Get severity level with color coding"""
        severity_colors = {
            'low': '🟢',
            'medium': '🟡',
            'high': '🟠',
            'critical': '🔴'
        }
        return f"{severity_colors.get(self.severity_level, '⚪')} {self.get_severity_level_display()}"

    def save(self, *args, **kwargs):
        if self.pk:  # if updating
            old_instance = DiseaseReport.objects.get(pk=self.pk)
            if not self.email_notification_sent and not old_instance.is_confirmed and self.is_confirmed:
                # Send email notification to all users with emails
                users = UserProfile.objects.exclude(email__isnull=True).exclude(email='')
                recipients = [u.email for u in users]
                if recipients:
                    subject = f"Confirmed Disease Report: {self.disease_type}"
                    body = f"A disease report has been confirmed:\n\nDisease Type: {self.disease_type}\nAffected Area: {self.affected_area}\nCases Reported: {self.cases_reported}\nSeverity: {self.severity_level}\nOutbreak Start: {self.outbreak_start_date}\nAdditional Info: {self.additional_info}\n\nPlease check your dashboard for more details."
                    send_community_health_email(subject, body, recipients)
                    self.email_notification_sent = True
        super().save(*args, **kwargs)

class HealthEvent(models.Model):
    """
    Model for health events and schedule items
    Corresponds to the schedule section in user-dashboard.html
    """
    EVENT_TYPES = [
        ('visit', 'Community Visit'),
        ('vaccination', 'Vaccination Drive'),
        ('workshop', 'Health Workshop'),
        ('screening', 'Health Screening'),
        ('meeting', 'Team Meeting'),
        ('other', 'Other Event'),
    ]

    created_by = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='health_events',
        verbose_name="Created By"
    )
    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPES,
        verbose_name="Event Type"
    )
    title = models.CharField(max_length=200, verbose_name="Event Title")
    description = models.TextField(verbose_name="Event Description")
    location = models.CharField(max_length=255, verbose_name="Location")
    start_datetime = models.DateTimeField(verbose_name="Start Date & Time")
    end_datetime = models.DateTimeField(verbose_name="End Date & Time")
    assigned_to = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Assigned To"
    )
    status = models.CharField(
        max_length=20,
        choices=[('scheduled', 'Scheduled'), ('completed', 'Completed'), ('cancelled', 'Cancelled')],
        default='scheduled',
        verbose_name="Status"
    )
    email_notification_sent = models.BooleanField(
        default=False,
        verbose_name="Email Notification Sent"
    )
    notes = models.TextField(blank=True, null=True, verbose_name="Notes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Health Event"
        verbose_name_plural = "Health Events"
        ordering = ['start_datetime']

    def __str__(self):
        return f"{self.title} - {self.get_event_type_display()}"

    def save(self, *args, **kwargs):
        if not self.email_notification_sent and self.status == 'scheduled':
            if self.pk:  # if updating
                old_instance = HealthEvent.objects.get(pk=self.pk)
                if old_instance.status != 'scheduled':
                    # Send email notification to all users with emails
                    users = UserProfile.objects.exclude(email__isnull=True).exclude(email='')
                    recipients = [u.email for u in users]
                    if recipients:
                        subject = f"New Health Event Scheduled: {self.title}"
                        body = f"A new health event has been scheduled:\n\nEvent Type: {self.get_event_type_display()}\nTitle: {self.title}\nDescription: {self.description}\nLocation: {self.location}\nStart: {self.start_datetime}\nEnd: {self.end_datetime}\n\nPlease check your dashboard for more details."
                        send_community_health_email(subject, body, recipients)
                        self.email_notification_sent = True
            else:  # if creating
                # Send email notification to all users with emails
                users = UserProfile.objects.exclude(email__isnull=True).exclude(email='')
                recipients = [u.email for u in users]
                if recipients:
                    subject = f"New Health Event Scheduled: {self.title}"
                    body = f"A new health event has been scheduled:\n\nEvent Type: {self.get_event_type_display()}\nTitle: {self.title}\nDescription: {self.description}\nLocation: {self.location}\nStart: {self.start_datetime}\nEnd: {self.end_datetime}\n\nPlease check your dashboard for more details."
                    send_community_health_email(subject, body, recipients)
                    self.email_notification_sent = True
        super().save(*args, **kwargs)

    def is_upcoming(self):
        """Check if event is upcoming (within next 7 days)"""
        return self.start_datetime > timezone.now() and (self.start_datetime - timezone.now()).days <= 7

class CommunityAlert(models.Model):
    """
    Model for community alerts sent to all citizens
    """
    created_by = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='community_alerts',
        verbose_name="Created By",
        limit_choices_to={'role': 'health_worker'}
    )
    subject = models.CharField(max_length=200, verbose_name="Alert Subject")
    message = models.TextField(verbose_name="Alert Message")
    sent_at = models.DateTimeField(auto_now_add=True)
    recipients_count = models.PositiveIntegerField(default=0, verbose_name="Number of Recipients")
    sent_successfully = models.PositiveIntegerField(default=0, verbose_name="Sent Successfully")
    sent_failed = models.PositiveIntegerField(default=0, verbose_name="Sent Failed")

    class Meta:
        verbose_name = "Community Alert"
        verbose_name_plural = "Community Alerts"
        ordering = ['-sent_at']

    def __str__(self):
        return f"{self.subject} - {self.sent_at.strftime('%Y-%m-%d %H:%M')}"
