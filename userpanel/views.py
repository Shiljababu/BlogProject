from django.shortcuts import render, redirect, get_object_or_404
from adminpanel.models import Profile, Blog, Comment, User
from .forms import BlogForm, CommentForm, ProfileForm, ResetForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout


# Ensure user is logged in, redirect to 404 if not
@login_required(login_url='/404/')
def userhome(request):
    # Get the search query from the URL
    query = request.GET.get('q', '')
    
    if query:
        # Search blogs by title or description with the query
        blogs = Blog.objects.filter(status='visible', title__icontains=query) | Blog.objects.filter(status='visible', description__icontains=query)
    else:
       # If no search query, get all visible blogs
        blogs = Blog.objects.filter(status='visible')
     # Render the page with the blogs
    return render(request, 'userpanel/user_home.html', {'blogs': blogs})



@login_required(login_url = '/404/')
# create a function to show named account settings
def account_settings(request):
    # Render the view_profile template as account settings is a dropdown list
    return render(request, 'userpanel/view_profile.html')


@login_required(login_url = '/404/')
#create a function to add new blog posts
def upload_blog(request):
    # If the request is a POST (form submission)
    if request.method == 'POST':
        # Create a form with the data and files submitted
        form = BlogForm(request.POST, request.FILES)
        # Checks if the form data is valid
        if form.is_valid():
            # if valid save the new blog post to the database
            blog = form.save(commit=False)
            blog.author = request.user  # Assign the logged-in user as the author
            blog.save()
            messages.success(request, 'Blog updated successfully!!!')
            # Redirect to the home page after saving
            return redirect('userhome')
    else:
         # If not a POST request, create an empty form
        form = BlogForm()
    # Render the template for uploading a blog with the form
    return render(request, 'userpanel/add_blog.html', {'form':form})


def deactivate_account(request):
    # If the request is a POST (form submission)
    if request.method == 'POST':  
         # Get the logged-in user
        user = request.user  # Get the logged-in user
        user.is_active = False  # Deactivate the user account
        user.save()  # Save changes to the database
        messages.success(request, 'Your account has been deactivated.')  # Show success message
        return redirect('logout')  # Redirect to logout
    else:
        return redirect('userprofile')  # Redirect to user profile if not a POST request

@login_required(login_url = '/404/')
# Function to handle editing an existing blog post
def edit_blog(request, blog_id):
    # Get the blog post with the given ID or show a 404 error if not found
    blog = get_object_or_404(Blog, id=blog_id)
    # Check if the logged-in user is the author of the blog post
    if blog.author != request.user:
        # Redirect to the home page if the user is not the author
        return redirect('userhome')
    # If the request is a POST (form submission)
    if request.method == 'POST':
        # Create a form instance with the submitted data and files
        form = BlogForm(request.POST, request.FILES, instance=blog)
        # Check if the form data is valid
        if form.is_valid():
            # Save the updated blog post to the database
            form.save()
            # Show a success message and redirect to the blog view page
            messages.success(request, 'Blog updated successfully!!!')
            return redirect('view_blog', blog_id=blog.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # If not a POST request, create a form instance with the existing blog post
        form = BlogForm(instance=blog)
    # Render the template for editing the blog post with the form
    return render(request, 'userpanel/edit_blog.html', {'form': form, 'blog':blog})


# Function to display a single blog post along with comments
@login_required(login_url='/404/')
def view_blog(request, blog_id):
    # Get the blog by its ID, or show a 404 error if the blog is not found
    blog = get_object_or_404(Blog, id=blog_id)

    # Get all comments for this blog that are visible
    comments = Comment.objects.filter(blog=blog, status='visible')
    # Count how many comments there are
    count = comments.count()
    # Prepare a variable to hold a comment that may be edited
    comment_to_edit = None

    form = CommentForm()
    # If the form is submitted (a POST request)
    if request.method == 'POST':
        # If the form has a delete comment ID
        if 'delete_comment_id' in request.POST:
            # Get the ID of the comment to delete
            comment_id = request.POST.get('delete_comment_id')
            # Find the comment with this ID for this blog, or show a 404 error if not found
            comment = get_object_or_404(Comment, id=comment_id, blog=blog)
            # If the current user is the author of the comment
            if comment.author == request.user:
                # Delete the comment
                comment.delete()
                # Show a success message
                messages.success(request, 'Comment deleted successfully!')
        
        # If the form has an edit comment ID
        elif 'edit_comment_id' in request.POST:
            # Get the ID of the comment to edit
            comment_id = request.POST.get('edit_comment_id')
            # Find the comment with this ID for this blog, or show a 404 error if not found
            comment_to_edit = get_object_or_404(Comment, id=comment_id, blog=blog)

            # If the current user is the author of the comment
            if comment_to_edit.author == request.user:
                # Create a form with the comment data to edit it
                form = CommentForm(request.POST, instance=comment_to_edit)

                # If the form data is correct
                if form.is_valid():
                    # Save the changes to the comment
                    form.save()
                    # Show a success message
                    messages.success(request, 'Comment updated successfully!')
                    # Go back to the blog view page
                    return redirect('view_blog', blog_id=blog.id)
                else:
                    # Show an error message if the form has problems
                    messages.error(request, f'Error updating comment:')
            else:
                # Show an error message if the user is not the author of the comment
                messages.error(request, 'You are not authorized to edit this comment.')
            # Go back to the blog view page
            return redirect('view_blog', blog_id=blog.id)
        
        else:
            # Create a form
            form = CommentForm(request.POST)
            # If the form data is correct
            if form.is_valid():
                # Save the new comment but don't commit to the database yet
                comment = form.save(commit=False)
                # Set the author of the comment to the current user
                comment.author = request.user
                # Set the blog for the comment
                comment.blog = blog
                # Save the comment to the database
                comment.save()
                # Show a success message
                messages.success(request, 'Comment added successfully!')
                # Go back to the blog view page
                return redirect('view_blog', blog_id=blog.id)
            else:
                # Show an error message if the form has problems
                messages.error(request, f'Error adding comment:')
    
    else:
        # If the form is not submitted, create a blank form
        form = CommentForm()
        # If there is an edit comment ID in the URL
        if 'edit_comment_id' in request.GET:
            # Get the ID of the comment to edit
            comment_id = request.GET.get('edit_comment_id')
            # Find the comment with this ID for this blog, or show a 404 error if not found
            comment_to_edit = get_object_or_404(Comment, id=comment_id, blog=blog)
            # Create a form with the comment data to edit it
            form = CommentForm(instance=comment_to_edit)

    
    context = {
        'blog': blog,  
        'comments': comments,  
        'count': count, 
        'form': form, 
        'comment_to_edit': comment_to_edit,  
        'user': request.user,  
    }

    # Render the blog view page
    return render(request, 'userpanel/view_blog.html', context)


# Ensure user is logged in, redirect to 404 if not
@login_required(login_url='/404/')  
def delete_blog(request, blog_id):
    # Get the blog with the given ID and check if the logged-in user is the author
    blog = get_object_or_404(Blog, id=blog_id, author=request.user)  
    # Delete the blog from the database
    blog.delete() 
    return redirect('my_blogs')  


# Ensure user is logged in, redirect to 404 if not
@login_required(login_url='/404/')  
def my_blogs(request):
     # Get all blogs for the logged-in user
    user_blogs = Blog.objects.filter(author=request.user) 
    # Get published blogs
    published_blogs = user_blogs.filter(status='visible')  
     # Get draft blogs
    draft_blogs = user_blogs.filter(status='draft') 
    # Get all blogs for the user
    all_blogs = user_blogs  

    return render(request, 'userpanel/my_blog.html', {
        'blogs': all_blogs,
        'published_blogs': published_blogs,
        'draft_blogs': draft_blogs,
    })  



@login_required(login_url='/404/')
def blog_list(request):
    # Get all blog posts from the database
    blogs = Blog.objects.all()
    # Print blog posts to the console (for debugging purposes)
    print(blogs)
    # Render the template for displaying the list of blogs
    return render(request, 'userpanel/user_blog_list.html', {'blogs': blogs})


@login_required(login_url='/404/')  
def reset(request):
    # If the request is a POST 
    if request.method == 'POST':  
        # Create form with submitted data and current user
        form = ResetForm(user=request.user, data=request.POST) 
        # Check if the form data is valid 
        if form.is_valid(): 
            # Save the new password to the database 
            form.save()  
            # Show success message
            messages.success(request, 'Your password has been updated successfully.')
            return redirect('site_login')  
        else:

            messages.error(request, 'Please correct the errors below.')  # Show error message
    else:
         # Create form for resetting the password if not a POST request
        form = ResetForm(user=request.user) 
    return render(request, 'userpanel/reset_password.html', {'form': form})  


# Function to display the user's profile
@login_required(login_url = '/404/')
def user_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    
# Render the template for displaying the user's profile
    return render(request, 'userpanel/user_profile.html', {'profile': profile})


@login_required(login_url='/404/')
# This function lets users edit their profile.
def edit_profile(request):
    # Try to get the profile for the current user, or create a new one if it doesn't exist
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # If the request is a POST, get the form data and files from the request
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # If the form is valid, save the profile data to the database
            form.save()
            
            # Update the current user's email with the new one from the form
            user = request.user
            user.email = request.POST.get('email', user.email)
            user.save()

            # Show a success message that the profile was updated
            messages.success(request, 'Profile updated successfully!')
            # Redirect the user to their profile page
            return redirect('user_profile')
        else:
            # If the form is not valid, print the errors
            print("Form errors:", form.errors)
    else:
        # If the request is not a POST, create a form with the existing profile data
        form = ProfileForm(instance=profile)
    
    # Prepare the context with the form, user's username, and email
    context = {
        'form': form,
        'username': request.user.username,
        'email': request.user.email,
    }
    
    # Render the edit_profile.html template with the context
    return render(request, 'userpanel/edit_profile.html', context)

@login_required(login_url='/404/')
# This function logs out the current user
def logout(request):
    # Log out the current user
    auth_logout(request)
    # After logging out, redirect to the home page
    return redirect('sitehome')
