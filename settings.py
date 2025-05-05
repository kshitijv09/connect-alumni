# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Using Gmail SMTP server
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = '211118@iiitt.ac.in'  # Add your Gmail address here
EMAIL_HOST_PASSWORD = 'surajpura'  # Add your Gmail app password here
DEFAULT_FROM_EMAIL = '211118@iiitt.ac.in'  # Add your Gmail address here