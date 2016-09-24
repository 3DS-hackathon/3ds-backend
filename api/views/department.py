from api.models import Department
from api.serializers import DepartmentSerializer
from .common import RetrieveModelView


class DepartmentView(RetrieveModelView):
    lookup_field = 'id'
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def get_default_id(self):
        return self.request.user.department.id
