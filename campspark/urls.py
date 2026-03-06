from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from adminpanel.views import (
    home,
    login_view,
    logout_view,
    dashboard_router,
    staff_dashboard,
    admin_dashboard
)

from ai_assistant.views import complaint_ai_dashboard, campus_ai_chat, test_ai_page
from complaints_app.views import complaint_stats


urlpatterns = [

    # Django Admin
    path("admin/", admin.site.urls),

    # Home & Login
    path("", home, name="home"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    # Smart Dashboard Router
    path("dashboard/", dashboard_router, name="dashboard"),

    # Staff
    path("staff/", staff_dashboard, name="staff_dashboard"),
    path("staff/", include("camp_staff.urls")),

    # Admin Panel
    path("admin-panel/", admin_dashboard, name="admin_dashboard"),

    # Student Module
    path("student/", include("students.urls")),

    # AI Assistant
    path("ai/", include("ai_assistant.urls")),
    path("ai/complaint-stats/", complaint_ai_dashboard),
    path("ai/chat/", campus_ai_chat),
    path("ai/test/", test_ai_page),

    # Complaints
    path("complaints/", include("complaints_app.urls")),
    path("stats/", complaint_stats),

    # Attendance
    path("attendance/", include("attendance.urls")),

    # Scholarships
    path("scholarships/", include("scholarships.urls")),

    # Marks
    path("marks/", include("marks.urls")),

    # Fees
    path("fees/", include("camp_fees.urls")),

    # Academics
    path("academics/", include("academics.urls")),

    # Notifications
    path("notifications/", include("notifications.urls")),

    # Reports
    path("reports/", include("reports.urls")),

    # Special Roles
    path("special/", include("special_roles.urls")),

    # Library
    path("library/", include("library.urls")),

    # Assets
    path("assets/", include("assets.urls")),

    # Events
    path("events/", include("events.urls")),

    # Projects
    path("projects/", include("projects.urls")),
]


# Media support
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)