from rest_framework import viewsets
from .models import Tutor
from .serializers import TutorSerializer

class TutorViewSet(viewsets.ModelViewSet):
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer
