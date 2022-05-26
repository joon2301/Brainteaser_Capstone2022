from django.forms import ModelForm, Textarea
from .models import Comment

class commentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['Comment']
        widgets = {
            'Comment': Textarea(attrs={
               'class': 'form-control',
                'rows': '3',
                'placeholder': '댓글을 입력 해주세요!',
                'required': True,
            }),
        }
