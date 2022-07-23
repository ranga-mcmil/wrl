from django.contrib import admin
from .models import User, Student, Supervisor, Contact, WorkSupervisor, StudentProfile

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name')


admin.site.register(Student)
admin.site.register(StudentProfile)
admin.site.register(Supervisor)
admin.site.register(WorkSupervisor)
admin.site.register(Contact)