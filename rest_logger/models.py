from django.db import models
from django.contrib.auth.models import User

class ExceptionLog(models.Model):
	user_id = models.IntegerField(null=True)
	request_method = models.CharField(max_length=10)
	request_path = models.CharField(max_length=150)
	traceback = models.TextField()
	remote_address = models.CharField(max_length=20)
	timestamp = models.DateTimeField(auto_now_add=True, blank=True)
	exception = models.TextField()

	class Meta:
		verbose_name = 'Exception Log'
		verbose_name_plural = 'Exception Logs'
		db_table = 'exception_logs'


	def __str__(self):
		return self.request_path


class RequestLog(models.Model):
	user_id = models.IntegerField(null=True)
	request_method = models.CharField(max_length=10)
	request_path = models.CharField(max_length=500)
	response_status = models.IntegerField()
	request_body = models.TextField(null=True)
	remote_address = models.CharField(max_length=50)
	server_hostname = models.CharField(max_length=50)
	run_time = models.FloatField()
	timestamp = models.DateTimeField(auto_now_add=True, blank=True)

	class Meta:
		verbose_name = 'Request Log'
		verbose_name_plural = 'Request Logs'
		db_table = 'request_logs'

	def __str__(self):
		return self.request_path