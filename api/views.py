import json
import datetime

from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import (
    Document,
    TypeOfService,
    Service,
    Speciality,
    Doctor,
    DoctorEducationRow,
    DoctorExperienceRow,
    DoctorCertificate,
    DoctorKeys,
    Order, User,
)


def method_not_allowed():
    return JsonResponse({'message': 'unavailable method'}, status=400)


def get_request_data(request):
    """
    Поддержка:
    1. application/json
    2. multipart/form-data
    3. x-www-form-urlencoded
    """
    if request.method != 'POST':
        return {}

    content_type = request.content_type or ''
    if 'application/json' in content_type:
        try:
            return json.loads(request.body.decode('utf-8'))
        except Exception:
            return {}

    return request.POST


def as_bool(value):
    return str(value).lower() in ['1', 'true', 'yes', 'on']


def parse_date_safe(date_str):
    try:
        return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    except Exception:
        return None


def serialize_document(document):
    return {
        'id': document.id,
        'title': document.title,
        'file': document.file.url if document.file else '',
    }


def serialize_type_of_service(type_of_service):
    if not type_of_service:
        return None

    return {
        'id': type_of_service.id,
        'name': type_of_service.name,
    }


def serialize_speciality(speciality):
    if not speciality:
        return None

    return {
        'id': speciality.id,
        'name': speciality.name,
    }


def serialize_service(service):
    return {
        'id': service.id,
        'name': service.name,
        'description': service.description,
        'price': str(service.price),
        'image': service.image.url if service.image else '',
        'type_of_service': serialize_type_of_service(service.type_of_service),
    }


def serialize_doctor(doctor):
    return {
        'id': doctor.id,
        'fio': doctor.fio,
        'experience': doctor.experience,
        'speciality': serialize_speciality(doctor.speciality),
        'description': doctor.description,
        'photo': doctor.photo.url if doctor.photo else '',
    }


def serialize_doctor_education_row(row):
    return {
        'id': row.id,
        'doctor_id': row.doctor_id,
        'description': row.description,
    }


def serialize_doctor_experience_row(row):
    return {
        'id': row.id,
        'doctor_id': row.doctor_id,
        'description': row.description,
    }


def serialize_doctor_certificate(certificate):
    return {
        'id': certificate.id,
        'doctor_id': certificate.doctor_id,
        'file': certificate.file.url if certificate.file else '',
    }


def serialize_doctor_key(key):
    return {
        'id': key.id,
        'doctor_id': key.doctor_id,
        'photo': key.photo.url if key.photo else '',
        'description': key.description,
    }


def serialize_order(order):
    return {
        'id': order.id,
        'fio': order.fio,
        'email': order.email,
        'phone': order.phone,
        'date': order.date.strftime('%Y-%m-%d') if order.date else None,
        'question': order.question,
    }


@csrf_exempt
def login_view(request):
    if request.method != 'POST':
        return method_not_allowed()

    data = get_request_data(request)

    username = data.get('username') or data.get('email')
    password = data.get('password')

    if not username or not password:
        return JsonResponse({'message': 'username/email and password required'}, status=400)

    user = authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse({'message': 'login error'}, status=400)

    user_login(request, user)
    return JsonResponse({'message': 'login success'}, status=200)


@csrf_exempt
def logout_view(request):
    if request.method != 'POST':
        return method_not_allowed()

    user_logout(request)
    return JsonResponse({'message': 'logout success'}, status=200)


# =========================
# Document
# =========================
@csrf_exempt
def get_all_documents(request):
    if request.method != 'GET':
        return method_not_allowed()

    documents = Document.objects.all().order_by('id')
    documents_list = [serialize_document(document) for document in documents]

    return JsonResponse({'documents': documents_list}, status=200)

@csrf_exempt
def get_document_detail(request, document_id):
    if request.method != 'GET':
        return method_not_allowed()

    try:
        document = Document.objects.get(id=document_id)
    except Document.DoesNotExist:
        return JsonResponse({'message': 'document not found'}, status=404)

    return JsonResponse({'document': serialize_document(document)}, status=200)


@csrf_exempt
def create_document(request):
    if request.method != 'POST':
        return method_not_allowed()

    data = get_request_data(request)

    title = data.get('title')
    file_obj = request.FILES.get('file')

    if not title:
        return JsonResponse({'message': 'title required'}, status=400)

    if not file_obj:
        return JsonResponse({'message': 'file required'}, status=400)

    document = Document.objects.create(
        title=title,
        file=file_obj,
    )

    return JsonResponse({
        'message': 'document created successfully',
        'document': serialize_document(document),
    }, status=201)


@csrf_exempt
def update_document(request, document_id):
    if request.method != 'POST':
        return method_not_allowed()

    try:
        document = Document.objects.get(id=document_id)
    except Document.DoesNotExist:
        return JsonResponse({'message': 'document not found'}, status=404)

    data = get_request_data(request)

    title = data.get('title')
    file_clear = data.get('file_clear')

    if title is not None:
        document.title = title

    if as_bool(file_clear):
        if document.file:
            document.file.delete(save=False)
        document.file = None

    if 'file' in request.FILES:
        if document.file:
            document.file.delete(save=False)
        document.file = request.FILES['file']

    document.save()

    return JsonResponse({
        'message': 'document updated successfully',
        'document': serialize_document(document),
    }, status=200)


@csrf_exempt
def delete_document(request, document_id):
    if request.method != 'POST':
        return method_not_allowed()

    try:
        document = Document.objects.get(id=document_id)
    except Document.DoesNotExist:
        return JsonResponse({'message': 'document not found'}, status=404)

    if document.file:
        document.file.delete(save=False)

    document.delete()

    return JsonResponse({'message': 'document deleted successfully'}, status=200)


# =========================
# Speciality
# =========================
@csrf_exempt
def get_all_specialities(request):
    if request.method != 'GET':
        return method_not_allowed()

    specialities = Speciality.objects.all().order_by('id')
    specialities_list = [serialize_speciality(speciality) for speciality in specialities]

    return JsonResponse({'specialities': specialities_list}, status=200)

@csrf_exempt
def get_speciality_detail(request, speciality_id):
    if request.method != 'GET':
        return method_not_allowed()

    try:
        speciality = Speciality.objects.get(id=speciality_id)
    except Speciality.DoesNotExist:
        return JsonResponse({'message': 'speciality not found'}, status=404)

    return JsonResponse({'speciality': serialize_speciality(speciality)}, status=200)


@csrf_exempt
def create_speciality(request):
    if request.method != 'POST':
        return method_not_allowed()

    data = get_request_data(request)
    name = data.get('name')

    if not name:
        return JsonResponse({'message': 'name required'}, status=400)

    speciality = Speciality.objects.create(name=name)

    return JsonResponse({
        'message': 'speciality created successfully',
        'speciality': serialize_speciality(speciality),
    }, status=201)


@csrf_exempt
def update_speciality(request, speciality_id):
    if request.method != 'POST':
        return method_not_allowed()

    try:
        speciality = Speciality.objects.get(id=speciality_id)
    except Speciality.DoesNotExist:
        return JsonResponse({'message': 'speciality not found'}, status=404)

    data = get_request_data(request)
    name = data.get('name')

    if name is not None:
        speciality.name = name

    speciality.save()

    return JsonResponse({
        'message': 'speciality updated successfully',
        'speciality': serialize_speciality(speciality),
    }, status=200)


@csrf_exempt
def delete_speciality(request, speciality_id):
    if request.method != 'POST':
        return method_not_allowed()

    try:
        speciality = Speciality.objects.get(id=speciality_id)
    except Speciality.DoesNotExist:
        return JsonResponse({'message': 'speciality not found'}, status=404)

    speciality.delete()

    return JsonResponse({'message': 'speciality deleted successfully'}, status=200)


# =========================
# TypeOfService
# =========================
@csrf_exempt
def get_all_type_of_service(request):
    if request.method != 'GET':
        return method_not_allowed()

    types = TypeOfService.objects.all().order_by('id')
    types_list = [serialize_type_of_service(type_obj) for type_obj in types]

    return JsonResponse({'types': types_list}, status=200)

@csrf_exempt
def get_type_of_service_detail(request, type_id):
    if request.method != 'GET':
        return method_not_allowed()

    try:
        type_obj = TypeOfService.objects.get(id=type_id)
    except TypeOfService.DoesNotExist:
        return JsonResponse({'message': 'type of service not found'}, status=404)

    return JsonResponse({'type': serialize_type_of_service(type_obj)}, status=200)


@csrf_exempt
def create_type_of_service(request):
    if request.method != 'POST':
        return method_not_allowed()

    data = get_request_data(request)
    name = data.get('name')

    if not name:
        return JsonResponse({'message': 'name required'}, status=400)

    type_obj = TypeOfService.objects.create(name=name)

    return JsonResponse({
        'message': 'type of service created successfully',
        'type': serialize_type_of_service(type_obj),
    }, status=201)


@csrf_exempt
def update_type_of_service(request, type_id):
    if request.method != 'POST':
        return method_not_allowed()

    try:
        type_obj = TypeOfService.objects.get(id=type_id)
    except TypeOfService.DoesNotExist:
        return JsonResponse({'message': 'type of service not found'}, status=404)

    data = get_request_data(request)
    name = data.get('name')

    if name is not None:
        type_obj.name = name

    type_obj.save()

    return JsonResponse({
        'message': 'type of service updated successfully',
        'type': serialize_type_of_service(type_obj),
    }, status=200)


@csrf_exempt
def delete_type_of_service(request, type_id):
    if request.method != 'POST':
        return method_not_allowed()

    try:
        type_obj = TypeOfService.objects.get(id=type_id)
    except TypeOfService.DoesNotExist:
        return JsonResponse({'message': 'type of service not found'}, status=404)

    type_obj.delete()

    return JsonResponse({'message': 'type of service deleted successfully'}, status=200)


# =========================
# Service
# =========================
@csrf_exempt
def get_all_services(request):
    if request.method != 'GET':
        return method_not_allowed()

    services = Service.objects.select_related('type_of_service').all().order_by('id')
    services_list = [serialize_service(service) for service in services]

    return JsonResponse({'services': services_list}, status=200)

@csrf_exempt
def get_service_detail(request, service_id):
    if request.method != 'GET':
        return method_not_allowed()

    try:
        service = Service.objects.select_related('type_of_service').get(id=service_id)
    except Service.DoesNotExist:
        return JsonResponse({'message': 'service not found'}, status=404)

    return JsonResponse({'service': serialize_service(service)}, status=200)

@csrf_exempt
def get_services_with_type_of_service(request, type_of_service_id):
    if request.method != 'GET':
        return method_not_allowed()

    services = Service.objects.select_related('type_of_service').filter(
        type_of_service__id=type_of_service_id
    ).order_by('id')
    services_list = [serialize_service(service) for service in services]

    return JsonResponse({'services': services_list}, status=200)


@csrf_exempt
def create_service(request):
    if request.method != 'POST':
        return method_not_allowed()

    data = get_request_data(request)

    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    type_of_service_id = data.get('type_of_service_id')
    image = request.FILES.get('image')

    if not name or not description or price in [None, '']:
        return JsonResponse({'message': 'name, description, price required'}, status=400)

    if not image:
        return JsonResponse({'message': 'image required'}, status=400)

    type_of_service = None
    if type_of_service_id not in [None, '']:
        try:
            type_of_service = TypeOfService.objects.get(id=type_of_service_id)
        except TypeOfService.DoesNotExist:
            return JsonResponse({'message': 'type of service not found'}, status=404)

    service = Service.objects.create(
        name=name,
        description=description,
        price=price,
        image=image,
        type_of_service=type_of_service,
    )

    return JsonResponse({
        'message': 'service created successfully',
        'service': serialize_service(service),
    }, status=201)


@csrf_exempt
def update_service(request, service_id):
    if request.method != 'POST':
        return method_not_allowed()

    try:
        service = Service.objects.get(id=service_id)
    except Service.DoesNotExist:
        return JsonResponse({'message': 'service not found'}, status=404)

    data = get_request_data(request)

    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    type_of_service_id = data.get('type_of_service_id')
    image_clear = data.get('image_clear')

    if name is not None:
        service.name = name

    if description is not None:
        service.description = description

    if price not in [None, '']:
        service.price = price

    if type_of_service_id is not None:
        if type_of_service_id == '':
            service.type_of_service = None
        else:
            try:
                service.type_of_service = TypeOfService.objects.get(id=type_of_service_id)
            except TypeOfService.DoesNotExist:
                return JsonResponse({'message': 'type of service not found'}, status=404)

    if as_bool(image_clear):
        if service.image:
            service.image.delete(save=False)
        service.image = None

    if 'image' in request.FILES:
        if service.image:
            service.image.delete(save=False)
        service.image = request.FILES['image']

    service.save()

    return JsonResponse({
        'message': 'service updated successfully',
        'service': serialize_service(service),
    }, status=200)


@csrf_exempt
def delete_service(request, service_id):
    if request.method != 'POST':
        return method_not_allowed()

    try:
        service = Service.objects.get(id=service_id)
    except Service.DoesNotExist:
        return JsonResponse({'message': 'service not found'}, status=404)

    if service.image:
        service.image.delete(save=False)

    service.delete()

    return JsonResponse({'message': 'service deleted successfully'}, status=200)


# =========================
# Doctor
# =========================
@csrf_exempt
def get_all_doctors(request):
    if request.method != 'GET':
        return method_not_allowed()

    doctors = Doctor.objects.select_related('speciality').all().order_by('id')
    doctors_list = [serialize_doctor(doctor) for doctor in doctors]

    return JsonResponse({'doctors': doctors_list}, status=200)

@csrf_exempt
def get_doctor_detail(request, doctor_id):
    if request.method != 'GET':
        return method_not_allowed()

    try:
        doctor = Doctor.objects.select_related('speciality').get(id=doctor_id)
    except Doctor.DoesNotExist:
        return JsonResponse({'message': 'doctor not found'}, status=404)

    education_rows = DoctorEducationRow.objects.filter(doctor_id=doctor.id).order_by('id')
    experience_rows = DoctorExperienceRow.objects.filter(doctor_id=doctor.id).order_by('id')
    certificates = DoctorCertificate.objects.filter(doctor_id=doctor.id).order_by('id')
    keys = DoctorKeys.objects.filter(doctor_id=doctor.id).order_by('id')

    return JsonResponse({
        'doctor': {
            **serialize_doctor(doctor),
            'education_rows': [serialize_doctor_education_row(row) for row in education_rows],
            'experience_rows': [serialize_doctor_experience_row(row) for row in experience_rows],
            'certificates': [serialize_doctor_certificate(item) for item in certificates],
            'keys': [serialize_doctor_key(item) for item in keys],
        }
    }, status=200)

@csrf_exempt
def get_doctors_with_specific(request, spec_id):
    if request.method != 'GET':
        return method_not_allowed()

    doctors = Doctor.objects.select_related('speciality').filter(speciality__id=spec_id).order_by('id')
    doctors_list = [serialize_doctor(doctor) for doctor in doctors]

    return JsonResponse({'doctors': doctors_list}, status=200)


@csrf_exempt
def create_doctor(request):
    if request.method != 'POST':
        return method_not_allowed()

    data = get_request_data(request)

    fio = data.get('fio')
    experience = data.get('experience')
    speciality_id = data.get('speciality_id')
    description = data.get('description')
    photo = request.FILES.get('photo')

    if not fio or experience in [None, ''] or not description:
        return JsonResponse({'message': 'fio, experience, description required'}, status=400)

    speciality = None
    if speciality_id not in [None, '']:
        try:
            speciality = Speciality.objects.get(id=speciality_id)
        except Speciality.DoesNotExist:
            return JsonResponse({'message': 'speciality not found'}, status=404)

    doctor = Doctor.objects.create(
        fio=fio,
        experience=experience,
        speciality=speciality,
        description=description,
        photo=photo,
    )

    return JsonResponse({
        'message': 'doctor created successfully',
        'doctor': serialize_doctor(doctor),
    }, status=201)


@csrf_exempt
def update_doctor(request, doctor_id):
    if request.method != 'POST':
        return method_not_allowed()

    try:
        doctor = Doctor.objects.get(id=doctor_id)
    except Doctor.DoesNotExist:
        return JsonResponse({'message': 'doctor not found'}, status=404)

    data = get_request_data(request)

    fio = data.get('fio')
    experience = data.get('experience')
    speciality_id = data.get('speciality_id')
    description = data.get('description')
    photo_clear = data.get('photo_clear')

    if fio is not None:
        doctor.fio = fio

    if experience not in [None, '']:
        doctor.experience = experience

    if description is not None:
        doctor.description = description

    if speciality_id is not None:
        if speciality_id == '':
            doctor.speciality = None
        else:
            try:
                doctor.speciality = Speciality.objects.get(id=speciality_id)
            except Speciality.DoesNotExist:
                return JsonResponse({'message': 'speciality not found'}, status=404)

    if as_bool(photo_clear):
        if doctor.photo:
            doctor.photo.delete(save=False)
        doctor.photo = None

    if 'photo' in request.FILES:
        if doctor.photo:
            doctor.photo.delete(save=False)
        doctor.photo = request.FILES['photo']

    doctor.save()

    return JsonResponse({
        'message': 'doctor updated successfully',
        'doctor': serialize_doctor(doctor),
    }, status=200)


@csrf_exempt
def delete_doctor(request, doctor_id):
    if request.method != 'POST':
        return method_not_allowed()

    try:
        doctor = Doctor.objects.get(id=doctor_id)
    except Doctor.DoesNotExist:
        return JsonResponse({'message': 'doctor not found'}, status=404)

    if doctor.photo:
        doctor.photo.delete(save=False)

    doctor.delete()

    return JsonResponse({'message': 'doctor deleted successfully'}, status=200)


# =========================
# DoctorEducationRow
# =========================
@csrf_exempt
def get_doctor_education_rows(request, doctor_id):
    if request.method != 'GET':
        return method_not_allowed()

    rows = DoctorEducationRow.objects.filter(doctor_id=doctor_id).order_by('id')
    rows_list = [serialize_doctor_education_row(row) for row in rows]

    return JsonResponse({'education_rows': rows_list}, status=200)

@csrf_exempt
def get_doctor_education_row_detail(request, row_id):
    if request.method != 'GET':
        return method_not_allowed()

    try:
        row = DoctorEducationRow.objects.get(id=row_id)
    except DoctorEducationRow.DoesNotExist:
        return JsonResponse({'message': 'education row not found'}, status=404)

    return JsonResponse({'education_row': serialize_doctor_education_row(row)}, status=200)


@csrf_exempt
def create_doctor_education_row(request, doctor_id):
    if request.method != 'POST':
        return method_not_allowed()

    try:
        doctor = Doctor.objects.get(id=doctor_id)
    except Doctor.DoesNotExist:
        return JsonResponse({'message': 'doctor not found'}, status=404)

    data = get_request_data(request)
    description = data.get('description')

    if not description:
        return JsonResponse({'message': 'description required'}, status=400)

    row = DoctorEducationRow.objects.create(
        doctor=doctor,
        description=description,
    )

    return JsonResponse({
        'message': 'doctor education row created successfully',
        'education_row': serialize_doctor_education_row(row),
    }, status=201)


@csrf_exempt
def update_doctor_education_row(request, row_id):
    if request.method != 'POST':
        return method_not_allowed()

    try:
        row = DoctorEducationRow.objects.get(id=row_id)
    except DoctorEducationRow.DoesNotExist:
        return JsonResponse({'message': 'education row not found'}, status=404)

    data = get_request_data(request)
    description = data.get('description')
    doctor_id = data.get('doctor_id')

    if description is not None:
        row.description = description

    if doctor_id is not None:
        try:
            row.doctor = Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            return JsonResponse({'message': 'doctor not found'}, status=404)

    row.save()

    return JsonResponse({
        'message': 'doctor education row updated successfully',
        'education_row': serialize_doctor_education_row(row),
    }, status=200)


@csrf_exempt
def delete_doctor_education_row(request, row_id):
    if request.method != 'POST':
        return method_not_allowed()

    try:
        row = DoctorEducationRow.objects.get(id=row_id)
    except DoctorEducationRow.DoesNotExist:
        return JsonResponse({'message': 'education row not found'}, status=404)

    row.delete()

    return JsonResponse({'message': 'doctor education row deleted successfully'}, status=200)


# =========================
# DoctorExperienceRow
# =========================
@csrf_exempt
def get_doctor_experience_rows(request, doctor_id):
    if request.method != 'GET':
        return method_not_allowed()

    rows = DoctorExperienceRow.objects.filter(doctor_id=doctor_id).order_by('id')
    rows_list = [serialize_doctor_experience_row(row) for row in rows]

    return JsonResponse({'experience_rows': rows_list}, status=200)

@csrf_exempt
def get_doctor_experience_row_detail(request, row_id):
    if request.method != 'GET':
        return method_not_allowed()

    try:
        row = DoctorExperienceRow.objects.get(id=row_id)
    except DoctorExperienceRow.DoesNotExist:
        return JsonResponse({'message': 'experience row not found'}, status=404)

    return JsonResponse({'experience_row': serialize_doctor_experience_row(row)}, status=200)


@csrf_exempt
def create_doctor_experience_row(request, doctor_id):
    if request.method != 'POST':
        return method_not_allowed()

    try:
        doctor = Doctor.objects.get(id=doctor_id)
    except Doctor.DoesNotExist:
        return JsonResponse({'message': 'doctor not found'}, status=404)

    data = get_request_data(request)
    description = data.get('description')

    if not description:
        return JsonResponse({'message': 'description required'}, status=400)

    row = DoctorExperienceRow.objects.create(
        doctor=doctor,
        description=description,
    )

    return JsonResponse({
        'message': 'doctor experience row created successfully',
        'experience_row': serialize_doctor_experience_row(row),
    }, status=201)


@csrf_exempt
def update_doctor_experience_row(request, row_id):
    if request.method != 'POST':
        return method_not_allowed()

    try:
        row = DoctorExperienceRow.objects.get(id=row_id)
    except DoctorExperienceRow.DoesNotExist:
        return JsonResponse({'message': 'experience row not found'}, status=404)

    data = get_request_data(request)
    description = data.get('description')
    doctor_id = data.get('doctor_id')

    if description is not None:
        row.description = description

    if doctor_id is not None:
        try:
            row.doctor = Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            return JsonResponse({'message': 'doctor not found'}, status=404)

    row.save()

    return JsonResponse({
        'message': 'doctor experience row updated successfully',
        'experience_row': serialize_doctor_experience_row(row),
    }, status=200)


@csrf_exempt
def delete_doctor_experience_row(request, row_id):
    if request.method != 'POST':
        return method_not_allowed()

    try:
        row = DoctorExperienceRow.objects.get(id=row_id)
    except DoctorExperienceRow.DoesNotExist:
        return JsonResponse({'message': 'experience row not found'}, status=404)

    row.delete()

    return JsonResponse({'message': 'doctor experience row deleted successfully'}, status=200)


# =========================
# DoctorCertificate
# =========================
@csrf_exempt
def get_doctor_certificates(request, doctor_id):
    if request.method != 'GET':
        return method_not_allowed()

    certificates = DoctorCertificate.objects.filter(doctor_id=doctor_id).order_by('id')
    certificates_list = [serialize_doctor_certificate(item) for item in certificates]

    return JsonResponse({'certificates': certificates_list}, status=200)

@csrf_exempt
def get_doctor_certificate_detail(request, certificate_id):
    if request.method != 'GET':
        return method_not_allowed()

    try:
        certificate = DoctorCertificate.objects.get(id=certificate_id)
    except DoctorCertificate.DoesNotExist:
        return JsonResponse({'message': 'doctor certificate not found'}, status=404)

    return JsonResponse({'certificate': serialize_doctor_certificate(certificate)}, status=200)


@csrf_exempt
def create_doctor_certificate(request, doctor_id):
    if request.method != 'POST':
        return method_not_allowed()

    try:
        doctor = Doctor.objects.get(id=doctor_id)
    except Doctor.DoesNotExist:
        return JsonResponse({'message': 'doctor not found'}, status=404)

    file_obj = request.FILES.get('file')
    if not file_obj:
        return JsonResponse({'message': 'file required'}, status=400)

    certificate = DoctorCertificate.objects.create(
        doctor=doctor,
        file=file_obj,
    )

    return JsonResponse({
        'message': 'doctor certificate created successfully',
        'certificate': serialize_doctor_certificate(certificate),
    }, status=201)


@csrf_exempt
def update_doctor_certificate(request, certificate_id):
    if request.method != 'POST':
        return method_not_allowed()

    try:
        certificate = DoctorCertificate.objects.get(id=certificate_id)
    except DoctorCertificate.DoesNotExist:
        return JsonResponse({'message': 'doctor certificate not found'}, status=404)

    data = get_request_data(request)
    doctor_id = data.get('doctor_id')
    file_clear = data.get('file_clear')

    if doctor_id is not None:
        try:
            certificate.doctor = Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            return JsonResponse({'message': 'doctor not found'}, status=404)

    if as_bool(file_clear):
        if certificate.file:
            certificate.file.delete(save=False)
        certificate.file = None

    if 'file' in request.FILES:
        if certificate.file:
            certificate.file.delete(save=False)
        certificate.file = request.FILES['file']

    certificate.save()

    return JsonResponse({
        'message': 'doctor certificate updated successfully',
        'certificate': serialize_doctor_certificate(certificate),
    }, status=200)


@csrf_exempt
def delete_doctor_certificate(request, certificate_id):
    if request.method != 'POST':
        return method_not_allowed()

    try:
        certificate = DoctorCertificate.objects.get(id=certificate_id)
    except DoctorCertificate.DoesNotExist:
        return JsonResponse({'message': 'doctor certificate not found'}, status=404)

    if certificate.file:
        certificate.file.delete(save=False)

    certificate.delete()

    return JsonResponse({'message': 'doctor certificate deleted successfully'}, status=200)


# =========================
# DoctorKeys
# =========================
@csrf_exempt
def get_doctor_keys(request, doctor_id):
    if request.method != 'GET':
        return method_not_allowed()

    keys = DoctorKeys.objects.filter(doctor_id=doctor_id).order_by('id')
    keys_list = [serialize_doctor_key(item) for item in keys]

    return JsonResponse({'keys': keys_list}, status=200)

@csrf_exempt
def get_doctor_key_detail(request, key_id):
    if request.method != 'GET':
        return method_not_allowed()

    try:
        key = DoctorKeys.objects.get(id=key_id)
    except DoctorKeys.DoesNotExist:
        return JsonResponse({'message': 'doctor key not found'}, status=404)

    return JsonResponse({'key': serialize_doctor_key(key)}, status=200)


@csrf_exempt
def create_doctor_key(request, doctor_id):
    if request.method != 'POST':
        return method_not_allowed()

    try:
        doctor = Doctor.objects.get(id=doctor_id)
    except Doctor.DoesNotExist:
        return JsonResponse({'message': 'doctor not found'}, status=404)

    data = get_request_data(request)
    description = data.get('description')
    photo = request.FILES.get('photo')

    if not description:
        return JsonResponse({'message': 'description required'}, status=400)

    if not photo:
        return JsonResponse({'message': 'photo required'}, status=400)

    key = DoctorKeys.objects.create(
        doctor=doctor,
        description=description,
        photo=photo,
    )

    return JsonResponse({
        'message': 'doctor key created successfully',
        'key': serialize_doctor_key(key),
    }, status=201)


@csrf_exempt
def update_doctor_key(request, key_id):
    if request.method != 'POST':
        return method_not_allowed()

    try:
        key = DoctorKeys.objects.get(id=key_id)
    except DoctorKeys.DoesNotExist:
        return JsonResponse({'message': 'doctor key not found'}, status=404)

    data = get_request_data(request)
    description = data.get('description')
    doctor_id = data.get('doctor_id')
    photo_clear = data.get('photo_clear')

    if description is not None:
        key.description = description

    if doctor_id is not None:
        try:
            key.doctor = Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            return JsonResponse({'message': 'doctor not found'}, status=404)

    if as_bool(photo_clear):
        if key.photo:
            key.photo.delete(save=False)
        key.photo = None

    if 'photo' in request.FILES:
        if key.photo:
            key.photo.delete(save=False)
        key.photo = request.FILES['photo']

    key.save()

    return JsonResponse({
        'message': 'doctor key updated successfully',
        'key': serialize_doctor_key(key),
    }, status=200)


@csrf_exempt
def delete_doctor_key(request, key_id):
    if request.method != 'POST':
        return method_not_allowed()

    try:
        key = DoctorKeys.objects.get(id=key_id)
    except DoctorKeys.DoesNotExist:
        return JsonResponse({'message': 'doctor key not found'}, status=404)

    if key.photo:
        key.photo.delete(save=False)

    key.delete()

    return JsonResponse({'message': 'doctor key deleted successfully'}, status=200)


# =========================
# Order
# =========================
@csrf_exempt
def get_all_orders(request):
    if request.method != 'GET':
        return method_not_allowed()

    orders = Order.objects.all().order_by('-id')
    orders_list = [serialize_order(order) for order in orders]

    return JsonResponse({'orders': orders_list}, status=200)

@csrf_exempt
def get_order_detail(request, order_id):
    if request.method != 'GET':
        return method_not_allowed()

    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return JsonResponse({'message': 'order not found'}, status=404)

    return JsonResponse({'order': serialize_order(order)}, status=200)


@csrf_exempt
def create_order(request):
    if request.method != 'POST':
        return method_not_allowed()

    data = get_request_data(request)

    fio = data.get('fio')
    email = data.get('email')
    phone = data.get('phone')
    date_str = data.get('date')
    question = data.get('question')

    if not fio or not email or not phone or not date_str or not question:
        return JsonResponse({'message': 'fio, email, phone, date, question required'}, status=400)

    order_date = parse_date_safe(date_str)
    if not order_date:
        return JsonResponse({'message': 'date must be in format YYYY-MM-DD'}, status=400)

    order = Order.objects.create(
        fio=fio,
        email=email,
        phone=phone,
        date=order_date,
        question=question,
    )

    return JsonResponse({
        'message': 'order created successfully',
        'order': serialize_order(order),
    }, status=201)


@csrf_exempt
def update_order(request, order_id):
    if request.method != 'POST':
        return method_not_allowed()

    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return JsonResponse({'message': 'order not found'}, status=404)

    data = get_request_data(request)

    fio = data.get('fio')
    email = data.get('email')
    phone = data.get('phone')
    date_str = data.get('date')
    question = data.get('question')

    if fio is not None:
        order.fio = fio

    if email is not None:
        order.email = email

    if phone is not None:
        order.phone = phone

    if question is not None:
        order.question = question

    if date_str is not None:
        parsed_date = parse_date_safe(date_str)
        if not parsed_date:
            return JsonResponse({'message': 'date must be in format YYYY-MM-DD'}, status=400)
        order.date = parsed_date

    order.save()

    return JsonResponse({
        'message': 'order updated successfully',
        'order': serialize_order(order),
    }, status=200)


@csrf_exempt
def delete_order(request, order_id):
    if request.method != 'POST':
        return method_not_allowed()

    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return JsonResponse({'message': 'order not found'}, status=404)

    order.delete()

    return JsonResponse({'message': 'order deleted successfully'}, status=200)


def json_error(message, status=400):
    return JsonResponse({
        'ok': False,
        'error': message
    }, status=status)


def json_success(data=None, status=200):
    return JsonResponse({
        'ok': True,
        'data': data
    }, status=status)


def parse_json_body(request):
    try:
        body = request.body.decode('utf-8')
        return json.loads(body) if body else {}
    except Exception:
        return None


def user_to_dict(user):
    return {
        'id': user.id,
        'email': user.email,
        'fio': user.fio,
        'phone': user.phone,
    }


@require_http_methods(["GET"])
def users_list(request):
    users = User.objects.all().order_by('id')
    return json_success([user_to_dict(user) for user in users])


@require_http_methods(["GET"])
def user_detail(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return json_error('Пользователь не найден', status=404)

    return json_success(user_to_dict(user))


@csrf_exempt
@require_http_methods(["POST"])
def create_user(request):
    data = parse_json_body(request)
    if data is None:
        return json_error('Некорректный JSON')

    email = (data.get('email') or '').strip()
    fio = (data.get('fio') or '').strip()
    phone = (data.get('phone') or '').strip()
    password = data.get('password')

    if not email:
        return json_error('Поле email обязательно')

    if not password:
        return json_error('Поле password обязательно')

    if User.objects.filter(email=email).exists():
        return json_error('Пользователь с таким email уже существует')

    user = User(
        email=email,
        fio=fio if fio else None,
        phone=phone if phone else None,
    )
    user.set_password(password)
    user.save()

    return json_success(user_to_dict(user), status=201)


@csrf_exempt
@require_http_methods(["POST", "PUT", "PATCH"])
def update_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return json_error('Пользователь не найден', status=404)

    data = parse_json_body(request)
    if data is None:
        return json_error('Некорректный JSON')

    if 'email' in data:
        email = (data.get('email') or '').strip()

        if not email:
            return json_error('Поле email не может быть пустым')

        if User.objects.filter(email=email).exclude(id=user.id).exists():
            return json_error('Пользователь с таким email уже существует')

        user.email = email

    if 'fio' in data:
        fio = (data.get('fio') or '').strip()
        user.fio = fio if fio else None

    if 'phone' in data:
        phone = (data.get('phone') or '').strip()
        user.phone = phone if phone else None

    if 'password' in data:
        password = data.get('password')
        if not password:
            return json_error('Поле password не может быть пустым')
        user.set_password(password)

    user.save()

    return json_success(user_to_dict(user))


@csrf_exempt
@require_http_methods(["POST", "DELETE"])
def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return json_error('Пользователь не найден', status=404)

    user.delete()

    return json_success({
        'message': 'Пользователь удалён',
        'id': user_id
    })
