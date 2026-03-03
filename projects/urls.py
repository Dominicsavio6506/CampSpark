from django.urls import path
from . import views

urlpatterns = [
    path("", views.projects_home, name="projects_home"),
    path("create/", views.create_project, name="create_project"),
    path("edit/<int:project_id>/", views.edit_project, name="edit_project"),
    path("staff/", views.staff_panel, name="staff_panel"),
    path("detail/<int:project_id>/", views.project_detail, name="project_detail"),
    path("archive/", views.archive_projects, name="archive_projects"),
    path(
        "assign/<int:project_id>/",
        views.assign_project_to_staff,
        name="assign_project"
    ),
    path("staff/all/", views.staff_all_projects, name="staff_all"),
    path("staff/my/", views.staff_my_projects, name="staff_my"),
    path(
        "archive/<int:project_id>/",
        views.manual_archive,
        name="manual_archive"
    ),
    path(
        "admin-control/",
        views.admin_project_control,
        name="admin_project_control"
    ),
    path("staff/unassign/<int:pk>/", views.unassign_project, name="unassign_project"),
    path("member/remove/<int:pk>/", views.remove_member, name="remove_member"),
    path("progress/add/<int:project_id>/",
         views.add_progress,
         name="add_progress"),
]