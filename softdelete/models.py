from django.db import models
from django.utils import timezone

class SoftDeletQueryset(models.query.QuerySet):
	def delete(self):
		return self.update(is_deleted=True, deleted_at=timezone.now())

	def hard_delete(self):
		return super().delete()


class SoftDeletManager(models.Manager):
	def get_queryset(self):
		return SoftDeletQueryset(self.model, self._db).filter(is_deleted=False)


class DeletedQueryset(models.query.QuerySet):
	def restore(self, *args, **kwargs):
		qs =self.filter(*args, **kwargs)
		qs.update(is_deleted=False)


class DeleteManager(models.Manager):
	def get_queryset(self):
		return DeletedQueryset(self.model, self._db).filter(is_deleted=True)

class SoftDeleteModel(models.Model):
	is_deleted = models.BooleanField(default=False)
	deleted_at = models.DateTimeField(blank=True, null=True)

	objects = SoftDeletManager()
	deleted_objects = DeleteManager()

	class Meta:
		abstract = True


	def delete(self, *args, **kwargs):
		self.is_deleted = True
		self.deleted_at = timezone.now()
		self.save()

	def restore(self):
		self.is_deleted = False
		self.save()

	def hard_delete(self, *args, **kwargs):
		super().delete(*args, **kwargs)