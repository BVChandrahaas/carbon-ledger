"""
Abstract base models that other models inherit from.
Provides common fields and functionality.
"""

import uuid
from django.db import models


class UUIDModel(models.Model):
    """
    Abstract model with UUID primary key.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    """
    Abstract model with created_at and updated_at timestamps.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class SoftDeleteManager(models.Manager):
    """
    Manager that excludes soft-deleted objects by default.
    """
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)
    
    def alive(self):
        """Return only non-deleted objects."""
        return self.get_queryset()
    
    def deleted(self):
        """Return only deleted objects."""
        return super().get_queryset().filter(deleted_at__isnull=False)
    
    def with_deleted(self):
        """Return all objects including deleted."""
        return super().get_queryset()


class SoftDeleteModel(models.Model):
    """
    Abstract model with soft delete functionality.
    """
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    objects = SoftDeleteManager()
    all_objects = models.Manager()  # Access all objects including deleted
    
    class Meta:
        abstract = True
    
    def delete(self, using=None, keep_parents=False):
        """
        Soft delete: Set deleted_at instead of actually deleting.
        """
        from django.utils import timezone
        self.deleted_at = timezone.now()
        self.save(using=using)
    
    def hard_delete(self):
        """
        Actually delete the object from database.
        """
        super().delete()
    
    def restore(self):
        """
        Restore a soft-deleted object.
        """
        self.deleted_at = None
        self.save()


class BaseModel(UUIDModel, TimeStampedModel, SoftDeleteModel):
    """
    Base model combining UUID, timestamps, and soft delete.
    Most models should inherit from this.
    """
    class Meta:
        abstract = True
