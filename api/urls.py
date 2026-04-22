from django.urls import path

from .views import *


urlpatterns = [
    path('login/', login_view),
    path('logout/', logout_view),

    path('api/users/', users_list, name='users_list'),                 # GET
    path('api/users/<int:user_id>/', user_detail, name='user_detail'), # GET
    path('api/users/create/', create_user, name='create_user'),        # POST
    path('api/users/<int:user_id>/update/', update_user, name='update_user'),  # POST / PUT
    path('api/users/<int:user_id>/delete/', delete_user, name='delete_user'),  # POST / DELETE


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
