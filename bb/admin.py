from django.contrib import admin

from bb.models import Activity


@admin.register(Activity)
class ModelNameAdmin(admin.ModelAdmin):
    pass
