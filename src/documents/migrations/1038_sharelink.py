# Generated by Django 4.1.10 on 2023-08-14 14:51

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.contrib.auth.management import create_permissions
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from django.db import migrations
from django.db import models
from django.db.models import Q


def add_sharelink_permissions(apps, schema_editor):
    # create permissions without waiting for post_migrate signal
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, apps=apps, verbosity=0)
        app_config.models_module = None

    add_permission = Permission.objects.get(codename="add_document")
    sharelink_permissions = Permission.objects.filter(codename__contains="sharelink")

    for user in User.objects.filter(Q(user_permissions=add_permission)).distinct():
        user.user_permissions.add(*sharelink_permissions)

    for group in Group.objects.filter(Q(permissions=add_permission)).distinct():
        group.permissions.add(*sharelink_permissions)


def remove_sharelink_permissions(apps, schema_editor):
    sharelink_permissions = Permission.objects.filter(codename__contains="sharelink")

    for user in User.objects.all():
        user.user_permissions.remove(*sharelink_permissions)

    for group in Group.objects.all():
        group.permissions.remove(*sharelink_permissions)


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("documents", "1037_webp_encrypted_thumbnail_conversion"),
    ]

    operations = [
        migrations.CreateModel(
            name="ShareLink",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        blank=True,
                        db_index=True,
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created",
                    ),
                ),
                (
                    "expiration",
                    models.DateTimeField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="expiration",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        blank=True,
                        editable=False,
                        unique=True,
                        verbose_name="slug",
                    ),
                ),
                (
                    "document_version",
                    models.CharField(
                        choices=[("archive", "Archive"), ("original", "Original")],
                        default="archive",
                        max_length=50,
                    ),
                ),
                (
                    "document",
                    models.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="share_links",
                        to="documents.document",
                        verbose_name="document",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="share_links",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="owner",
                    ),
                ),
            ],
            options={
                "verbose_name": "share link",
                "verbose_name_plural": "share links",
                "ordering": ("created",),
            },
        ),
        migrations.RunPython(add_sharelink_permissions, remove_sharelink_permissions),
    ]
