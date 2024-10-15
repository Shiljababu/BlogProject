from django.contrib.auth.models import User
from django import forms
from adminpanel.models import Profile, Blog, User, Comment
from django.contrib.auth.forms import PasswordChangeForm

# Form for creating or editing a blog post
class BlogForm(forms.ModelForm):
    # Field for the blog title
    title = forms.CharField(
        label='Blog Title', 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter the title of the blog'
        })
    )

   

    # Field for the blog content
    description = forms.CharField(
        label='Content', 
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Write your content here...',
            'rows': 5
        })
    )

    # Field for uploading a blog image
    blog_image = forms.ImageField(
        label='Image', 
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'placeholder': 'Upload your image'
        }),
        required=False
    )

    # Field for selecting the status of the blog (draft or published)
    status = forms.ChoiceField(
        label='Status', 
        choices=[('draft', 'Draft'), ('visible', 'Published')], 
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'Enter the title of the blog'
        })
    )

    # Connected to the Blog model and choose which fields to use
    class Meta:
        model = Blog
        fields = ['title', 'description', 'blog_image', 'status']

# Form for adding a comment
class CommentForm(forms.ModelForm):
    # Field for the comment 
    comment = forms.CharField(
        label='Comment', 
        widget=forms.Textarea(attrs={
            'class': 'form-control comment-textarea',
            'placeholder': 'Enter your comment here...'
        })
    )

    # Connected to the Comment model and choose which fields to use
    class Meta:
        model = Comment
        fields = ['comment']

# Form for creating or editing user profiles
class ProfileForm(forms.ModelForm):
   

    # Field for the phone number
    phone = forms.IntegerField(
        label='Phone Number', 
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your phone number'
        })
    )

    # Field for the profile description (not required)
    profile_description = forms.CharField(
        label='Description', 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Say about you'
        }), 
        required=False
    )

    # Field for the email (not required)
    

    # Field for the profile image (not required)
    profile_image = forms.ImageField(
        label='Profile Image', 
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'placeholder': 'Upload your profile image'
        }), 
        required=False
    )

    # Field for the ID proof image (not required)
    id_proof = forms.ImageField(
        label='ID Proof', 
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'placeholder': 'Upload your ID proof image'
        }), 
        required=False
    )

    # Connected to the Profile model and choose which fields to use
    class Meta:
        model = Profile
        fields = [ 'phone', 'profile_description', 'profile_image', 'id_proof']

# Form for changing user passwords
class ResetForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    #fields to use in this form
    class Meta:
        fields = ['old_password', 'new_password1', 'new_password2']
