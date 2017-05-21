"""API Views."""
import facebook
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status, serializers
from django.shortcuts import get_object_or_404
from django.http.response import Http404
from .serializers import PersonSerializer
from .models import Person
from .utils import get_facebook_obj
# Create your views here.


class PersonView(APIView):
    """A simple view for get and create person info."""

    authentication_classes = (authentication.SessionAuthentication, authentication.BasicAuthentication,)
    permission_classes = (permissions.AllowAny,)
    serializer_class = PersonSerializer

    def get_queryset(self):
        """Return queryset object."""
        queryset = Person.objects.all()
        return queryset

    def get_object(self, person):
        """Return an instance of object or error 404."""
        person = get_object_or_404(Person, facebook_id=person)
        return person

    def get(self, request, person=None):
        """Return all objects based on get_queryset() method."""
        limit = self.request.query_params.get('limit', None)
        queryset = self.get_queryset().values('id', 'name', 'facebook_id', 'gender', 'username')

        if person:
            instance = self.get_object(person)
            serializer = self.serializer_class(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if limit:
            queryset = queryset[:int(limit)]
        return Response(queryset, status=status.HTTP_200_OK)

    def post(self, request):
        """
            Create a Person object based on facebook information.

        :return: A representation of created object.
        """
        # import ipdb; ipdb.set_trace()
        data = {}
        facebook_id = request.data.get('facebookId')

        if not facebook_id:
            raise serializers.ValidationError('Informe o facebookID')

        try:
            instance = self.get_object(facebook_id)
        except Http404:
            instance = None

        if instance:
            serializer = self.serializer_class(instance=instance)
            return Response(serializer.data, status=status.HTTP_200_OK)

        try:
            facebook_user_info = get_facebook_obj(facebook_id)
        except facebook.GraphAPIError:
            raise serializers.ValidationError('Usuário com esse ID não existe ou não pode ser encontrado.')

        data.update({
            'facebook_id': facebook_user_info.get('id'),
            'name': facebook_user_info.get('name'),
            'gender': facebook_user_info.get('gender'),
            'username': 'Placeholder'
        })

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, person):
        """
            Delete an instance of Person.

        :param person: A facebookID that identifies a Person
        :return: 204 no content if delete or 404 if not found
        """
        person = get_object_or_404(Person, facebook_id=person)
        person.delete()
        return Response([], status=status.HTTP_204_NO_CONTENT)
