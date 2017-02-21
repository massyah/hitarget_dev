from django.contrib import admin

# Register your models here.
from hitarget.models import Lead, Company, Contact, Category, Location

admin.site.register(Company)
admin.site.register(Contact)
admin.site.register(Category)
admin.site.register(Location)


class LeadAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'date_publish',
                    'status', 'maturity_level')
    list_filter = ('status', 'date_created', 'date_publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'date_publish'
    ordering = ['status', 'date_publish']


admin.site.register(Lead, LeadAdmin)
