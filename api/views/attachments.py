from rest_framework import views, status
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from api.serializers import AttachmentSerializer


class AttachmentCreator(views.APIView):
    serializer_class = AttachmentSerializer
    parser_classes = (FileUploadParser,)

    def post(self, request, filename, format=None):
        serializer = AttachmentSerializer(
            data={'path': request.data['file']}
        )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
