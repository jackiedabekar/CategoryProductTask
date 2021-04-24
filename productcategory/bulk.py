from rest_framework.exceptions import ValidationError
import os


def check_for_csv(self,request):
    uploaded_file = []
    if 'upload_file' in request.FILES:
        uploaded_file_data = request.FILES['upload_file']
        ALLOWED_TYPES = ['csv']
        try:
            extension = os.path.splitext(uploaded_file_data.name)[1][1:].lower()
            if extension in ALLOWED_TYPES:
                upload_file = request.data['upload_file']
                return upload_file
            else: 
                raise ValidationError('File types is not allowed')
        except:
            raise ValidationError('Invalid file type')
    else:
        raise ValidationError('Invalid file type')