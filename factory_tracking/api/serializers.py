from machinery.models import Machine, Warning
from faults.models import FaultCase
from users.models import User
from rest_framework import serializers

class MachineSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Machine
        fields = ['name', 'status', 'created_at', 'updated_at']

class WarningSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Warning
        fields = ['machine', 'message', 'added_by', 'created_at']

class FaultCaseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FaultCase
        fields = ['machine', 'reported_by', 'description', 'status']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['role']

