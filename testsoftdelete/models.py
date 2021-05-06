from django.db import models
from softdelete.models import SoftDeleteModel

class Course(SoftDeleteModel):
	course_name = models.CharField(max_length=20)
	created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

	def __str__(self):
		return self.course_name

	class Meta:
		verbose_name = 'Course'
		verbose_name_plural = 'Course\'s'


class Student(SoftDeleteModel):
	student_name = models.CharField(max_length=30)
	course_taken = models.ForeignKey(Course, on_delete=models.CASCADE)

	def __str__(self):
		return self.student_name

	class Meta:
		verbose_name = 'Student'
		verbose_name_plural = 'Student\'s'
