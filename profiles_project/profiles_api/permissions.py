from rest_framework import permissions

class UpdateOwnProfile(permissions.BasePermission):
    """Permiso de usuario para editar su propio perfil"""

    def has_object_permission(self, request, view, obj):
        """Revisar el usuario intenta edsietar su propio perfil """

        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.id == request.user.id

class UpdateOwnStatus(permissions.BasePermission):
    """Permite actualizar el status feed propio"""

    def has_object_permission(self, request, views, obj):
        """Revisar si el esta intentando editar su propio perfil"""
        if request.method in permissions.SAFE_METHODS:
            return True

        return object.user_profile_id == request.user.id