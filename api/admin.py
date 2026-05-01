from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import (
    User, Document, TypeOfService, Service, Speciality,
    Doctor, DoctorEducationRow, DoctorExperienceRow,
    DoctorCertificate, DoctorKeys, Order
)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('fio', 'phone')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'fio', 'phone', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'fio', 'phone', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'fio', 'phone')
    ordering = ('email',)
    filter_horizontal = ()


class DoctorEducationRowInline(admin.TabularInline):
    model = DoctorEducationRow
    extra = 1


class DoctorExperienceRowInline(admin.TabularInline):
    model = DoctorExperienceRow
    extra = 1


class DoctorCertificateInline(admin.TabularInline):
    model = DoctorCertificate
    extra = 1


class DoctorKeysInline(admin.TabularInline):
    model = DoctorKeys
    extra = 1


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('fio', 'speciality', 'experience')
    list_filter = ('speciality',)
    search_fields = ('fio', 'description')
    inlines = [
        DoctorEducationRowInline,
        DoctorExperienceRowInline,
        DoctorCertificateInline,
        DoctorKeysInline,
    ]


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'file')
    search_fields = ('title',)


@admin.register(TypeOfService)
class TypeOfServiceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'type_of_service')
    list_filter = ('type_of_service',)
    search_fields = ('name', 'description')


@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(DoctorEducationRow)
class DoctorEducationRowAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'description')
    list_filter = ('doctor',)
    search_fields = ('doctor__fio', 'description')


@admin.register(DoctorExperienceRow)
class DoctorExperienceRowAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'description')
    list_filter = ('doctor',)
    search_fields = ('doctor__fio', 'description')


@admin.register(DoctorCertificate)
class DoctorCertificateAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'file')
    list_filter = ('doctor',)
    search_fields = ('doctor__fio',)


@admin.register(DoctorKeys)
class DoctorKeysAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'description')
    list_filter = ('doctor',)
    search_fields = ('doctor__fio', 'description')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('fio', 'email', 'phone', 'date')
    list_filter = ('date',)
    search_fields = ('fio', 'email', 'phone', 'question')
    date_hierarchy = 'date'