from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from rest_framework.authentication import TokenAuthentication
from profiles_api import serializers, models, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated


class HelloApiView(APIView):
    """ API View de prueba"""

    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """Retornar lista de caracteristicas del APIview"""
        an_apiview = [
            'Usamos métodos HTTP como funciones (get, post, patch, put, delete)',
            'Es similar a una vista tradicional de Django',
            'Nos da el mayor control sobre la lógica de nuestra aplicación',
            'Está mapeado manualmente a los URLs',
        ]

        return Response({'message': 'Hello!', 'an_apiview': an_apiview})


    def post(self, request):
        """ Crea un mensaje con nuestro nombre """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message':message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
    def put(self, request, pk=None):
        """Maneja actualizar un objeto"""
        return Response({'method':'put'})

    def patch(self, request, ps=None):
        """Maneja actualizacion parcial de un objeto"""
        return Response({'method':'patch'})

    def delete(self, request, ps=None):
        """Borrar un objeto"""
        return Response({'method':'delete'})

class HelloViewSet(viewsets.ViewSet):
    """Testing API ViewSet"""

    serializer_class = serializers.HelloSerializer

    def list(self,request):
        i_viewset=[
            'Usar acciones (list, create, retrieve, update, parcial_update)',
            'Automaticamente mapea a los Urls usando Routers',
            'Provee mas funcionalidad con menos codigo'
        ]

        return Response({'message':'Hello', 'i_viewset':i_viewset})


    def create(self, request):
        """Crea un nuevo mensaje de hola mundo"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message=f'hola {name}'
            return Response({'message':message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def retrieve(self, request, pk=None):
        """Obtiene un objeto y su id"""

        return Response({'http_method':'GET'})
    
    def update(self, request, pk=None):
        """Actualizar un objeto"""

        return Response({'http_method':'PUT'})

    def partial_update(self, request, pk=None):
        """Actualizar una parte de un objeto"""

        return Response({'http_method':'PATCH'})

    def destroy(self, request, pk=None):
        """Elimina un objeto"""

        return Response({'http_method':'DELETE'})

class UserProfileViewSet(viewsets.ModelViewSet):
    """Crear y actualiszar perfiles"""

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()

    autentication_classes= (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name','email')

class UserLoginApiView(ObtainAuthToken):
    """Crea token de autenticacion de usuario"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Manejar el crear, leer y actualizarel profile feed"""
    TokenAuthentication_classes=(TokenAuthentication)
    serializer_class = serializers.ProfileFeedItemSerializer
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated,)
    queryset = models.ProfileFeedItem.objects.all()

    def perform_create(self, serializer):
        """ Setear el perfil de usuario para el usuario que esta logeado"""
        serializer.save(user_profile=self.request.user)
