from django.contrib import admin
from .models import QAThread, QAMessage
admin.site.register(QAThread)
admin.site.register(QAMessage)
