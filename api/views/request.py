from rest_framework import views, status
from rest_framework.response import Response
from api.serializers import TaskRequestSerializer, RequestSerializer


class RequestCreator(views.APIView):

    def post(self, request, format=None):
        data = {'user_id': request.user.id, **request.data}
        serializer = TaskRequestSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        response_serializer = RequestSerializer(instance=serializer.save())
        return Response(response_serializer.data,
                        status=status.HTTP_201_CREATED)


