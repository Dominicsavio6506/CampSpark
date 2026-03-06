from django.contrib import admin
from .models import Student, Department


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "roll_number", "department_fk")
    list_per_page = 20


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name",)