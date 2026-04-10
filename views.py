from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile, PatientRecord, DiseaseReport, HealthEvent, CommunityAlert
from django.db import IntegrityError
from datetime import datetime
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
from django.utils import timezone
import random
import time
from community_appilication.alert import send_community_health_email

def index(request):
	return render(request, 'index.html')

@csrf_protect
def register_view(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		confirm_password = request.POST.get('confirm_password')
		role = request.POST['role']
		first_name = request.POST.get('first_name', '')
		last_name = request.POST.get('last_name', '')
		email = request.POST.get('email', '')
		phone_number = request.POST.get('phone_number', '')
		date_of_birth = request.POST.get('date_of_birth', None)
		gender = request.POST.get('gender', '')
		address = request.POST.get('address', '')
		aadhar_number = request.POST.get('aadhar_number')
		city = request.POST.get('city', '')
		emergency_contact_name = request.POST.get('emergency_contact_name', '')
		emergency_contact_phone = request.POST.get('emergency_contact_phone', '')
		blood_group = request.POST.get('blood_group', '')
		profile_picture = request.FILES.get('profile_picture', None)

		if password != confirm_password:
			messages.error(request, 'Passwords do not match.')
			return render(request, 'frontend_html/register.html')

		try:
			user = UserProfile.objects.create_user(
				username=username,
				password=password,
				role=role,
				first_name=first_name,
				last_name=last_name,
				email=email,
				phone_number=phone_number,
				gender=gender,
				address=address,
				city=city,
				emergency_contact_name=emergency_contact_name,
				emergency_contact_phone=emergency_contact_phone,
				blood_group=blood_group,
				profile_picture=profile_picture
			)
			if date_of_birth:
				try:
					user.date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
				except ValueError:
					messages.error(request, 'Invalid date format for Date of Birth.')
					return render(request, 'frontend_html/register.html')
			user.save()
			messages.success(request, 'Registration successful. Please log in.')
			return redirect('user:login')
		except IntegrityError:
			messages.error(request, 'Username already exists.')
	return render(request, 'frontend_html/register.html')

@csrf_protect
def register_citizen_view(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		confirm_password = request.POST.get('confirm_password')
		role = 'citizen'  # Set role to citizen
		first_name = request.POST.get('first_name', '')
		last_name = request.POST.get('last_name', '')
		email = request.POST.get('email', '')
		phone_number = request.POST.get('phone_number', '')
		date_of_birth = request.POST.get('date_of_birth', None)
		gender = request.POST.get('gender', '')
		address = request.POST.get('address', '')
		city = request.POST.get('city', '')
		emergency_contact_name = request.POST.get('emergency_contact_name', '')
		emergency_contact_phone = request.POST.get('emergency_contact_phone', '')
		blood_group = request.POST.get('blood_group', '')
		profile_picture = request.FILES.get('profile_picture', None)

		if password != confirm_password:
			messages.error(request, 'Passwords do not match.')
			return render(request, 'frontend_html/register_citizen.html')

		try:
			user = UserProfile.objects.create_user(
				username=username,
				password=password,
				role=role,
				first_name=first_name,
				last_name=last_name,
				email=email,
				phone_number=phone_number,
				gender=gender,
				address=address,
				city=city,
				emergency_contact_name=emergency_contact_name,
				emergency_contact_phone=emergency_contact_phone,
				blood_group=blood_group,
				profile_picture=profile_picture
			)
			if date_of_birth:
				try:
					user.date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
				except ValueError:
					messages.error(request, 'Invalid date format for Date of Birth.')
					return render(request, 'frontend_html/register_citizen.html')
			user.save()
			messages.success(request, 'Registration successful. Please log in.')
			return redirect('user:login')
		except IntegrityError:
			messages.error(request, 'Username already exists.')
	return render(request, 'frontend_html/register_citizen.html')

@csrf_protect
def register_health_worker_view(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		confirm_password = request.POST.get('confirm_password')
		role = 'health_worker'  # Set role to health_worker
		first_name = request.POST.get('first_name', '')
		last_name = request.POST.get('last_name', '')
		email = request.POST.get('email', '')
		phone_number = request.POST.get('phone_number', '')
		date_of_birth = request.POST.get('date_of_birth', None)
		gender = request.POST.get('gender', '')
		address = request.POST.get('address', '')
		city = request.POST.get('city', '')
		emergency_contact_name = request.POST.get('emergency_contact_name', '')
		emergency_contact_phone = request.POST.get('emergency_contact_phone', '')
		blood_group = request.POST.get('blood_group', '')
		profile_picture = request.FILES.get('profile_picture', None)

		if password != confirm_password:
			messages.error(request, 'Passwords do not match.')
			return render(request, 'frontend_html/register_health_worker.html')

		try:
			user = UserProfile.objects.create_user(
				username=username,
				password=password,
				role=role,
				first_name=first_name,
				last_name=last_name,
				email=email,
				phone_number=phone_number,
				gender=gender,
				address=address,
				city=city,
				emergency_contact_name=emergency_contact_name,
				emergency_contact_phone=emergency_contact_phone,
				blood_group=blood_group,
				profile_picture=profile_picture
			)
			if date_of_birth:
				try:
					user.date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
				except ValueError:
					messages.error(request, 'Invalid date format for Date of Birth.')
					return render(request, 'frontend_html/register_health_worker.html')
			user.save()
			messages.success(request, 'Registration successful. Please log in.')
			return redirect('user:login')
		except IntegrityError:
			messages.error(request, 'Username already exists.')
	return render(request, 'frontend_html/register_health_worker.html')

@login_required
def health_worker_dashboard(request):
	# Health workers can see all records
	patient_records = PatientRecord.objects.all()
	disease_reports = DiseaseReport.objects.all()
	health_events = HealthEvent.objects.all()
	citizens = UserProfile.objects.filter(role='citizen', is_superuser=False)
	context = {
		'patient_records': patient_records,
		'disease_reports': disease_reports,
		'health_events': health_events,
		'citizens': citizens,
	}
	return render(request, 'frontend_html/user_dashboard.html', context)

@login_required
def citizen_dashboard(request):
	# Citizens can only see their own records and confirmed disease reports
	citizen_full_name = request.user.get_full_name()
	if citizen_full_name:
		patient_records = PatientRecord.objects.filter(name=citizen_full_name)
	else:
		patient_records = PatientRecord.objects.none()
	health_events = HealthEvent.objects.filter(status='scheduled')
	disease_reports = DiseaseReport.objects.filter(is_confirmed=True)
	context = {
		'patient_records': patient_records,
		'health_events': health_events,
		'disease_reports': disease_reports,
	}
	return render(request, 'frontend_html/citizen_dashboard.html', context)

@csrf_protect
def login_view(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			if not user.email:
				messages.error(request, 'No email associated with this account. Please contact support.')
				return render(request, 'frontend_html/login.html')
			# Generate OTP
			otp = random.randint(100000, 999999)
			request.session['otp'] = str(otp)
			request.session['user_id'] = user.id
			request.session['otp_timestamp'] = time.time()
			# Send OTP email
			subject = 'Your CHWMS Login OTP'
			message = f'Your OTP is {otp}. It is valid for 5 minutes.'
			from_email = 'sonubiju17@gmail.com'
			try:
				send_mail(subject, message, from_email, [user.email])
				messages.success(request, 'OTP sent to your email. Please verify to complete login.')
			except Exception as e:
				messages.error(request, f'Failed to send OTP. Error: {str(e)}. Please try again.')
				return render(request, 'frontend_html/login.html')
			return redirect('user:otp_verify')
		else:
			messages.error(request, 'Invalid username or password.')
	return render(request, 'frontend_html/login.html')

def logout_view(request):
	logout(request)
	return redirect('user:index')

@csrf_protect
def otp_verify(request):
	if request.method == 'POST':
		entered_otp = request.POST.get('otp', '').strip()
		session_otp = request.session.get('otp')
		user_id = request.session.get('user_id')
		timestamp = request.session.get('otp_timestamp')
		if not all([session_otp, user_id, timestamp]):
			messages.error(request, 'Session expired. Please log in again.')
			return redirect('user:login')
		current_time = time.time()
		if current_time - timestamp > 300:  # 5 minutes
			request.session.pop('otp', None)
			request.session.pop('user_id', None)
			request.session.pop('otp_timestamp', None)
			messages.error(request, 'OTP expired. Please log in again.')
			return redirect('user:login')
		if entered_otp == session_otp:
			try:
				user = UserProfile.objects.get(id=user_id)
				login(request, user)
				user.email_verified = True
				user.save()
				request.session.pop('otp', None)
				request.session.pop('user_id', None)
				request.session.pop('otp_timestamp', None)
				if user.role == 'health_worker':
					return redirect('user:health_worker_dashboard')
				else:
					return redirect('user:citizen_dashboard')
			except UserProfile.DoesNotExist:
				messages.error(request, 'User not found.')
				return redirect('user:login')
		else:
			messages.error(request, 'Invalid OTP. Please try again.')
			if 'resend' in request.POST:
				# Resend OTP
				try:
					user = UserProfile.objects.get(id=user_id)
					otp = random.randint(100000, 999999)
					request.session['otp'] = str(otp)
					request.session['otp_timestamp'] = time.time()
					subject = 'Your CHWMS Login OTP'
					message = f'Your OTP is {otp}. It is valid for 5 minutes.'
					from_email = 'sonubiju17@gmail.com'
					try:
						send_mail(subject, message, from_email, [user.email])
						messages.success(request, 'OTP resent to your email.')
					except Exception as e:
						messages.error(request, f'Failed to resend OTP. Error: {str(e)}. Please try again.')
				except UserProfile.DoesNotExist:
					messages.error(request, 'User not found.')
					return redirect('user:login')
	return render(request, 'frontend_html/otp_verify.html')

@csrf_protect
def forgot_password_view(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		email = request.POST.get('email')

		try:
			user = UserProfile.objects.get(username=username, email=email)
			# Here you would typically send a password reset email
			# For now, we'll just show a success message
			messages.success(request, 'Password reset instructions have been sent to your email.')
			return redirect('user:login')
		except UserProfile.DoesNotExist:
			messages.error(request, 'No user found with the provided username and email.')

	return render(request, 'frontend_html/forgot_password.html')

@login_required
@csrf_protect
def edit_profile_view(request):
	if request.method == 'POST':
		first_name = request.POST.get('first_name', '')
		last_name = request.POST.get('last_name', '')
		email = request.POST.get('email', '')
		phone_number = request.POST.get('phone_number', '')
		date_of_birth = request.POST.get('date_of_birth', None)
		gender = request.POST.get('gender', '')
		address = request.POST.get('address', '')
		city = request.POST.get('city', '')
		aadhar_number = request.POST.get('aadhar_number', '')
		emergency_contact_name = request.POST.get('emergency_contact_name', '')
		emergency_contact_phone = request.POST.get('emergency_contact_phone', '')
		blood_group = request.POST.get('blood_group', '')
		profile_picture = request.FILES.get('profile_picture', None)

		user = request.user
		user.first_name = first_name
		user.last_name = last_name
		user.email = email
		user.phone_number = phone_number
		user.gender = gender
		user.address = address
		user.city = city
		user.aadhar_number = aadhar_number
		user.emergency_contact_name = emergency_contact_name
		user.emergency_contact_phone = emergency_contact_phone
		user.blood_group = blood_group
		if profile_picture:
			user.profile_picture = profile_picture

		if date_of_birth:
			try:
				user.date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
			except ValueError:
				messages.error(request, 'Invalid date format for Date of Birth.')
				return render(request, 'frontend_html/edit_profile.html')

		try:
			user.save()
			messages.success(request, 'Profile updated successfully.')
			return redirect('user:edit_profile')
		except IntegrityError:
			messages.error(request, 'Aadhar number already exists.')
			return render(request, 'frontend_html/edit_profile.html')

	return render(request, 'frontend_html/edit_profile.html')

@login_required
@require_http_methods(["POST"])
def create_community_alert(request):
	if not request.user.is_health_worker():
		return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)
	subject = request.POST.get('subject')
	message = request.POST.get('message')
	if not subject or not message:
		return JsonResponse({'status': 'error', 'message': 'Subject and message are required'})
	alert = CommunityAlert.objects.create(
		created_by=request.user,
		subject=subject,
		message=message
	)
	citizens = UserProfile.objects.filter(role='citizen').exclude(email__isnull=True).exclude(email='')
	recipients = [citizen.email for citizen in citizens]
	print(f"Community alert recipients: {recipients}")
	result = send_community_health_email(subject, message, recipients)
	alert.recipients_count = len(recipients)
	alert.sent_successfully = result['sent']
	alert.sent_failed = result['failed']
	alert.save()
	return JsonResponse({'status': 'success', 'message': f'Community alert created and sent to {result["sent"]} citizens. Failed: {result["failed"]}'})

# CRUD views for PatientRecord
@login_required
@require_http_methods(["POST"])
def create_patient_record(request):
	if not request.user.is_health_worker():
		return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)
	# Extract data from POST and create PatientRecord
	data = request.POST
	citizen_id = data.get('citizen_id')
	citizen = None
	if citizen_id:
		try:
			citizen = UserProfile.objects.get(id=citizen_id, role='citizen')
		except UserProfile.DoesNotExist:
			pass
	patient = PatientRecord(
		created_by=request.user,
		citizen=citizen,
		name=data.get('name'),
		age=data.get('age'),
		gender=data.get('gender'),
		contact_number=data.get('contact_number'),
		address=data.get('address'),
		condition=data.get('condition'),
		diagnosis_date=data.get('diagnosis_date'),
		treatment_plan=data.get('treatment_plan'),
		medications=data.get('medications'),
		allergies=data.get('allergies'),
		emergency_contact=data.get('emergency_contact'),
		emergency_phone=data.get('emergency_phone'),
		notes=data.get('notes'),
	)
	patient.save()
	return JsonResponse({'status': 'success', 'message': 'Patient record created'})

@login_required
@require_http_methods(["POST"])
def update_patient_record(request, pk):
	if not request.user.is_health_worker():
		return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)
	patient = get_object_or_404(PatientRecord, pk=pk)
	data = request.POST
	patient.name = data.get('name')
	patient.age = data.get('age')
	patient.gender = data.get('gender')
	patient.contact_number = data.get('contact_number')
	patient.address = data.get('address')
	patient.condition = data.get('condition')
	patient.diagnosis_date = data.get('diagnosis_date')
	patient.treatment_plan = data.get('treatment_plan')
	patient.medications = data.get('medications')
	patient.allergies = data.get('allergies')
	patient.emergency_contact = data.get('emergency_contact')
	patient.emergency_phone = data.get('emergency_phone')
	patient.notes = data.get('notes')
	patient.save()
	return JsonResponse({'status': 'success', 'message': 'Patient record updated'})

@login_required
def get_patient_record(request, pk):
	if not request.user.is_health_worker():
		return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)
	patient = get_object_or_404(PatientRecord, pk=pk)
	data = {
		'id': patient.id,
		'name': patient.name,
		'age': patient.age,
		'gender': patient.gender,
		'contact_number': patient.contact_number,
		'address': patient.address,
		'condition': patient.condition,
		'diagnosis_date': patient.diagnosis_date.strftime('%Y-%m-%d') if patient.diagnosis_date else '',
		'treatment_plan': patient.treatment_plan,
		'medications': patient.medications,
		'allergies': patient.allergies,
		'emergency_contact': patient.emergency_contact,
		'emergency_phone': patient.emergency_phone,
		'notes': patient.notes,
	}
	return JsonResponse(data)

@login_required
def get_citizen_data(request, pk):
	if not request.user.is_health_worker():
		return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)
	citizen = get_object_or_404(UserProfile, pk=pk, role='citizen')
	data = {
		'status': 'success',
		'citizen': {
			'id': citizen.id,
			'username': citizen.username,
			'get_full_name': citizen.get_full_name(),
			'age': citizen.age,
			'gender': citizen.gender,
			'phone_number': citizen.phone_number,
			'address': citizen.address,
			'emergency_contact_name': citizen.emergency_contact_name,
			'emergency_contact_phone': citizen.emergency_contact_phone,
		}
	}
	return JsonResponse(data)

@login_required
@require_http_methods(["POST"])
def delete_patient_record(request, pk):
	if not request.user.is_health_worker():
		return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)
	patient = get_object_or_404(PatientRecord, pk=pk)
	patient.delete()
	return JsonResponse({'status': 'success', 'message': 'Patient record deleted'})

# CRUD views for DiseaseReport
@login_required
@require_http_methods(["POST"])
def create_disease_report(request):
	data = request.POST
	report = DiseaseReport(
		created_by=request.user,
		disease_type=data.get('disease_type'),
		affected_area=data.get('affected_area'),
		cases_reported=data.get('cases_reported'),
		severity_level=data.get('severity_level', 'medium'),
		outbreak_start_date=data.get('outbreak_start_date'),
		additional_info=data.get('additional_info'),
		reporter_name=request.user.username,
		reporter_contact=data.get('reporter_contact'),
		is_confirmed=False,
		action_taken=data.get('action_taken'),
	)
	report.save()
	return JsonResponse({'status': 'success', 'message': 'Disease report created'})

@login_required
@require_http_methods(["POST"])
def update_disease_report(request, pk):
	report = get_object_or_404(DiseaseReport, pk=pk)
	data = request.POST
	report.disease_type = data.get('disease_type')
	report.affected_area = data.get('affected_area')
	report.cases_reported = data.get('cases_reported')
	report.severity_level = data.get('severity_level', 'medium')
	report.outbreak_start_date = data.get('outbreak_start_date')
	report.additional_info = data.get('additional_info')
	report.reporter_contact = data.get('reporter_contact')
	# Only allow superusers to set is_confirmed to True
	is_confirmed_value = data.get('is_confirmed')
	if is_confirmed_value == 'true':
		if request.user.is_superuser:
			report.is_confirmed = True
		else:
			return JsonResponse({'status': 'error', 'message': 'Permission denied to confirm report'}, status=403)
	else:
		report.is_confirmed = False
	report.action_taken = data.get('action_taken')
	report.save()
	return JsonResponse({'status': 'success', 'message': 'Disease report updated'})

@login_required
@require_http_methods(["POST"])
def delete_disease_report(request, pk):
	report = get_object_or_404(DiseaseReport, pk=pk)
	report.delete()
	return JsonResponse({'status': 'success', 'message': 'Disease report deleted'})

# CRUD views for HealthEvent
@login_required
@require_http_methods(["POST"])
def create_health_event(request):
	data = request.POST
	event = HealthEvent(
		created_by=request.user,
		event_type=data.get('event_type'),
		title=data.get('title'),
		description=data.get('description'),
		location=data.get('location'),
		start_datetime=data.get('start_datetime'),
		end_datetime=data.get('end_datetime'),
		assigned_to=data.get('assigned_to'),
		status=data.get('status', 'scheduled'),
		notes=data.get('notes'),
	)
	event.save()

	# Send email notification to assigned health worker if email exists
	if event.assigned_to:
		# Find user by username or email in assigned_to field
		assigned_users = UserProfile.objects.filter(username=event.assigned_to) | UserProfile.objects.filter(email=event.assigned_to)
		recipients = [user.email for user in assigned_users if user.email]
		print(f"Health event recipients: {recipients}")
		if recipients:
			subject = f"New Health Event Assigned: {event.title}"
			body = f"You have been assigned to a new health event:\n\nTitle: {event.title}\nDescription: {event.description}\nLocation: {event.location}\nStart: {event.start_datetime}\nEnd: {event.end_datetime}\n\nPlease check your dashboard for more details."
			send_community_health_email(subject, body, recipients)

	return JsonResponse({'status': 'success', 'message': 'Health event created'})

@login_required
@require_http_methods(["POST"])
def update_health_event(request, pk):
	event = get_object_or_404(HealthEvent, pk=pk)
	data = request.POST
	event.event_type = data.get('event_type')
	event.title = data.get('title')
	event.description = data.get('description')
	event.location = data.get('location')
	event.start_datetime = data.get('start_datetime')
	event.end_datetime = data.get('end_datetime')
	event.assigned_to = data.get('assigned_to')
	event.status = data.get('status', 'scheduled')
	event.notes = data.get('notes')
	event.save()
	return JsonResponse({'status': 'success', 'message': 'Health event updated'})

@login_required
@require_http_methods(["POST"])
def delete_health_event(request, pk):
	event = get_object_or_404(HealthEvent, pk=pk)
	event.delete()
	return JsonResponse({'status': 'success', 'message': 'Health event deleted'})

# Workflow views for DiseaseReport
@login_required
@require_http_methods(["POST"])
def verify_disease_report(request, pk):
	if not request.user.is_health_worker():
		return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)

	report = get_object_or_404(DiseaseReport, pk=pk)
	if report.status != 'pending':
		return JsonResponse({'status': 'error', 'message': 'Report is not in pending status'}, status=400)

	data = request.POST
	action = data.get('action')  # 'verify' or 'reject'
	comment = data.get('comment', '')

	if action == 'verify':
		report.status = 'verified'
		report.verifier = request.user
		report.verifier_comment = comment
		report.verified_date = timezone.now()
		message = 'Disease report verified successfully'
	elif action == 'reject':
		report.status = 'rejected'
		report.verifier = request.user
		report.verifier_comment = comment
		report.verified_date = timezone.now()
		message = 'Disease report rejected'
	else:
		return JsonResponse({'status': 'error', 'message': 'Invalid action'}, status=400)

	report.save()
	return JsonResponse({'status': 'success', 'message': message})

@login_required
@require_http_methods(["POST"])
def approve_disease_report(request, pk):
	if not request.user.is_health_worker():
		return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)

	report = get_object_or_404(DiseaseReport, pk=pk)
	if report.status != 'verified':
		return JsonResponse({'status': 'error', 'message': 'Report is not in verified status'}, status=400)

	data = request.POST
	action = data.get('action')  # 'approve' or 'reject'
	comment = data.get('comment', '')

	if action == 'approve':
		report.status = 'approved'
		report.approver = request.user
		report.approver_comment = comment
		report.approved_date = timezone.now()
		report.is_confirmed = True  # Set confirmed when approved
		message = 'Disease report approved successfully'
	elif action == 'reject':
		report.status = 'rejected'
		report.approver = request.user
		report.approver_comment = comment
		report.approved_date = timezone.now()
		message = 'Disease report rejected'
	else:
		return JsonResponse({'status': 'error', 'message': 'Invalid action'}, status=400)

	report.save()
	return JsonResponse({'status': 'success', 'message': message})




