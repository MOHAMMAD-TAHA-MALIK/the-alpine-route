

# Register your models here.
from django.contrib import admin
from .models import Trek, TrekEvent, Comment

@admin.register(Trek)
class TrekAdmin(admin.ModelAdmin):
    list_display = ('title', 'destination', 'date', 'difficulty', 'created_by')
    list_filter = ('difficulty', 'date')
    search_fields = ('title', 'destination')

@admin.register(TrekEvent)
class TrekEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'date', 'created_at')
    list_filter = ('date',)
    search_fields = ('title', 'location')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'trek', 'created_at')