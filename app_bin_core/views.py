from rest_framework import generics, permissions, response, status
from django.contrib.auth.models import User
from rest_framework.response import Response
import re
from api.serializers import ChangePasswordSerializer


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"error_message": "Wrong old password."}, status=status.HTTP_400_BAD_REQUEST)
            new_password_entry = serializer.data.get("new_password")
            reg = "[^\w\d]*(([0-9]+.*[A-Za-z]+.*)|[A-Za-z]+.*([0-9]+.*))"
            pat = re.compile(reg)

            if 8 <= len(new_password_entry) <= 16:
                password_validation = re.search(pat, new_password_entry)
                if password_validation:
                    self.object.set_password(
                        serializer.data.get("new_password"))
                else:
                    return Response({"error_message":
                                     "Password must contain a combination of letters and numbers"},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error_message":
                                 "Password must contain at least 8 to 16 characters"},
                                status=status.HTTP_400_BAD_REQUEST)

            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
