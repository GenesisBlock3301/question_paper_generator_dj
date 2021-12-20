from django import forms
from question_generator.models import Department,Faculty,Profile

class ProfileForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Name'}),
        required=True, max_length=100)
    id_no = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'ID NO'}),
        required=True, max_length=100)
    faculty = forms.CharField(
        widget=forms.Select(
            attrs={'class': 'form-select form-select-lg mb-3'},
            choices=Faculty.objects.all().values_list('faculty_name', 'faculty_name')))
    department = forms.CharField(
        widget=forms.Select(
            attrs={'class': 'form-select form-select-lg mb-3'},
            choices=Department.objects.all().values_list('department_name', 'department_name')))

    class Meta:
        model = Profile
        fields = ("name", "id_no", "faculty", "department")
