from django.contrib import admin
from .models import ExceptionLog, RequestLog

@admin.register(ExceptionLog)
class ExceptionAdmin(admin.ModelAdmin):
	list_display = ['id', 
					'user_id', 
					#'request_method',
					'request_path', 
					'remote_address', 
					'timestamp'
					]

@admin.register(RequestLog)
class RequestAdmin(admin.ModelAdmin):
	list_display = ['id', 
					'user_id', 
					#'request_method'
					'request_path', 
					'response_status', 
					'remote_address', 
					#'server_hostname'
					'run_time',
					'timestamp'
					]