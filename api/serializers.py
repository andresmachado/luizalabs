"""API serializers."""
from rest_framework import serializers
from .models import Person


class PersonSerializer(serializers.ModelSerializer):
    """Class to serialize and deserialize information about Person object."""

    class Meta:
        """Meta info about serializer."""

        model = Person
        fields = ('__all__')
