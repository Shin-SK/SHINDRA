from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """ 管理者 (`admin`) のみ許可 """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsMemberUser(BasePermission):
    """ 同好会会員 (`member`) 以上は許可 """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'member']

class IsMemberOrPublic(BasePermission):
    """ `public` は全員OK、`members` は `member` 以上のみ許可 """
    def has_object_permission(self, request, view, obj):
        if obj.visibility == 'public':
            return True  # 全員OK
        return request.user.is_authenticated and request.user.role in ['admin', 'member']
