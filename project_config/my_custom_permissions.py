from rest_framework.permissions import BasePermission, SAFE_METHODS



class IsOwnerOrReadOnly(BasePermission):
    """
    Разрешает изменение только владельцу объекта.
    Просмотр разрешен всем.
    """
    def has_permission(self, request, view):
        # SAFE_METHODS: [GET, HEAD, OPTIONS] запросы
        if request.method in SAFE_METHODS:
            return True
        '''Если тут вместо view.action == 'create' использовать request.method == 'POST' к примеру,
        то будут заблокированы ВСЕ POST запросы. В том числе и в has_object_permission.
        Поскольку в List методе можно только создать юзера, то view.action == 'create' достаточно.'''
        if view.action == 'create':
            return request.user.is_staff or request.user.is_superuser
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        # Для (PUT, PATCH, DELETE) проверяем, что пользователь - владелец или админ
        return obj == request.user or request.user.is_staff or request.user.is_superuser # ✅ Ключевая строка!



class IsOwnerPostOrReadOnly(BasePermission):
    """
    Разрешает изменение только владельцу объекта.
    Просмотр разрешен всем.
    """
    def has_permission(self, request, view):
        # SAFE_METHODS: [GET, HEAD, OPTIONS] запросы
        if request.method in SAFE_METHODS:
            return True
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        # Для (PUT, PATCH, DELETE) проверяем, что пользователь - владелец или админ
        return obj.author.pk == request.user.pk or request.user.is_staff or request.user.is_superuser #Ключевая строка!



class IsOwnerCommentOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # SAFE_METHODS: [GET, HEAD, OPTIONS] запросы
        if request.method in SAFE_METHODS:
            return True
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if view.action == 'destroy':
            return obj.post.author_id == request.user.pk or obj.author_comm_id == request.user.pk
        if view.action == 'update' or view.action == 'partial_update':
            return obj.author_comm_id == request.user.pk
        return False
