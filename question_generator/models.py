from django.db import models
import uuid
from ckeditor.fields import RichTextField
from accounts.models import User


class Faculty(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    faculty_name = models.CharField(max_length=255, blank=True, null=True)
    short_form = models.CharField(max_length=255, blank=True, null=True)
    about_faculty = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.faculty_name}"

    class Meta:
        verbose_name_plural = "Faculties"
        ordering = ["-id"]


class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    department_name = models.CharField(max_length=255, blank=True, null=True)
    short_form = models.CharField(max_length=255, blank=True, null=True)
    about_department = models.CharField(max_length=255, blank=True, null=True)
    faculty = models.ForeignKey(Faculty, related_name="deparments",
                                on_delete=models.CASCADE, verbose_name="related faculty")

    def __str__(self) -> str:
        return f"{self.department_name}"


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course_title = models.CharField(max_length=255, blank=True, null=True)
    about_course = models.CharField(max_length=255, blank=True, null=True)
    sort_form = models.CharField(max_length=255, blank=True, null=True)
    course_code = models.CharField(max_length=255, blank=True, null=True)
    department = models.ForeignKey(Department, related_name="courses",
                                   on_delete=models.CASCADE, verbose_name="related department")

    def __str__(self) -> str:
        return f"{self.course_title}"


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    term_name = models.CharField(max_length=255, blank=True, null=True)
    full_mark = models.CharField(max_length=255, blank=True, null=True)
    difficulty_level = models.CharField(max_length=255, blank=True, null=True)
    duration = models.CharField(max_length=255, blank=True, null=True)
    batch = models.CharField(max_length=255, blank=True, null=True)
    faculty = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    course = models.CharField(max_length=255, blank=True, null=True)
    semester = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(
        User, related_name="questions", on_delete=models.CASCADE)
    body = RichTextField(blank=True, null=True)
    approve = models.BooleanField(default=False, blank=True, null=True)
    created_time = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)
    updated_time = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.course}"


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.FileField(upload_to="profile/",blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    user = models.OneToOneField(User, related_name="users",
                                on_delete=models.CASCADE)
    short_name = models.CharField(max_length=255, blank=True, null=True)
    faculty = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=255, blank=True, null=True)
    designation = models.CharField(max_length=255, blank=True, null=True)
    course_question = models.CharField(max_length=255,default='', blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.user.is_teacher:
            self.role = "Teacher"
        else:
            self.role = "Admin"
        super(Profile, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.name}"
