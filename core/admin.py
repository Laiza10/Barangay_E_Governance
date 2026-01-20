from django.contrib import admin
from .models import DocumentRequest, Complaint, Announcement

admin.site.register(DocumentRequest)
admin.site.register(Complaint)
admin.site.register(Announcement)
