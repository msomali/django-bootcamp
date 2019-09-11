from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from first_app.models import Topic, Webpage, AccessRecord
from first_app.forms import RegUser, UserForm, UserProfileInfoForm

# For Login including HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    """
    My First View
    Each View must return a HttpResponse
    The parameter to pass can be anything not request
    We can also pass some HTML instead of a string Hello World!
    For us to see this view when we are running our server, we have to map this view to the urls.py file.
    """
    # return HttpResponse("Hello World!")
    # my_dict = {'insert_me':"I'm coming from the view.py!"}

    webpages_list = AccessRecord.objects.order_by('date')
    date_dict = {'access_records': webpages_list}
    return render(request, 'first_app/index.html', context=date_dict)

def regUser(request):
    form = RegUser()

    # Check if the request method is POST
    if request.method == 'POST':
        form = RegUser(request.POST)

        # Check if form is valid
        if form.is_valid():
            # Do something here
            print("Validation Success!")
            print("Name: " + form.cleaned_data['name'])
            print("Email: " + form.cleaned_data['email'])
            print("Text: " + form.cleaned_data['text'])
    return render(request, 'first_app/reg_user.html', {'form':form})

def home(request):
    cont_dict = {'text':"hello world!",'number':100}
    return render(request, 'first_app/home.html', cont_dict)

def other(request):
    return render(request, 'first_app/other.html')

def relative(request):
    return render(request, 'first_app/relative_url_templates.html')

def index5(request):
    return render(request, 'first_app/index5.html')

def register(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # Save form to a database
            user = user_form.save()
            # Hash the password
            user.set_password(user.password)
            # Save the password to the user information
            user.save()

            profile = profile_form.save(commit=False)
            # OneToOne Relationship
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(user.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'first_app/registration.html',
                    {'registered':registered,
                    'user_form':user_form,
                    'profile_form':profile_form}
                    )

# Special Message after login
@login_required
def special(request):
    return HttpResponse("You are logged in, Nice!")

# Logout View
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index5'))

def user_login(request):
    # Check if user submitted data
    if request.method == 'POST':
        # Save submitted data to variables
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the submitted data
        user = authenticate(username=username, password=password)

        # Check if user exists
        if(user):
            # If user is active
            if user.is_active:
                # Allow the user to login
                login(request, user)
                return HttpResponseRedirect(reverse('index5'))
            else:
                return HttpResponse("Account is not active!")
        else:
            #These will print to the console
            print("Someone tried to login and failed!")
            print("Username: {} and Password: {}".format(username,password))
            # This will return to page
            return HttpResponse("Invalid login details supplied!")
    else:
        return render(request, 'first_app/login.html', {})