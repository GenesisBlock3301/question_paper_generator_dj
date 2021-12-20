from django import forms
from . models import Department, Faculty, Question, Course
from ckeditor.widgets import CKEditorWidget

DIFFICULTY = [
    ('Easy', 'Easy'),
    ('Medium', 'Medium'),
    ('Hard', 'Hard'),
]
TERM_NAME = [
    ('Mid', "Mid Term"),
    ('Final', "Final Term"),
    ('Class Test', "Class Test")
]

MARKS = [
    ('100',100),
    ('40',40),
    ('15',15)
]
class CreationQuestionForm(forms.ModelForm):
    faculty = forms.CharField(widget=forms.Select(
        attrs={'class': 'form-select form-select-lg mb-3',"placeholder":"Faculty"},
        choices=Faculty.objects.all().values_list('faculty_name', 'faculty_name'))
    )
    term_name = forms.CharField(
        widget=forms.Select(
            attrs={'class': 'form-select form-select-lg mb-3'}, choices=TERM_NAME),
        required=True, max_length=100)
    full_mark = forms.CharField(widget=forms.Select(
        attrs={'class': 'form-select form-select-lg mb-3'},
        choices=MARKS
    ))
    difficulty_level = forms.CharField(
        widget=forms.Select(
            attrs={'class': 'form-select form-select-lg mb-3'}, choices=DIFFICULTY),
        required=True, max_length=100)
    batch = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Batch'}),
        required=True, max_length=100)
    department = forms.CharField(
        widget=forms.Select(
            attrs={'class': 'form-select form-select-lg mb-3'},
            choices=Department.objects.all().values_list('department_name', 'department_name')))
    course = forms.CharField(
        widget=forms.Select(
            attrs={'class': 'form-select form-select-lg mb-3'},
            choices=Course.objects.all().values_list('course_title', 'course_title')))
    duration = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Duration'}),
        required=True, max_length=100)
    semester = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Semester'}),
        required=True, max_length=100)

    body = forms.CharField(
        widget=CKEditorWidget(attrs={'class': 'form-control'}),
        required=True, max_length=100)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # self.fields['course'].queryset = Course.objects.all()
    #     # # self.fields.widget.Sel
    #     # self.fields['course'].widget.attrs.update({'class': 'form-select'})

    #     # self.fields["department"].queryset = Department.objects.all()
    #     # self.fields['department'].widget.attrs.update({'class': 'form-select'})

    class Meta:
        model = Question
        fields = ("faculty", "full_mark", "course", "department", "difficulty_level", "body")
