from django.contrib import admin
from .models import ApiKey

@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "key", "created_at")
    search_fields = ("name", "owner__username", "key")
    readonly_fields = ("key", "created_at")

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("owner",)
        return self.readonly_fields
