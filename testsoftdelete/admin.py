from django.contrib import admin
from .models import Course, Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
	list_display = ['id', 'student_name', 'course_taken']
	list_editable = ['course_taken']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
	list_display = ['id', 'course_name', 'created_at']
