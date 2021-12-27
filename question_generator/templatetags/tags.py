from django import template
from question_generator.models import Course, Profile
from question_generator.views import question_approval


register = template.Library()


def CourseCode(value):
    courseCode = Course.objects.filter(course_title=value).first()
    return courseCode.course_code

def teacher_name(value):
    teacher = Profile.objects.filter(user__email=value).first()
    print(value)
    if not teacher:
        return "null"
    else:
        return teacher.name


register.filter('CourseCode', CourseCode)
register.filter('teacher_name', teacher_name)