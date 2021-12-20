from django import template
from question_generator.models import Course


register = template.Library()


def CourseCode(value):
    customer = Course.objects.filter(course_title=value).first()
    return customer.course_code




register.filter('CourseCode', CourseCode)