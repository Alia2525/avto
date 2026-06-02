from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers

User = get_user_model()


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def save(self) -> None:
        email = self.validated_data["email"]
        user = User.objects.filter(email__iexact=email).first()
        if not user:
            return  # do not leak existence

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # In production this should be a real frontend URL (public host).
        reset_payload = {"uid": uid, "token": token}
        send_mail(
            subject="Password reset",
            message=f"Use this payload to reset password: {reset_payload}",
            from_email=None,
            recipient_list=[user.email],
        )


class ResetPasswordConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate_new_password(self, value: str) -> str:
        from django.contrib.auth.password_validation import validate_password

        validate_password(value)
        return value

    def save(self) -> None:
        uid = self.validated_data["uid"]
        token = self.validated_data["token"]
        new_password = self.validated_data["new_password"]

        user_id = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=user_id)
        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError({"token": "Invalid or expired token."})

        user.set_password(new_password)
        user.save(update_fields=["password"])

