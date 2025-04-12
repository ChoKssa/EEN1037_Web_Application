from machinery.models import Machine, Warning
from faults.models import FaultCase
from users.models import User
from rest_framework import permissions, viewsets
from api.serializers import MachineSerializer, WarningSerializer, FaultCaseSerializer, UserSerializer
from api.authentication import ApiKeyAuthentication

class MachineViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows machines to be viewed or edited.
    """
    queryset = Machine.objects.all().order_by('name')
    serializer_class = MachineSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [ApiKeyAuthentication]

class WarningViewSet(viewsets.ModelViewSet):
    """
    API endpoint for warning
    """
    queryset = Warning.objects.all()
    serializer_class = WarningSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [ApiKeyAuthentication]

class FaultCaseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Faults to be viewed or edited.
    """
    queryset = FaultCase.objects.all()
    serializer_class = FaultCaseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [ApiKeyAuthentication]

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [ApiKeyAuthentication]
