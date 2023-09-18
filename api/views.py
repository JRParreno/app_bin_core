from base64 import urlsafe_b64encode
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from oauth2_provider.models import get_access_token_model
from oauth2_provider.signals import app_authorized
from oauth2_provider.views.base import TokenView
from .serializers import ResetPasswordEmailRequestSerializer
from rest_framework import generics, permissions, response, status
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import smart_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.template.loader import get_template
from .email import Util
# Create your views here.


class TokenViewWithUserId(TokenView):
    @method_decorator(sensitive_post_parameters("password"))
    def post(self, request, *args, **kwargs):
        url, headers, body, status = self.create_token_response(request)
        print(body)

        if status == 200:
            body = json.loads(body)
            access_token = body.get("access_token")
            if access_token is not None:
                token = get_access_token_model().objects.get(
                    token=access_token)
                app_authorized.send(
                    sender=self, request=request,
                    token=token)
                body['id'] = str(token.user.id)
                body = json.dumps(body)
        response = HttpResponse(content=body, status=status)
        for k, v in headers.items():
            response[k] = v
        return response


class RequestPasswordResetEmail(generics.CreateAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer
    permission_classes = []

    def post(self, request):
        email_address = request.data.get('email_address', '')
        check_identity = User.objects.filter(email__exact=email_address)
        if check_identity.exists():
            identity = check_identity.first()
            uidb64 = urlsafe_b64encode(smart_bytes(identity.id))
            token = PasswordResetTokenGenerator().make_token(identity)

            relative_link = reverse(
                'api:password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            current_site = get_current_site(
                request=request).domain
            abs_url: str = f"https://{current_site}{relative_link}"

            context_email = {
                "url": abs_url,
                "full_name": f"{identity.first_name} {identity.last_name}"
            }
            message = get_template(
                'forgot_password/index.html').render(context_email)

            context = {
                'email_body': message,
                'to_email': identity.email,
                'email_subject': 'Reset your password'
            }

            Util.send_email(context)
        else:
            return response.Response({'error_message': 'Email not found!'}, status=status.HTTP_404_NOT_FOUND)

        return response.Response(
            {'success': 'We have sent you a link to reset your password'},
            status=status.HTTP_200_OK
        )
