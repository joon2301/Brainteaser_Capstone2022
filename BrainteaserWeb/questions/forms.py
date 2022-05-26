from django.forms import ModelForm, Textarea
from .models import TeaserAnswer


class answerForm(ModelForm):
    class Meta:
        model = TeaserAnswer
        fields = ['Answer']
        widgets = {
            'Answer': Textarea(attrs={
               'class': 'form-control',
                'rows': '3',
                'placeholder': '답안을 입력 해주세요!',
                'required': True,
                'id': '0',
            }),
        }


class answerChildForm(ModelForm):
    class Meta:
        model = TeaserAnswer
        fields = ['Answer']

        widgets = {
            'Answer': Textarea(attrs={
               'class': 'form-control',
                'rows': '2',
                'placeholder': '대댓을 입력 해주세요!',
                'required': True,
            }),
        }