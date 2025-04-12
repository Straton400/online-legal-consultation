from django.shortcuts import render
from .models import Lawyer  # Import your models
from django.shortcuts import render, get_object_or_404

# Create your views here.

from django.shortcuts import render, redirect
from .forms import LawyerRegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import LawyerProfileForm, ClientRegistrationForm
from .models import LawyerProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from .models import LegalNews
from .models import Client


def home(request):
    return render(request, 'index.html')

#view for lawyer regestration   
def lawyer_register(request):
    if request.method == 'POST':
        form = LawyerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('lawyer_login')  # Redirect to login page
        else:
            messages.error(request, "Registration failed. Please inter the correct information.")
    else:
        form = LawyerRegistrationForm()

    return render(request, 'lawyer_register.html', {'form': form})

#login view for lawyer

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate user
        lawyer = authenticate(request, username=username, password=password)
        
        if lawyer is not None:
            # Log the user in
            login(request, lawyer)
            messages.success(request, "You have successfully logged in!")
            return redirect('lawyer_dashboard')  # Redirect to home or dashboard after login
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('lawyer_login')  # Stay on the login page if authentication fails

    return render(request, 'lawyer_login.html')  # Your login template


# v
# your_app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LawyerLoginForm

def lawyer_login(request):
    if request.method == 'POST':
        form = LawyerLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            lawyer = authenticate(request, username=username, password=password)
            if lawyer is not None:
                login(request, lawyer)
                messages.success(request, f'Successfully logged in as {username}!')
                # Redirect to the lawyer's dashboard or a success page
                return redirect('lawyer_dashboard')  # Replace 'lawyer_dashboard' with your actual URL name
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LawyerLoginForm()
    return render(request, 'lawyer_login.html', {'form': form})

# lawyeer dashboard
def lawyer_dashboard(request):
    if request.user.is_authenticated and isinstance(request.user, Lawyer):
        context = {
            # You might have other context variables here
        }
        return render(request, 'lawyer_dashboard.html', context)
    else:
        return redirect('lawyer_login')
def lawyer_logout(request):
    auth_logout(request)
    messages.success(request, 'Successfully logged out.')
    return redirect('home')

@login_required
def create_lawyer_profile(request):
    # Check if the lawyer already has a profile
    if hasattr(request.user, 'lawyerprofile'):  # Ensure you check for 'lawyerprofile', not 'lawyer'
        return redirect('lawyer_dashboard')  # or wherever you want to redirect

    if request.method == 'POST':
        form = LawyerProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.lawyer = request.user  # Link the profile to the logged-in lawyer (user)
            profile.save()
            return redirect('lawyer_dashboard')  # or a success page
    else:
        form = LawyerProfileForm()

    return render(request, 'create_profile.html', {'form': form})


#view for list available lawyer
def lawyer_list(request):
    lawyers = LawyerProfile.objects.filter(is_available=True)  # show only available ones
    return render(request, 'lawyer_list.html', {'lawyers': lawyers})

#about view
def about_page(request):
    return render(request, 'about.html')


#view to handle legal news
def legal_news(request):
    # Fetch the latest legal news
    latest_news = LegalNews.objects.all()
    featured_news = LegalNews.objects.filter(is_featured=True)

    context = {
        'latest_news': latest_news,
        'featured_news': featured_news,
    }

    return render(request, 'legal_news.html', context)


def legal_news_detail(request, pk):
    news_item = get_object_or_404(LegalNews, pk=pk)
    return render(request, 'legal_news_detail.html', {'news_item': news_item})

#client regestration 
def client_register(request):
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client registered successfully!')
            return redirect('client_login')  # We'll define this next
    else:
        form = ClientRegistrationForm()
    return render(request, 'register.html', {'form': form})



#client login
def client_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            client = Client.objects.get(email=email, password=password)
            request.session['client_id'] = client.id
            messages.success(request, 'Login successful')
            return redirect('client_dashboard')  # You'll define this later
        except Client.DoesNotExist:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

# client dashboard
@login_required
def client_dashboard(request):
    return render(request, 'client_dashboard.html')