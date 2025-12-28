# subjects/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from service_section.Subject.models import Subject

@api_view(['GET'])
def list_subjects(request):
    subjects = Subject.objects.all().values('id', 'name')
    return Response(list(subjects))
