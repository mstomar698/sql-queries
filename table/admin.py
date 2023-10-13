from django.contrib import admin
from .models import Certificate, Student, Teacher

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_teachers')

    def display_teachers(self, obj):
        return ", ".join([teacher.name for teacher in obj.teachers.all()])
    display_teachers.short_description = 'Teachers'

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('teachers')

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('certificate_id', 'student_name', 'teacher_name', 'created_at',)