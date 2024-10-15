from django.shortcuts import render, redirect, get_object_or_404
from adminpanel.models import Profile, Blog, Comment, User
from .forms import BlogForm, CommentForm, LoginForm, AdminResetForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.urls import reverse


def is_staff(user):
    # Check if the user is a staff member
    return user.is_staff



def admin_login(request):
    # Check if the form is submitted (a POST request)
    if request.method == 'POST':
        # Create a form object with the data from the submitted form
        form = LoginForm(request.POST)
        # Check if the form data is correct and valid
        if form.is_valid():
            # Get the username from the form data
            username = form.cleaned_data.get('username')
            # Get the password from the form data
            password = form.cleaned_data.get('password')
            # Check if the username and password match a user in the database
            user = authenticate(request, username=username, password=password)
            # If the user exists and is an admin/staff member
            if user is not None and user.is_staff:
                # Log the user in (start the session)
                login(request, user)
                # Redirect the user to the admin home page
                return redirect('adminhome') 
            else:
                # If the username, password, or authorization is wrong, show an error message
                messages.error(request, 'Invalid Username or password or not authorized.')
                # Redirect the user back to the login page
                return redirect('admin_login')  
    else:
        # If the form is not submitted, just create a blank form
        form = LoginForm()
    # Show the login page with the form
    return render(request, 'adminpanel/admin_login.html', {'form': form})


@login_required(login_url='/404/')
@user_passes_test(is_staff)
def adminhome(request):
    # Get the search query from the URL
    query = request.GET.get('query', '')
    
    if query:
        # If there is a search query, filter blogs by title
        blogs = Blog.objects.filter(title__icontains=query)
    else:
        # If no search query, get all blogs
        blogs = Blog.objects.all()

    # Get statistics about users and blogs
    total_users = User.objects.count()
    inactive_users = User.objects.filter(is_active=False).count()
    total_blogs = Blog.objects.count()
    hidden_blogs = Blog.objects.filter(status='draft').count()
    users = User.objects.all()  # Get all users

    if request.method == 'POST':
        # Handle hiding or showing blogs
        if 'hide_blog' in request.POST or 'show_blog' in request.POST:
            # Get the blog ID from the POST request
            blog_id = request.POST.get('blog_id')
            # Find the blog with the given ID
            blog = get_object_or_404(Blog, id=blog_id)

            if 'hide_blog' in request.POST and request.user.is_staff:
                # If the hide_blog action is in the POST request and user is staff
                blog.status = 'draft'  # Set blog status to draft (hidden)
                blog.save()
                # Show a success message
                messages.success(request, 'Blog has been hidden.')
                # Redirect back to the admin home page
                return redirect('adminhome')
                
            elif 'show_blog' in request.POST and request.user.is_staff:
                # If the show_blog action is in the POST request and user is staff
                blog.status = 'visible'  # Set blog status to visible
                blog.save()
                # Show a success message
                messages.success(request, 'Blog is now visible.')

            # Redirect back to the admin home page
            return redirect('adminhome')  # Redirect after hiding/showing blog

    # Create context with blog and user statistics
    context = {
        'blogs': blogs,
        'total_users': total_users,
        'inactive_users': inactive_users,
        'total_blogs': total_blogs,
        'hidden_blogs': hidden_blogs,
        'users': users,
        'query': query,  # Include the search query in the context
    }

    # Render the admin home page with the context
    return render(request, 'adminpanel/admin_home.html', context)

@login_required(login_url='/404/')
@user_passes_test(is_staff)
def user_list(request, user_id=None):
    # Handle POST requests for activating or deactivating users
    if request.method == 'POST':
        # Get the user ID and action from the POST request
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        
        if user_id and action:
            # Find the user with the given ID
            user = get_object_or_404(User, id=user_id)
            
            if action == 'activate':
                # Activate the user
                user.is_active = True
                user.save()
                # Show a success message
                messages.success(request, f'User {user.username} activated.')
                
            elif action == 'deactivate':
                # Deactivate the user
                user.is_active = False
                user.save()
                # Show a success message
                messages.success(request, f'User {user.username} deactivated.')

            # Redirect to the user list page
            return HttpResponseRedirect(reverse('user_list'))

    # Handle GET requests for searching users
    query = request.GET.get('q', '')
    if query:
        # Search users by username or email
        users = User.objects.filter(username__icontains=query) | User.objects.filter(email__icontains=query)
    else:
        # Get all users if no search query
        users = User.objects.all()

    if user_id:
        # Show detailed view for a specific user
        user = get_object_or_404(User, id=user_id)
        return render(request, 'adminpanel/admin_view_user.html', {'user': user})

    # Show list of active and inactive users
    active_users = users.filter(is_active=True)
    inactive_users = users.filter(is_active=False)
    
    return render(request, 'adminpanel/user_list.html', {
        'users': users,
        'active_users': active_users,
        'inactive_users': inactive_users,
        'search_query': query,  # Include the search query in the context
    })


@user_passes_test(is_staff)
@login_required(login_url='/404/')
def blog_list(request):
    # Handle POST requests for hiding or showing blogs
    if request.method == 'POST':
        if 'hide_blog' in request.POST:
            # Get the blog ID from the POST request
            blog_id = request.POST.get('hide_blog')
            if request.user.is_staff:
                # Find the blog with the given ID
                blog = get_object_or_404(Blog, id=blog_id)
                # Set blog status to draft (hidden)
                blog.status = 'draft'
                blog.save()
                # Show a success message
                messages.success(request, 'Blog has been hidden.')
                # Redirect back to the blog list page
                return redirect('blog_list')

        elif 'show_blog' in request.POST:
            # Get the blog ID from the POST request
            blog_id = request.POST.get('show_blog')
            if request.user.is_staff:
                # Find the blog with the given ID
                blog = get_object_or_404(Blog, id=blog_id)
                # Set blog status to visible
                blog.status = 'visible'
                blog.save()
                # Show a success message
                messages.success(request, 'Blog is now visible.')
                # Redirect back to the blog list page
                return redirect('blog_list')

    # Handle GET requests for searching blogs
    query = request.GET.get('q', '')
    if query:
        # Search in visible and hidden blogs by title
        visible_blogs = Blog.objects.filter(status='visible', title__icontains=query)
        hidden_blogs = Blog.objects.filter(status='draft', title__icontains=query)
    else:
        # Show all visible and hidden blogs
        visible_blogs = Blog.objects.filter(status='visible')
        hidden_blogs = Blog.objects.filter(status='draft')

    # Create context with visible and hidden blogs
    context = {
        'visible_blogs': visible_blogs,
        'hidden_blogs': hidden_blogs,
        'search_query': query,  # Include the search query in the context
    }

    # Render the blog list page with the context
    return render(request, 'adminpanel/blog_list.html', context)



@login_required(login_url='/404/')
@user_passes_test(is_staff)
def blog_view(request, blog_id):
    # Get the blog with the given ID or show a 404 page if not found.
    blog = get_object_or_404(Blog, id=blog_id)
    
    # Check if the user is not an admin and the blog is hidden.
    if not request.user.is_staff and blog.status == 'hidden':
        # Show an error message and redirect to the home page.
        messages.error(request, 'This blog is not visible.')
        return redirect('adminhome')

    # Get comments for this blog.
    comments = Comment.objects.filter(blog=blog)
    # Check if the user is not an admin.
    if not request.user.is_staff:
        # Show only visible comments if the user is not an admin.
        comments = comments.filter(status='visible')
    
    # Count the number of comments.
    count = comments.count()

    # Check if the form was submitted.
    if request.method == 'POST':
        # Check if the 'hide_blog' button was pressed.
        if 'hide_blog' in request.POST:
            # Check if the user is an admin.
            if request.user.is_staff:
                # Set the blog status to 'draft' to hide it.
                blog.status = 'draft'
                blog.save()
                # Show a success message.
                messages.success(request, 'Blog has been hidden.')
                return redirect('blog_view', blog_id=blog.id)

        # Check if the 'show_blog' button was pressed.
        elif 'show_blog' in request.POST:
            # Check if the user is an admin.
            if request.user.is_staff:
                # Set the blog status to 'visible' to show it.
                blog.status = 'visible'
                blog.save()
                # Show a success message.
                messages.success(request, 'Blog is now visible.')
                return redirect('blog_view', blog_id=blog.id)

        # Check if the 'comment_action_hide' button was pressed.
        elif 'comment_action_hide' in request.POST:
            # Get the comment ID from the POST request.
            comment_id = request.POST.get('comment_action_hide')
            # Check if the user is an admin.
            if request.user.is_staff:
                # Get the comment with the given ID.
                comment = get_object_or_404(Comment, id=comment_id, blog=blog)
                # Set the comment status to 'hidden'.
                comment.status = 'hidden'
                comment.save()
                # Show a success message.
                messages.success(request, 'Comment has been hidden.')

        # Check if the 'comment_action_show' button was pressed.
        elif 'comment_action_show' in request.POST:
            # Get the comment ID from the POST request.
            comment_id = request.POST.get('comment_action_show')
            # Check if the user is an admin.
            if request.user.is_staff:
                # Get the comment with the given ID.
                comment = get_object_or_404(Comment, id=comment_id, blog=blog)
                # Set the comment status to 'visible'.
                comment.status = 'visible'
                comment.save()
                # Show a success message.
                messages.success(request, 'Comment is now visible.')

        # Create a form with the submitted data.
        form = CommentForm(request.POST)
        # Check if the form is valid.
        if form.is_valid():
            # Create a new comment from the form data but do not save it yet.
            comment = form.save(commit=False)
            # Set the author of the comment to the current user.
            comment.author = request.user
            # Set the blog of the comment to the current blog.
            comment.blog = blog
            # Save the comment to the database.
            comment.save()
            # Show a success message.
            messages.success(request, 'Comment added successfully!')
            # Redirect to the blog view page.
            return redirect('blog_view', blog_id=blog.id)
    else:
        # Create an empty form if it is not a POST request.
        form = CommentForm()

    # Prepare context data to pass to the template.
    context = {
        'blog': blog,
        'comments': comments,
        'count': count,
        'form': form,
        'user': request.user
    }
    
    # Render the blog view page with the context data.
    return render(request, 'adminpanel/blog_view.html', context)


@login_required(login_url='/404/')
@user_passes_test(is_staff)
def reset_password(request):
    # Create a form object to reset the password, with the current user's data
    form = AdminResetForm(user=request.user, data=request.POST or None)
    
    # If the form is submitted and the form data is correct
    if request.method == 'POST' and form.is_valid():
        # Save the new password for the user
        form.save()
        # Show a message that the password was updated successfully
        messages.success(request, 'Password updated successfully! Please log in again.')
        # Redirect the user to the admin login page since they need to log in with the new password
        return redirect('admin_login')  
    
    return render(request, 'adminpanel/reset_password.html', {'form': form})

   
@login_required(login_url='/404/')
@user_passes_test(is_staff)
def user_profile(request, user_id):
    # Get the user with the given ID or show a 404 page if not found.
    user = get_object_or_404(User, id=user_id)
    
    # Check if the form was submitted.
    if request.method == 'POST':
        # Get the action from the POST request.
        action = request.POST.get('action')
        
        # Check if the action is to activate the user.
        if action == 'activate':
            # Set the user's status to active.
            user.is_active = True
            user.save()
            # Show a success message.
            messages.success(request, f'User {user.username} activated.')
        # Check if the action is to deactivate the user.
        elif action == 'deactivate':
            # Set the user's status to inactive.
            user.is_active = False
            user.save()
            # Show a success message.
            messages.success(request, f'User {user.username} deactivated.')
        
        # Redirect to the user profile page after the action.
        return HttpResponseRedirect(reverse('user_profile', args=[user.id]))
    
    # Render the user profile page with the user data.
    return render(request, 'adminpanel/admin_view_user.html', {'user': user})



@login_required(login_url='/404/')
@user_passes_test(is_staff)
# Function to handle user logout
def logout(request):
    # Log out the user.
    auth_logout(request)
    # Redirect to the home page after logging out.
    return redirect('siteadmin')
