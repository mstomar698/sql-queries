
from datetime import date, datetime, timedelta
import os
import secrets
import jwt
import tempfile
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics
from .models import Certificate, Teacher, Student
from .serializers import TeacherSerializer, StudentSerializer
from xhtml2pdf import pisa
from django.template.loader import render_to_string

class TableView(generics.ListCreateAPIView):
    queryset_teachers = Teacher.objects.all()
    queryset_students = Student.objects.all()
    serializer_class_teachers = TeacherSerializer
    serializer_class_students = StudentSerializer

    def list(self, request, *args, **kwargs):
        teachers = self.serializer_class_teachers(
            self.queryset_teachers.prefetch_related('students'), many=True).data
        students = self.serializer_class_students(
            self.queryset_students.prefetch_related('teachers'), many=True).data

        teachers_dict = {}
        students_dict = {}

        for teacher in teachers:
            teacher_name = teacher['name']
            teacher_students = Student.objects.filter(
                teachers=teacher['id']).values_list('name', flat=True)
            teachers_dict[teacher_name] = list(teacher_students)

        for student in students:
            student_name = student['name']
            student_teachers = [teacher['name']
                                for teacher in student['teachers']]
            students_dict[student_name] = student_teachers

        print(f"Teachers: {teachers_dict}, Students: {students_dict}")
        context = {
            'teachers_and_students': teachers_dict,
            'students_and_teachers': students_dict,
        }

        return render(request, 'table/table.html', context)


def single_entries(request, name):
    context = {}
    if name.startswith('Teacher'):
        try:
            teacher = Teacher.objects.get(name=name)
            students = teacher.students.all()
            context['teacher_name'] = name
            context['related_students'] = students
        except Teacher.DoesNotExist:
            context['error_message'] = f'Teacher with name {name} does not exist.'
    else:
        try:
            student = Student.objects.get(name=name)
            teachers = student.teachers.all()
            context['student_name'] = name
            context['related_teachers'] = teachers
        except Student.DoesNotExist:
            context['error_message'] = f'Student with name {name} does not exist.'
    return render(request, 'table/single_entries.html', context)


# Without serializer for .html files
'''
def list(self, request, *args, **kwargs):
    teachers = Teacher.objects.all()
    students = Student.objects.all()

    print("Teachers:")
    for teacher in teachers:
        print(teacher)

    print("Students:")
    for student in students:
        print(student)

    context = {
        'teachers': teachers,
        'students': students,
    }

    return render(request, 'table/table.html', context)
'''


def certificates(request, url):
    url_parts = url.split('/')
    teacher_name = None
    student_name = None
    if url_parts[0] == "student":
        teacher_name = url_parts[1]
        student_name = url_parts[2]
    elif url_parts[0] == "teacher":
        student_name = url_parts[1]
        teacher_name = url_parts[2]
    elif url_parts[0] == "form":
        student_name = request.GET.get('input_student_name')
        teacher_name = request.GET.get('input_teacher_name')
    elif url_parts[0] == "validate":
        certificate_id = request.POST.get('certificateId')
        context = {}
        try:
            certificate = Certificate.objects.filter(certificate_id=certificate_id).first()
            context['certificate_id'] = certificate_id
            try:
                decoded_token = jwt.decode(certificate.jwt_token, 'demo-security-key', algorithms=['HS256'])
                expiration_timestamp = decoded_token['exp']
                expiration_date = datetime.fromtimestamp(expiration_timestamp)
                context['valid_till'] = expiration_date
                if decoded_token['certificate_id'] == certificate_id:
                    context['is_valid'] = True
                else:
                    context['is_valid'] = False
            except jwt.ExpiredSignatureError:
                context['is_valid'] = False
        except Certificate.DoesNotExist:
            context['certificate_id'] = None
            context['valid_till'] = None
            context['is_valid'] = False
        return render(request, 'table/certificates.html', context)
    else:
        teacher_name = None
        student_name = None
        context = {
            'teacher_name': teacher_name,
            'student_name': student_name,
        }
        return render(request, 'table/certificates.html', context)
    # JWT logic
    today = date.today()
    certificate_id = secrets.token_hex(5)
    # expiration_date = datetime.now() + timedelta(days=1) #for one day validity
    expiration_date = datetime(2023, 10, 17)
    expiration_timestamp = int(expiration_date.timestamp())
    token_payload = {
        'certificate_id': certificate_id,
        'exp': expiration_timestamp,
    }
    jwt_token = jwt.encode(token_payload, 'demo-security-key', algorithm='HS256')
    if teacher_name is not None and student_name is not None:
        certificate = Certificate(
            certificate_id=certificate_id,
            jwt_token=jwt_token,
            student_name=student_name,
            teacher_name=teacher_name
        )
        certificate.save()
    context = {
        'teacher_name': teacher_name,
        'student_name': student_name,
        'date': today,
        'certificate_id': certificate_id,
        'valid_till': expiration_date,
    }
    html = render_to_string('table/pdf.html', context)
    temp_file = tempfile.NamedTemporaryFile(delete=False)

    pisa_status = pisa.CreatePDF(str(html), dest=temp_file)
    if pisa_status.err:
        return render(request, 'table/certificates.html', context)

    temp_file.seek(0)
    pdf_data = temp_file.read()
    temp_file.close()

    os.unlink(temp_file.name)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="certificate_{student_name}.pdf"'
    response.write(pdf_data)

    return response