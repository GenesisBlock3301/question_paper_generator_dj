from django import forms
from . models import Question,Course
from ckeditor.widgets import CKEditorWidget



DIFFICULTY = [
        ('E', 'Easy'),
        ('M', 'Medium'),
        ('H', 'Hard'),
]
class CreationQuestionForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title', 'name': 'title'}),
        required=True, max_length=100)
    full_mark = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Mark', 'name': 'full_mark'}),
        required=True, max_length=100)
    difficulty_level = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-control'},choices=DIFFICULTY),
        required=True, max_length=100)
    body = forms.CharField(
        widget=CKEditorWidget(attrs={'class': 'form-control', 'name': 'body'}),
        required=True, max_length=100)


    class Meta:
        model = Question
        fields = ("title","full_mark","course","difficulty_level","body")
        # fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.all()
        print("self data",self.data)

        # if 'country' in self.data:
        #     try:
        #         country_id = int(self.data.get('country'))
        #         self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
        #     except (ValueError, TypeError):
        #         pass  # invalid input from the client; ignore and fallback to empty City queryset
        # elif self.instance.pk:
        #     self.fields['city'].queryset = self.instance.country.city_set.order_by('name')