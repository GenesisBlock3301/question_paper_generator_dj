from django import forms
from question_generator.models import Department, Faculty, Profile


class ProfileForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Name'}),
        required=False, max_length=100)
    image = forms.FileField(
        widget=forms.FileInput(
            attrs={'class': 'form-control-file', 'placeholder': 'image'}),
        required=False, max_length=100)
    faculty = forms.CharField(
        widget=forms.Select(
            attrs={'class': 'form-select form-select-lg mb-3'},
            choices=Faculty.objects.all().values_list('faculty_name', 'faculty_name')))
    department = forms.CharField(
        widget=forms.Select(
            attrs={'class': 'form-select form-select-lg mb-3'},
            choices=Department.objects.all().values_list('department_name', 'department_name')))
    short_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Short Name'}),
        required=False, max_length=100)
    
    designation = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Designation','required':False}),
        required=False, max_length=100)

    class Meta:
        model = Profile
        fields = ("name", "image", "faculty","short_name", "department")
