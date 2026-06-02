import os

import django


def main() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    django.setup()

    from django.contrib.auth import get_user_model

    User = get_user_model()

    username = os.getenv("DJANGO_SUPERUSER_USERNAME", "").strip()
    email = os.getenv("DJANGO_SUPERUSER_EMAIL", "").strip()
    password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "").strip()

    if not (username and password):
        return

    user, _created = User.objects.get_or_create(username=username, defaults={"email": email})
    if email and user.email != email:
        user.email = email

    user.is_staff = True
    user.is_superuser = True
    user.set_password(password)
    user.save()


if __name__ == "__main__":
    main()

