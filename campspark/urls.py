from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from django.contrib.auth import views as auth_views
from complaints_app.views import submit_complaint
from complaints_app.views import complaint_stats
from dashboard.views import admin_dashboard



# AI Views
from ai_assistant.views import complaint_ai_dashboard, campus_ai_chat, test_ai_page

# Admin Panel Views
from adminpanel.views import (
    home,
    login_view,
    logout_view,
    dashboard_router,
    staff_dashboard,    
    admin_dashboard
)

urlpatterns = [

    # Django Admin
    path('admin/', admin.site.urls),

    # Home & Login
    path("", home, name="home"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    # Smart Role Router
    path("dashboard/", dashboard_router, name="dashboard"),

    # Dashboards (Staff & Admin Only)
    path("staff/", staff_dashboard, name="staff_dashboard"),
    path("staff/", include("camp_staff.urls")),
    path("admin-panel/", admin_dashboard, name="admin_dashboard"),

    # ✅ Student Module (ONLY route here)
    path("student/", include("students.urls")),

    # AI Routes
    path("ai/", include("ai_assistant.urls")),
    path("ai/complaint-stats/", complaint_ai_dashboard),
    path("ai/chat/", campus_ai_chat),
    path("ai/test/", test_ai_page),

    # Complaints Module
    path("complaints/", include("complaints_app.urls")),
    

    # Attendance API / Module
    path("attendance/", include("attendance.urls")),

    #scolarship module
    path("scholarships/", include("scholarships.urls")),

    #Attendance 
    path("attendance/", include("attendance.urls")),

    #mark
    path("marks/", include("marks.urls")),
    path("fees/", include("camp_fees.urls")),

    path("academics/", include("academics.urls")),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    #Notification
    path('notifications/', include('notifications.urls')),

    #Report module
    path('reports/', include('reports.urls')),

    path('student/', include('students.urls')),
    path("stats/",complaint_stats),

    path('special/', include('special_roles.urls')),
    path('complaints/', include('complaints_app.urls')),

    path('dashboard/', include('dashboard.urls')),
    path('admin-panel/', admin_dashboard, name='admin_dashboard'),
    path('library/', include('library.urls')),
    path('assets/', include('assets.urls')),

    path("events/", include("events.urls")),

    path("projects/", include("projects.urls")),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Media Support (Photos)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
