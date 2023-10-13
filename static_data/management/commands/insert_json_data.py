import json
from django.core.management.base import BaseCommand
from table.models import Teacher, Student

class Command(BaseCommand):
    help = 'Insert JSON data into the database'

    def handle(self, *args, **kwargs):
        try:
            with open('./static_data/management/commands/JSON/dummy.json', 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)

                teachers_by_name = {teacher['fields']['name']: teacher for teacher in data if teacher['model'] == 'table.teacher'}

                for item in data:
                    model = item.get('model')
                    if model == 'table.teacher':
                        teacher_data = item['fields']
                        teacher, created = Teacher.objects.get_or_create(name=teacher_data['name'], defaults=teacher_data)
                        if not created:
                            teacher.__dict__.update(**teacher_data)
                            teacher.save()
                        print(f"{teacher.name} created/updated")
                    elif model == 'table.student':
                        student_data = item['fields']
                        student_name = student_data['name']
                        teacher_names = student_data.pop('teachers')
                        student, created = Student.objects.get_or_create(name=student_name, defaults=student_data)
                        if not created:
                            student.__dict__.update(**student_data)
                            student.save()
                        # Create relationships with teachers based on names
                        student.teachers.set([Teacher.objects.get(name=teacher_name) for teacher_name in teacher_names])
                        print(f"{student.name} for teachers {teacher_names} created/updated")

                self.stdout.write(self.style.SUCCESS('Data loaded successfully'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('JSON file not found'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))
