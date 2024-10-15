from django.contrib.auth.models import User
from django import forms
from .models import Profile, Blog, User, Comment
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm

class LoginForm(forms.Form):
    # Create a field for the username
    username = forms.CharField(label = 'Username', max_length = 100, required = True, widget = forms.TextInput(attrs = {
        'class':'form-control', 'placeholder':'Enter the username'
    }))

    # Create a field for the password
    password = forms.CharField(label = 'password', max_length = 100, required =True, widget=forms.PasswordInput(attrs={
        'class':'form-control','placeholder':'Enter the password'
    }))

    # Tell the form which model it should use.
    class Meta:
        model = User
        # Include these fields in the form
        fields = ['username','email','password']





class BlogForm(forms.ModelForm):
    title = forms.CharField(label='Blog Title', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter the title of the blog'
    }))

    author = forms.ModelChoiceField(label='Author Name', queryset=User.objects.all(),widget=forms.Select(attrs={
        'class': 'form-control',
        'placeholder': 'Enter the name of the author'
    }))

    description = forms.CharField(label='Content', widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Write your content here...',
        'rows':5
    }))

    blog_image = forms.ImageField(label='Image', widget=forms.ClearableFileInput(attrs={
        'class': 'form-control',
        'placeholder': 'Upload your image'
    }))

    status = forms.ChoiceField(label='Status', choices=[('draft', 'Draft'), ('published', 'Published')], widget=forms.Select(attrs={
        'class': 'form-control',
        'placeholder': 'Enter the title of the blog'
    }))

    class Meta:
        model = Blog
        fields = ['title','author','description','blog_image', 'status']
    
class CommentForm(forms.ModelForm):
    comment = forms.CharField(label = 'Comment', widget = forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your comment here...'
    }))
    class Meta:
        model = Comment
        fields=['comment']

# Form for changing user passwords
class AdminResetForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    #fields to use in this form
    class Meta:
        fields = ['old_password1', 'new_password3', 'new_password4']
