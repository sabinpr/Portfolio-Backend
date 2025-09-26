from decouple import config, Csv
from pathlib import Path
import dj_database_url
import os

# ------------------------
# BASE
# ------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------
# SECURITY
# ------------------------
SECRET_KEY = config("SECRET_KEY", default="unsafe-secret-key")
ENVIRONMENT = config("ENVIRONMENT", default="local")  # local, railway, render
DEBUG = config("DEBUG", default=(ENVIRONMENT == "local"), cast=bool)

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="localhost,127.0.0.1,.railway.app,.onrender.com",
    cast=Csv(),
)

CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS",
    default="https://portfolio-backend-production-d840.up.railway.app,"
    "https://portfolio-backend-xubo.onrender.com,"
    "https://www.sabinprajapati7.com.np,"
    "http://localhost:8000",
    cast=Csv(),
)

# ------------------------
# APPLICATIONS
# ------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "contact",
    "contactnabin",
    "contactishu",
]

MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ------------------------
# DATABASE
# ------------------------
DATABASES = {
    "default": dj_database_url.config(
        default=config("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=config("DB_SSL", default=False, cast=bool),
    )
}

# ------------------------
# PASSWORD VALIDATION
# ------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ------------------------
# INTERNATIONALIZATION
# ------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ------------------------
# STATIC FILES
# ------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ------------------------
# EMAIL
# ------------------------

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST", default="smtp.sendgrid.net")
EMAIL_PORT = config("EMAIL_PORT", cast=int, default=587)
EMAIL_HOST_USER = config(
    "EMAIL_HOST_USER", default="apikey"
)  # always 'apikey' for SendGrid
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")  # your SendGrid API key
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool, default=True)
EMAIL_USE_SSL = config("EMAIL_USE_SSL", cast=bool, default=False)


DEFAULT_FROM_EMAIL = config(
    "DEFAULT_FROM_EMAIL", default="sabinprajapati.verified@gmail.com"
)

# Custom admin emails
ADMIN_EMAIL = config("ADMIN_EMAIL", default=None)
NABIN_ADMIN_EMAIL = config("NABIN_ADMIN_EMAIL", default=None)
ISHU_ADMIN_EMAIL = config("ISHU_ADMIN_EMAIL", default=None)


# ------------------------
# CORS
# ------------------------
CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS",
    default="http://localhost:5173,https://my-portfolio-rho-bay-gr3zwm7m0v.vercel.app,https://www.sabinprajapati7.com.np,https://www.nabin-prajapati.com.np,https://www.ishushrestha.com.np",
    cast=Csv(),
)


# ------------------------
# LOGGING
# ------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {
        "django": {"handlers": ["console"], "level": "INFO"},
        "contact": {"handlers": ["console"], "level": "INFO"},
    },
}

# ------------------------
# DEFAULT AUTO FIELD
# ------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# SENDGRID API
SENDGRID_API_KEY = config("SENDGRID_API_KEY")
 