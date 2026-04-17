from pathlib import Path
import os
import mimetypes


BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-a5mu8ax7nnw=dw#75o#9x6jfhqdg4d#jgnl%9%n!^hdc2!xus+'
ALLOWED_HOSTS = ['*']
DEBUG = True


INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'app.apps.AppConfig',
	'api.apps.ApiConfig'
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'stoma.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [BASE_DIR / 'templates'],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
			],
		},
	},
]

WSGI_APPLICATION = 'stoma.wsgi.application'

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': BASE_DIR / 'db.sqlite3',
	}
}

AUTH_PASSWORD_VALIDATORS = [
	{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
	{'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
	{'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
	{'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]


AUTH_USER_MODEL = 'api.User'
LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Asia/Vladivostok'
USE_I18N = True
USE_TZ = True
APPEND_SLASH = False

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = ['*']

mimetypes.add_type("application/javascript", ".js", True)
mimetypes.add_type("application/javascript", ".mjs", True)
mimetypes.add_type("text/css", ".css", True)

STATIC_URL = '/static/'
if not DEBUG:
	STATIC_ROOT = os.path.join(BASE_DIR, 'static')
else:
	STATICFILES_DIRS = [
		os.path.join(BASE_DIR, "static"),
	]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
