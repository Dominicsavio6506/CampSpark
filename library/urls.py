from django.urls import path
from . import views

urlpatterns = [
    path('', views.library_home, name='library_home'),            
    path('panel/', views.library_admin_panel, name='library_panel'), 
    path('issue/<int:book_id>/', views.issue_book, name='issue_book'),
    path('my/', views.my_books, name='my_books'),
    path('manage/', views.manage_books, name='manage_books'),
    path('issued/', views.issued_books, name='issued_books'),
    path('return/<int:record_id>/', views.return_book, name='return_book'),


]

