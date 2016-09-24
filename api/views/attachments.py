from rest_framework import views, status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from api.serializers import AttachmentSerializer


class AttachmentCreator(views.APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        serializer = AttachmentSerializer(data={'path': request.data['file']})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
