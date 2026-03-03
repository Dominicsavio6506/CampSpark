from django.contrib import admin
from .models import Location, Asset, AssetIssue

admin.site.register(Location)

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('name','category','location',)
    search_fields = ('name','category',)


@admin.register(AssetIssue)
class AssetIssueAdmin(admin.ModelAdmin):
    list_display = ('asset','priority','status','created_at')
    list_filter = ('status','priority',)