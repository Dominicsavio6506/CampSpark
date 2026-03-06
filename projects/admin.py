from django.contrib import admin
from .models import Project, Department

admin.site.register(Department)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "team_name", "department", "status")
    list_filter = ("status", "department")
    search_fields = ("title", "team_name")