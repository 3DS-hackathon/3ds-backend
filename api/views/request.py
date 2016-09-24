from rest_framework import generics
from api.serializers import RequestSerializer


class RequestCreator(generics.CreateAPIView):
    serializer_class = RequestSerializer



