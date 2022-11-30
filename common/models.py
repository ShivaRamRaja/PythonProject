import uuid, threading, datetime
from django.db import models
from django.contrib.auth.models import User

request_local = threading.local()

def get_request():
    """Get request."""
    return getattr(request_local, 'request', None)


class CustomQuerySet(models.QuerySet):
    def delete(self):
        return super(CustomQuerySet, self).update(deleted=True)

    def hard_delete(self):
        return super(CustomQuerySet, self).delete()


class CustomManager(models.Manager):
    """
    Custom manager so as not to return deleted objects.
    """

    def get_queryset(self):
        """Return not deleted objects."""
        return CustomQuerySet(self.model).filter(deleted=False)

    def hard_delete(self, *args, **kwargs):
        return self.get_queryset().hard_delete()


class AbstractBase(models.Model):
    slug = models.CharField(
        default=uuid.uuid4, editable=False,
        unique=True, max_length=300
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(
        default=False, help_text="This is to make sure deletes are not actual deletes"
    )
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        related_name="%(class)s_created_by",
        blank=True, null=True,
        on_delete=models.DO_NOTHING
    )

    everything = models.Manager()
    objects = CustomManager()

    def save(self, *args, **kwargs):
        """Override save method and save created_by."""
        request_ = get_request()
        if request_:
            user = request_.user
            if self.pk is None:
                self.created_by = user
        super(AbstractBase, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Override delete."""
        now = datetime.now()
        self.deleted = True
        self.deleted_at = now
        self.save()

    def hard_delete(self, *args, **kwargs):
        """Hard delete."""
        self.delete = models.Model.delete(self)

    class Meta:
        """Define metadata options."""

        ordering = ["-updated_at", "-created_at"]
        abstract = True
