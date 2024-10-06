# your_app/serializers.py
#from rest_framework import serializers

#class FinancialDataSerializer(serializers.Serializer):
#    file = serializers.FileField()


# your_app/serializers.py
from rest_framework import serializers
import base64
from django.core.files.base import ContentFile

class Base64PDFFileField(serializers.FileField):
    def to_internal_value(self, data):
        # Check if this is a base64 string
        if isinstance(data, str) and data.startswith('data:application/octet-stream;base64,'):

            data = data.replace('application/octet-stream','application/pdf')

            # Strip the base64 header and decode the data
            format, pdfstr = data.split(';base64,')
            ext = format.split('/')[-1]
            file_name = f'uploaded_file.{ext}'
            data = ContentFile(base64.b64decode(pdfstr), name=file_name)
        
        return super(Base64PDFFileField, self).to_internal_value(data)

class FinancialDataSerializer(serializers.Serializer):
    file = Base64PDFFileField()
