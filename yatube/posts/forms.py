
from django import forms
from posts.models import Post
from django.contrib.auth import get_user_model

User = get_user_model()


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group',)
        labels = {
            'text': ('Текст'),
            'group': ('Группа'),
        }
        help_texts = {
            'text': ('хелп текстс текст'),
            'group': ('хелп текстс групс'),
        }

    def clean_text(self):
        data = self.cleaned_data['text']
        if data.lower() == '':
            raise forms.ValidationError('и что ты хотел этим сказать?')
        return data
