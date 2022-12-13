from django.contrib import admin
from .models import Course, Category, CourseReview

class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category', 
        'price',
        'rating',
        'image',
    )

    ordering = ('sku',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )

admin.site.register(Course, CourseAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CourseReview)