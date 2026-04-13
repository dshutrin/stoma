from django.urls import path

from .views import (
    login_view,
    logout_view,

    get_all_documents,
    get_document_detail,
    create_document,
    update_document,
    delete_document,

    get_all_specialities,
    get_speciality_detail,
    create_speciality,
    update_speciality,
    delete_speciality,

    get_all_type_of_service,
    get_type_of_service_detail,
    create_type_of_service,
    update_type_of_service,
    delete_type_of_service,

    get_all_services,
    get_service_detail,
    get_services_with_type_of_service,
    create_service,
    update_service,
    delete_service,

    get_all_doctors,
    get_doctor_detail,
    get_doctors_with_specific,
    create_doctor,
    update_doctor,
    delete_doctor,

    get_doctor_education_rows,
    get_doctor_education_row_detail,
    create_doctor_education_row,
    update_doctor_education_row,
    delete_doctor_education_row,

    get_doctor_experience_rows,
    get_doctor_experience_row_detail,
    create_doctor_experience_row,
    update_doctor_experience_row,
    delete_doctor_experience_row,

    get_doctor_certificates,
    get_doctor_certificate_detail,
    create_doctor_certificate,
    update_doctor_certificate,
    delete_doctor_certificate,

    get_doctor_keys,
    get_doctor_key_detail,
    create_doctor_key,
    update_doctor_key,
    delete_doctor_key,

    get_all_orders,
    get_order_detail,
    create_order,
    update_order,
    delete_order,
)


urlpatterns = [
    path('login/', login_view),
    path('logout/', logout_view),

    # documents
    path('documents/', get_all_documents),
    path('documents/<int:document_id>/', get_document_detail),
    path('documents/create/', create_document),
    path('documents/<int:document_id>/update/', update_document),
    path('documents/<int:document_id>/delete/', delete_document),

    # specialities
    path('specialities/', get_all_specialities),
    path('specialities/<int:speciality_id>/', get_speciality_detail),
    path('specialities/create/', create_speciality),
    path('specialities/<int:speciality_id>/update/', update_speciality),
    path('specialities/<int:speciality_id>/delete/', delete_speciality),

    # types of service
    path('types-of-service/', get_all_type_of_service),
    path('types-of-service/<int:type_id>/', get_type_of_service_detail),
    path('types-of-service/create/', create_type_of_service),
    path('types-of-service/<int:type_id>/update/', update_type_of_service),
    path('types-of-service/<int:type_id>/delete/', delete_type_of_service),

    # services
    path('services/', get_all_services),
    path('services/<int:service_id>/', get_service_detail),
    path('services/type/<int:type_of_service_id>/', get_services_with_type_of_service),
    path('services/create/', create_service),
    path('services/<int:service_id>/update/', update_service),
    path('services/<int:service_id>/delete/', delete_service),

    # doctors
    path('doctors/', get_all_doctors),
    path('doctors/<int:doctor_id>/', get_doctor_detail),
    path('doctors/speciality/<int:spec_id>/', get_doctors_with_specific),
    path('doctors/create/', create_doctor),
    path('doctors/<int:doctor_id>/update/', update_doctor),
    path('doctors/<int:doctor_id>/delete/', delete_doctor),

    # doctor education
    path('doctors/<int:doctor_id>/education/', get_doctor_education_rows),
    path('doctors/<int:doctor_id>/education/create/', create_doctor_education_row),
    path('doctor-education/<int:row_id>/', get_doctor_education_row_detail),
    path('doctor-education/<int:row_id>/update/', update_doctor_education_row),
    path('doctor-education/<int:row_id>/delete/', delete_doctor_education_row),

    # doctor experience
    path('doctors/<int:doctor_id>/experience/', get_doctor_experience_rows),
    path('doctors/<int:doctor_id>/experience/create/', create_doctor_experience_row),
    path('doctor-experience/<int:row_id>/', get_doctor_experience_row_detail),
    path('doctor-experience/<int:row_id>/update/', update_doctor_experience_row),
    path('doctor-experience/<int:row_id>/delete/', delete_doctor_experience_row),

    # doctor certificates
    path('doctors/<int:doctor_id>/certificates/', get_doctor_certificates),
    path('doctors/<int:doctor_id>/certificates/create/', create_doctor_certificate),
    path('doctor-certificates/<int:certificate_id>/', get_doctor_certificate_detail),
    path('doctor-certificates/<int:certificate_id>/update/', update_doctor_certificate),
    path('doctor-certificates/<int:certificate_id>/delete/', delete_doctor_certificate),

    # doctor keys
    path('doctors/<int:doctor_id>/keys/', get_doctor_keys),
    path('doctors/<int:doctor_id>/keys/create/', create_doctor_key),
    path('doctor-keys/<int:key_id>/', get_doctor_key_detail),
    path('doctor-keys/<int:key_id>/update/', update_doctor_key),
    path('doctor-keys/<int:key_id>/delete/', delete_doctor_key),

    # orders
    path('orders/', get_all_orders),
    path('orders/<int:order_id>/', get_order_detail),
    path('orders/create/', create_order),
    path('orders/<int:order_id>/update/', update_order),
    path('orders/<int:order_id>/delete/', delete_order),
]
