from django.contrib import admin
from .models import Machine, Collection, Warning

@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'get_collections', 'created_at')
    list_filter = ('status', 'collections')
    search_fields = ('name',)

    def get_collections(self, obj):
        return ", ".join([c.name for c in obj.collections.all()])
    get_collections.short_description = 'Collections'


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Warning)
class WarningAdmin(admin.ModelAdmin):
    list_display = ('machine', 'message', 'added_by', 'created_at')
    list_filter = ('machine',)
    search_fields = ('message',)
