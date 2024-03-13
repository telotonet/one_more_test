from rest_framework import serializers
from .models import Event, Organization
from accounts.serializers import UserSerializer

class OrganizationSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    combined_address = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = ('id', 'title', 'description', 'combined_address', 'members')

    def get_combined_address(self, obj):
        return f"{obj.address}, {obj.postcode}"

class EventSerializer(serializers.ModelSerializer):
    organizations = OrganizationSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'organizations', 'date')