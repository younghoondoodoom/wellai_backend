from django.db import models
from django.utils import timezone

# Create your models here.


class DeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class TimeStampModel(models.Model):

    created_at = models.DateTimeField(
        verbose_name="생성 날짜", db_index=True, default=timezone.now
    )
    modified_at = models.DateTimeField(verbose_name="수정 날짜", auto_now=True)

    class Meta:
        abstract = True


class DeleteModel(models.Model):

    is_deleted = models.BooleanField(verbose_name="삭제 상태", default=False)
    deleted_at = models.DateTimeField(verbose_name="삭제 날짜", null=True, blank=True)

    objects = DeleteManager()

    def delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    class Meta:
        abstract = True
