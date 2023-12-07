from django.contrib import admin

from taskList_app.models import ProfileImg, TaskList

@admin.register(ProfileImg)
class AdminProfile(admin.ModelAdmin):
    pass



@admin.register(TaskList)
class TaskListAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'done')