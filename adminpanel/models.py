from django.db import models
from django.contrib.auth.models import User

# Create a Profile model to store extra information about users.
class Profile(models.Model):
    # Link this profile to a user.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Store the user's phone number.
    phone = models.CharField(max_length=10)
    # Store a description about the user.
    profile_description = models.TextField()
    # Store the user's profile picture.
    profile_image = models.ImageField(upload_to='profile_images/')
    # Store the user's ID proof image.
    id_proof = models.ImageField(upload_to='id_proof/')

    # Return the username when the profile is shown as a string.
    def __str__(self):
        return self.user.username

# Create a Blog model to store blog posts.
class Blog(models.Model):
    # Store the title of the blog.
    title = models.CharField(max_length=200)
    # Link this blog to an author (user).
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # Store an image related to the blog.
    description = models.TextField()
    # Automatically set the date and time when the blog is created.
    blog_image = models.ImageField(upload_to='blog_content', blank = True, null = True)
    # Automatically set the date and time when the blog is updated.
    created_at = models.DateTimeField(auto_now_add=True)
    # Automatically set the date and time when the blog is updated.
    updated_at = models.DateTimeField(auto_now=True)
     # Store the status of the blog (default is 'visible').
    status = models.CharField(max_length=20, default = 'visible')

    # Return the title of the blog when it is shown as a string.
    def __str__(self):
        return self.title

# Create a Comment model to store comments on blogs.
class Comment(models.Model):
    # Store the content of the comment.
    comment = models.TextField()
    # Link this comment to an author (user).
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # Link this comment to a blog.
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    # Automatically set the date and time when the comment is created.
    created_at = models.DateTimeField(auto_now_add=True)
    # Automatically set the date and time when the comment is updated.
    updated_at = models.DateTimeField(auto_now=True)
    # Store the status of the comment (default is 'visible').
    status = models.CharField(max_length=20, default = 'visible')

    # Return a string showing who wrote the comment and which blog it is on.
    def __str__(self):
        return f'Comment by {self.author.username} on {self.blog.title}'
