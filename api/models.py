from django.db.models import *

from django.contrib.auth.models import AbstractBaseUser

from .managers import CustomUserManager


class User(AbstractBaseUser):
	"""
		Модель пользователя, используется для авторизации
	"""

	email = EmailField(unique=True, null=True, default=None, blank=True)
	fio = CharField(verbose_name='ФИО', max_length=255, null=True, default=None)
	phone = CharField(verbose_name='Номер телефона', null=True, default=None, max_length=30, blank=True)

	is_staff = BooleanField(default=False)
	is_superuser = BooleanField(default=False)
	is_active = BooleanField(default=True)

	objects = CustomUserManager()
	USERNAME_FIELD = 'email'

	def has_perm(self, perm, obj=None):
		return self.is_superuser

	def has_module_perms(self, app_label):
		return self.is_superuser

	@staticmethod
	def get_privs():
		return []

	class Meta:
		db_table = 'auth_user'
		verbose_name = 'Пользователь'
		verbose_name_plural = 'Пользователи'

	def __str__(self):
		return f'{self.fio}'


class Document(Model):
	title = CharField(max_length=255, verbose_name='Название документа')
	file = FileField(upload_to='documents', verbose_name='Файл', null=False)

	class Meta:
		verbose_name = 'Документ организации'
		verbose_name_plural = 'Документы организации'


class TypeOfService(Model):
	name = CharField(max_length=255, verbose_name='Название')

	class Meta:
		verbose_name = 'Вид услуг'
		verbose_name_plural = 'Виды услуг'


class Service(Model):
	name = CharField(max_length=255, verbose_name='Наименование услуги')
	description = TextField(verbose_name='Описание')
	price = DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость')
	image = ImageField(upload_to='service_images', verbose_name='Изображение')
	type_of_service = ForeignKey(TypeOfService, on_delete=SET_NULL, verbose_name='Вид услуг')

	class Meta:
		verbose_name = 'Услуга'
		verbose_name_plural = 'Услуги'


class Speciality(Model):
	name = CharField(verbose_name='Специальность', max_length=255)

	class Meta:
		verbose_name = 'Специальность'
		verbose_name_plural = 'Специальности'


class Doctor(Model):
	fio = CharField(max_length=150, verbose_name='ФИО')
	experience = PositiveIntegerField(verbose_name='Стаж (в годах)')
	speciality = ForeignKey(Speciality, on_delete=SET_NULL, null=True, verbose_name='Специальность')
	description = TextField(verbose_name='Краткое описание')

	class Meta:
		verbose_name = 'Врач'
		verbose_name_plural = 'Врачи'


class DoctorEducationRow(Model):
	doctor = ForeignKey(Doctor, on_delete=CASCADE)
	description = TextField()

	class Meta:
		verbose_name = 'Запись об образовании специалиста'
		verbose_name_plural = 'Записи об образовании специалистов'


class DoctorExperienceRow(Model):
	doctor = ForeignKey(Doctor, on_delete=CASCADE)
	description = TextField()

	class Meta:
		verbose_name = 'Запись об образовании специалиста'
		verbose_name_plural = 'Записи об образовании специалистов'


class DoctorCertificate(Model):
	file = FileField(upload_to='doctors_certificates')
	doctor = ForeignKey(Doctor, on_delete=CASCADE, verbose_name='Врач')

	class Meta:
		verbose_name = 'Сертификат специалиста'
		verbose_name_plural = 'Сертификаты специалистов'


class DoctorKeys(Model):
	photo = ImageField(upload_to='keys_photos', verbose_name='Изображение')
	description = TextField(verbose_name='Описание')
	doctor = ForeignKey(Doctor, on_delete=CASCADE, verbose_name='Врач')

	class Meta:
		verbose_name = 'Кейс специалиста'
		verbose_name_plural = 'Кейсы специалистов'


class Order(Model):
	fio = CharField(max_length=255, verbose_name='ФИО')
	email = EmailField(verbose_name='email')
	phone = CharField(max_length=20, verbose_name='phone')
	date = DateField(verbose_name='Предварительная дата')
	question = CharField(max_length=2048, verbose_name='Текст обращения')

	class Meta:
		verbose_name = 'Заявка на приём'
		verbose_name_plural = 'Заявки на приём'
