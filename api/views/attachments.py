from rest_framework import generics
from api.serializers import AttachmentSerializer


class AttachmentCreator(generics.CreateAPIView):
    serializer_class = AttachmentSerializer
