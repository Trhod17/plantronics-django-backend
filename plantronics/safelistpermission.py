from rest_framework import permissions
from plantronics import settings


class SafeListPermission(permissions.BasePermission):
    """
    Ensure the connecting ip is on the safe list configured
    in the plantronics/settings.py file
    """

    def has_permission(self, request, view):

        remote_addr = request.META['REMOTE_ADDR']

        for valid_ip in settings.REST_SAFE_LIST_IPS:
            if remote_addr == valid_ip or remote_addr.startswith(valid_ip):
                return True

        return False
