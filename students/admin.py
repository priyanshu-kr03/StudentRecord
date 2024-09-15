from django.contrib import admin
from .models import Student

# Register the Student model to be manageable via the admin panel
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'age', 'roll_number')  # Fields to display in the admin list view
    search_fields = ('name', 'roll_number')  # Fields to search
