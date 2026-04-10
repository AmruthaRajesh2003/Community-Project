from django.contrib import admin
from community_appilication.alert import email_alert
from .models import UserProfile, PatientRecord, DiseaseReport, HealthEvent, CommunityAlert

def send_alert_email(modeladmin, request, queryset):
    """
    Send an alert email to selected citizens using custom email function.
    """
    count = 0
    failed = 0
    for user in queryset:
        if user.role == 'citizen' and user.email:
            subject = 'Health Alert from Community Health Department'
            body = f'Dear {user.get_full_name() or user.username},\n\n' \
                   'This is an important health alert from the Community Health Department. ' \
                   'Please check your health status, follow local health guidelines, and stay informed.\n\n' \
                   'If you have any concerns, contact your local health worker.\n\n' \
                   'Regards,\nCommunity Health Department'
            success = email_alert(subject, body, user.email)
            if success:
                count += 1
            else:
                failed += 1
                modeladmin.message_user(request, f"Failed to send email to {user.email}", level='error')
    if count > 0:
        modeladmin.message_user(request, f"Alert emails sent successfully to {count} citizens.", level='success')
    if failed > 0:
        modeladmin.message_user(request, f"{failed} emails failed to send.", level='warning')
    if count == 0 and failed == 0:
        modeladmin.message_user(request, "No valid citizens with email addresses selected.", level='warning')

send_alert_email.short_description = "Send alert email to selected citizens"

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'role', 'phone_number', 'email')
    list_filter = ('role', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)
    actions = [send_alert_email]

@admin.register(PatientRecord)
class PatientRecordAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'gender', 'condition', 'diagnosis_date', 'contact_number')
    list_filter = ('gender', 'condition', 'diagnosis_date')
    search_fields = ('name', 'condition', 'contact_number')
    ordering = ('-diagnosis_date',)
    readonly_fields = ('created_at', 'updated_at')

    def has_add_permission(self, request):
        return request.user.is_health_worker()

    def has_change_permission(self, request, obj=None):
        return request.user.is_health_worker()

    def has_delete_permission(self, request, obj=None):
        return request.user.is_health_worker()

    def has_view_permission(self, request, obj=None):
        return request.user.is_health_worker()

@admin.register(DiseaseReport)
class DiseaseReportAdmin(admin.ModelAdmin):
    list_display = ('disease_type', 'affected_area', 'cases_reported', 'severity_level', 'status', 'reported_at', 'is_confirmed')
    list_filter = ('disease_type', 'severity_level', 'status', 'is_confirmed', 'reported_at')
    search_fields = ('affected_area', 'reporter_name', 'additional_info')
    ordering = ('-reported_at',)
    readonly_fields = ('reported_at', 'updated_at', 'verified_date', 'approved_date')
    fieldsets = (
        ('Report Details', {
            'fields': ('created_by', 'disease_type', 'affected_area', 'cases_reported', 'severity_level', 'outbreak_start_date', 'additional_info', 'reporter_name', 'reporter_contact')
        }),
        ('Workflow', {
            'fields': ('status', 'verifier', 'approver', 'verifier_comment', 'approver_comment', 'verified_date', 'approved_date')
        }),
        ('Actions', {
            'fields': ('is_confirmed', 'action_taken')
        }),
        ('Timestamps', {
            'fields': ('reported_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(HealthEvent)
class HealthEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'location', 'start_datetime', 'status', 'assigned_to')
    list_filter = ('event_type', 'status', 'start_datetime')
    search_fields = ('title', 'location', 'assigned_to', 'description')
    ordering = ('-start_datetime',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(CommunityAlert)
class CommunityAlertAdmin(admin.ModelAdmin):
    list_display = ('subject', 'created_by', 'sent_at', 'recipients_count', 'sent_successfully', 'sent_failed')
    list_filter = ('sent_at',)
    search_fields = ('subject', 'message', 'created_by__username')
    ordering = ('-sent_at',)
    readonly_fields = ('sent_at', 'recipients_count', 'sent_successfully', 'sent_failed')

# Register your models here.
