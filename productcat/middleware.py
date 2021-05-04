import time
import socket
import sys
import traceback
from rest_logger.models import ExceptionLog, RequestLog
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from rest_framework import status
from celery import shared_task
from productcat.settings import DEBUG

@shared_task
def save_logs(data):
	RequestLog.objects.create(**data)


class RequestLogMiddleWare():
	def __init__(self, get_response):
		self.get_response = get_response
		self.start_time = time.time()


	def __call__(self, request):
		response = self.get_response(request)
		self.start_time = time.time()
		return response

	def process_template_response(self, request, response):
		request_data = request
		request_type = request.META.get('HTTP_ACCEPT', request.META.get(
				'CONTENT_TYPE', 'application/json'))
		data = {
			'user_id': request.user.pk,
			'request_method' : request.method,
			'request_path' : request.get_full_path(),
			'response_status' : response.status_code,
			'remote_address' : request.META['REMOTE_ADDR'],
			'server_hostname' : socket.gethostname(),
			'request_body' : request_data.POST,
			'run_time' : time.time() - self.start_time
		}
		save_logs.delay(data)
		return response


# class TimeZoneMiddleWare():
# 	def __init__(self, get_response):
# 		self.get_response = get_response

# 	def __call__(self, request):
# 		tzname = None
# 		if request.user.is_authenticated():
# 			tzname = timezone.now()


@shared_task
def save_exception_log(data):
	ExceptionLog.objects.create(**data)


class ExceptionLoggingMiddleware(MiddlewareMixin):
	def process_exception(self, request, exception):
		if DEBUG:
			return None
		_,_,stacktrace = sys.exc_info()
		data = {
			"user_id": request_path.user.pl,
			"request_method" : request.method,
			"request_path" : request.get_full_path(),
			"remote_address": request.META['REMOTE_ADDR'],
			"traceback" : ''.join(traceback.format_tb(stacktrace)),
			"exception": str(exception)
		}
		save_exception_log.delay(data)
		response = {
			"status": status.HTTP_500_INTERNAL_SERVER_ERROR,
			"message": 'Internal Server Error'
		}
		return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)