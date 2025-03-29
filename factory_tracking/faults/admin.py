from django.contrib import admin
from .models import FaultCase, FaultImage, FaultNote, FaultNoteImage

# ----------------------------
# Inlines
# ----------------------------

class FaultImageInline(admin.TabularInline):
    model = FaultImage
    readonly_fields = ('preview',)
    fields = ('image', 'preview')
    extra = 1

class FaultNoteInline(admin.StackedInline):
    model = FaultNote
    extra = 1
    readonly_fields = ('created_at',)

# ----------------------------
# FaultCase Admin
# ----------------------------

@admin.register(FaultCase)
class FaultCaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'machine', 'status', 'reported_by', 'created_at', 'closed_at')
    list_filter = ('status', 'machine')
    search_fields = ('description',)
    readonly_fields = ('created_at', 'updated_at')
    inlines = [FaultImageInline, FaultNoteInline]

# ----------------------------
# FaultNoteImage Admin (optional, to manage them separately)
# ----------------------------

@admin.register(FaultNoteImage)
class FaultNoteImageAdmin(admin.ModelAdmin):
    list_display = ('note', 'uploaded_at', 'preview')
    readonly_fields = ('preview',)
    search_fields = ('note__content',)
