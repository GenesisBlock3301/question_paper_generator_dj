from django.db import models
import uuid
from ckeditor.fields import RichTextField
from accounts.models import User

class Faculty(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    faculty_name = models.CharField(max_length=255,blank=True,null=True)
    about_faculty = models.CharField(max_length=255,blank=True,null=True)

    def __str__(self) -> str:
        return f"{self.faculty_name}"
    
    class Meta:
        verbose_name_plural = "Faculties"
        ordering = ["-id"]


class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    department_name = models.CharField(max_length=255,blank=True,null=True)
    about_department = models.CharField(max_length=255,blank=True,null=True)
    faculty = models.ForeignKey(Faculty,related_name="deparments",on_delete=models.CASCADE,verbose_name="related faculty")

    def __str__(self) -> str:
        return f"{self.department_name}"



class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course_title = models.CharField(max_length=255,blank=True,null=True)
    about_course = models.CharField(max_length=255,blank=True,null=True)
    course_code = models.CharField(max_length=255,blank=True,null=True)
    department = models.ForeignKey(Department,related_name="courses",on_delete=models.CASCADE,verbose_name="related department")

    def __str__(self) -> str:
        return f"{self.course_title}"


class Question(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    full_mark = models.CharField(max_length=255,blank=True,null=True)
    difficulty_level = models.CharField(max_length=255,blank=True,null=True)
    course = models.ForeignKey(Course,related_name="questions",on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name="questions",on_delete=models.CASCADE)
    body = RichTextField(blank=True,null=True)
    approve = models.BooleanField(default=False,blank=True,null=True)
    created_time = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_time = models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self) -> str:
        return f"{self.title}"
    
    
    
    
