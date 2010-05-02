from django.contrib import admin

import models

class TaskInline(admin.TabularInline):
    model = models.Task

admin.site.register(models.Project,
                    inlines=(TaskInline,))
#admin.site.register(models.Task)
