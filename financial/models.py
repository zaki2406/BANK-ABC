

# Create your models here.
# financial/models.py
# your_app/models.py
from django.db import models

class FinancialReport(models.Model):
    file = models.FileField(upload_to='financial_reports/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)  # Optional

    def __str__(self):
        return self.file.name
