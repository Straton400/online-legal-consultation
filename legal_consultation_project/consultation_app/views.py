from django.shortcuts import render
from .models import Lawyer  # Import your models
from django.shortcuts import render, get_object_or_404
from .models import Lawyer, Client, Consultation
from django.db.models import Q
# Create your views here.

from django.shortcuts import render, redirect
from .forms import LawyerRegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import LawyerProfileForm, ClientRegistrationForm
from .models import LawyerProfile
from django.contrib.auth.decorators import login_required
from .models import Client
from .forms import ConsultationRequestForm
from .models import Lawyer, Consultation

from .forms import ConsultationUpdateForm



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
                return redirect('lawyer_dashboard')  # 
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LawyerLoginForm()
    return render(request, 'lawyer_login.html', {'form': form})

# lawyeer dashboard
from .models import Consultation

# views.py

def lawyer_dashboard(request):
    lawyer = request.user
    consultations = Consultation.objects.filter(lawyer=lawyer).order_by('-requested_at')
    
    # Filter the consultations that are pending as notifications
    pending_notifications = consultations.filter(status='pending')
    
    if request.method == 'POST':
        consultation_id = request.POST.get('consultation_id')
        consultation = get_object_or_404(Consultation, id=consultation_id)
        
        form = ConsultationUpdateForm(request.POST, instance=consultation)
        if form.is_valid():
            form.save()
            messages.success(request, "Consultation status updated successfully!")
            return redirect('lawyer_dashboard')
    else:
        form = ConsultationUpdateForm()

    context = {
        'consultations': consultations,
        'notifications': pending_notifications,
        'form': form,
    }
    return render(request, 'lawyer_base.html', context)


def lawyer_logout(request):
    auth_logout(request)
    messages.success(request, 'Successfully logged out.')
    return redirect('home')


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
    query = request.GET.get('q')
    if query:
        lawyers = LawyerProfile.objects.filter(
            Q(specialization__icontains=query)
        ).select_related('lawyer')
    else:
        lawyers = LawyerProfile.objects.all().select_related('lawyer')
    
    return render(request, 'lawyer_list.html', {'lawyers': lawyers})

#about view
def about_page(request):
    return render(request, 'about.html')


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

            # Get the 'next' parameter and redirect there if it exists
            next_page = request.GET.get('next')
            if next_page:
                return redirect(next_page)

            # Default redirect if there is no 'next'
            return redirect('client_dashboard')
        
        except Client.DoesNotExist:
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'login.html')


# client dashboard
def client_dashboard(request):
    if not request.session.get('client_id'):
        return redirect('client_login')

    client_id = request.session.get('client_id')
    client = Client.objects.get(id=client_id)

    # Fetch all consultations for the client
    consultations = Consultation.objects.filter(client=client).order_by('-requested_at')

    context = {
        'first_name': client.first_name,
        'consultations': consultations  # Pass the consultations to the template
    }
    return render(request, 'client_base.html', context)

#view for admin dashboard
# views.py



def admin_dashboard(request):
    # Fetch total counts
    total_lawyers = Lawyer.objects.count()
    total_clients = Client.objects.count()
    active_consultations = Consultation.objects.filter(status='active').count()

    # Fetch recent activities (limit to 5 most recent activities)
    recent_activities = Consultation.objects.all().order_by('-created_at')[:5]

    # Pass the data to the template
    context = {
        'total_lawyers': total_lawyers,
        'total_clients': total_clients,
        'active_consultations': active_consultations,
        'recent_activities': recent_activities,
    }
    return render(request, 'admin/dashboard.html', context)



#legal news view
from .models import LegalArticle

def legal_news_list(request):
    articles = LegalArticle.objects.all().order_by('-published_date')
    return render(request, 'legal_news.html', {'articles': articles})

def legal_news_detail(request, slug):
    article = get_object_or_404(LegalArticle, slug=slug)
    return render(request, 'legal_detail.html', {'article': article})


#view to allow client to view the profile of lawyer
def lawyer_detail(request, pk):
    lawyer = get_object_or_404(LawyerProfile, pk=pk)
    return render(request, 'lawyer_detail.html', {'lawyer': lawyer})



#view to hundle consultation request to the laywer
def consultation_requests_view(request):
    # Get the logged-in lawyer object directly
    lawyer = request.user
    consultations = Consultation.objects.filter(lawyer=lawyer).order_by('-requested_at')

    context = {
        'consultations': consultations
    }
    return render(request, 'consultation_requests.html', context)


#view to hundle cosultation detalis
def consultation_detail_view(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)

    # Optional: restrict access so only the assigned lawyer can view it
    if request.user != consultation.lawyer:
        return redirect('lawyer_dashboard')

    context = {
        'consultation': consultation
    }
    return render(request, 'details_consultation.html', context)

#view the client to request consultation 
def request_consultation(request, lawyer_id):
    # Check if user is logged in
    if not request.session.get('client_id'):
        # Redirect to login with the 'next' parameter
        return redirect(f'/client-login/?next=/request-consultation/{lawyer_id}/')

    lawyer = get_object_or_404(Lawyer, id=lawyer_id)

    if request.method == 'POST':
        form = ConsultationRequestForm(request.POST)
        if form.is_valid():
            consultation = form.save(commit=False)
            consultation.client_id = request.session.get('client_id')
            consultation.lawyer = lawyer
            consultation.save()
            return redirect('client_dashboard')
    else:
        form = ConsultationRequestForm()

    return render(request, 'request_consultation.html', {'lawyer': lawyer, 'form': form})


# view the lawyer to updte consulttion


def update_consultation_status(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)

    if request.method == 'POST':
        status = request.POST.get('status')
        scheduled_time = request.POST.get('scheduled_time')
        message_from_lawyer = request.POST.get('message_from_lawyer')

        # Update status, scheduled time, and message
        consultation.status = status
        consultation.message_from_lawyer = message_from_lawyer
        
        if scheduled_time:
            consultation.scheduled_time = scheduled_time

        if status == 'accepted':
            consultation.is_client_notified = False
            consultation.is_lawyer_notified = True
            messages.success(request, "Consultation Approved. The client will be notified.")
        elif status == 'rejected':
            consultation.is_client_notified = False
            consultation.is_lawyer_notified = True
            messages.warning(request, "Consultation Rejected. The client will be notified.")

        consultation.save()
        return redirect('consultation_requests')


#view to fetch the consultation request of login client 
def client_consultations_view(request):
    # Fetch the client ID from the session
    client_id = request.session.get('client_id')
    
    if not client_id:
        return redirect('client_login')  # Redirect if not logged in
    
    # Get the client object
    try:
        client = Client.objects.get(id=client_id)
    except Client.DoesNotExist:
        return redirect('client_login')
    
    # Fetch all consultations for this client
    consultations = Consultation.objects.filter(client=client).order_by('-requested_at')
    
    context = {
        'consultations': consultations
    }
    return render(request, 'client_consultations.html', context)





def delete_consultation(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)
    
    # Only allow deletion if the client is the owner of the request
    if request.session.get('client_id') == consultation.client.id:
        consultation.delete()
        messages.success(request, "Consultation request successfully deleted.")
    else:
        messages.error(request, "You are not authorized to delete this request.")
    
    return redirect('client_consultations_view')