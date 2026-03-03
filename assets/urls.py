from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.asset_list, name='asset_list'),
    path('add/', views.add_asset, name='add_asset'),
    path('report/', views.report_issue, name='report_issue'),
    path('issues/', views.issue_list, name='issue_list'),
    path('issues/update/<int:issue_id>/<str:status>/',
     views.update_issue_status,
     name='update_issue_status'),
]