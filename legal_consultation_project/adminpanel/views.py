from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from consultation_app.models import Lawyer, Client, Consultation,LawyerProfile
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from consultation_app.models import LawyerProfile, LegalArticle
from django.contrib.auth.hashers import check_password
from .models import AdminUser
from .forms import AdminLoginForm
from .forms import LegalArticleForm
from django.contrib import messages



@login_required(login_url='/admin-login/') 
def base_view(request):
    return render(request, 'adminpanel/admin_base.html')

def admin_dashboard(request):
    total_lawyers = Lawyer.objects.count()
    total_clients = Client.objects.count()
    total_consultations = Consultation.objects.count()

    context = {
        'total_lawyers': total_lawyers,
        'total_clients': total_clients,
        'total_consultations': total_consultations,
    }
    return render(request, 'adminpanel/dashboard.html', context)


def manage_lawyers(request):
    lawyers = Lawyer.objects.all()

    context = {
        'lawyers': lawyers
    }
    return render(request, 'adminpanel/manage_lawyers.html', context)


#virify lawyer view
def verify_lawyer(request, lawyer_id):
    lawyer = get_object_or_404(Lawyer, id=lawyer_id)
    lawyer.is_verified = True
    lawyer.save()
    messages.success(request, f"Lawyer {lawyer.first_name} {lawyer.last_name} has been verified successfully!")  # ✅ success message
    return redirect('manage_lawyers')


#delete lawyer view
def delete_lawyer(request, lawyer_id):
    lawyer = get_object_or_404(Lawyer, id=lawyer_id)
    lawyer.delete()
    messages.success(request, f"Lawyer {lawyer.first_name} {lawyer.last_name} has been deleted successfully!")
    return redirect('manage_lawyers')


#view lawyer

def view_lawyer_profile(request, lawyer_id):
    try:
        profile = LawyerProfile.objects.get(lawyer_id=lawyer_id)
    except LawyerProfile.DoesNotExist:
        return render(request, 'adminpanel/no_profile_found.html')
    
    return render(request, 'adminpanel/view_lawyer_profile.html', {'profile': profile})

def admin_logout(request):
    logout(request)
    return redirect('home')  # Redirect to home page after logout


#view to list the client in admin dashboard
def admin_clients_view(request):
    clients = Client.objects.all()
    return render(request, 'adminpanel/client.html', {'clients': clients})


#view to view client detais
def admin_view_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    return render(request, 'adminpanel/client_detail.html', {'client': client})


#view to delete
def admin_delete_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    client.delete()
    return redirect('admin_clients')



#view for admin login

def admin_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                admin_user = AdminUser.objects.get(username=username)
                if check_password(password, admin_user.password):
                    request.session['admin_id'] = admin_user.id
                    return redirect('admin_dashboard')  # replace with your dashboard URL name
                else:
                    messages.error(request, 'Invalid credentials')
            except AdminUser.DoesNotExist:
                messages.error(request, 'Admin user not found')
    else:
        form = AdminLoginForm()

    return render(request, 'adminpanel/admin_login.html', {'form': form})



def admin_add_article(request):
    if request.method == 'POST':
        form = LegalArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Article added successfully!")
            return redirect('admin_dashboard')
    else:
        form = LegalArticleForm()
    return render(request, 'adminpanel/add_article.html', {'form': form})


def manage_articles(request):
    if request.method == 'POST':
        article_id = request.POST.get('article_id')
        if article_id:
            # Update existing article
            article = get_object_or_404(LegalArticle, id=article_id)
            form = LegalArticleForm(request.POST, request.FILES, instance=article)
            if form.is_valid():
                form.save()
                messages.success(request, "Article updated successfully!")
        else:
            # Add new article
            form = LegalArticleForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Article added successfully!")
        return redirect('manage_articles')
    
    articles = LegalArticle.objects.all()
    form = LegalArticleForm()
    return render(request, 'adminpanel/manage_articles.html', {'form': form, 'articles': articles})

def delete_article(request, id):
    article = get_object_or_404(LegalArticle, id=id)
    article.delete()
    messages.success(request, "Article deleted successfully!")
    return redirect('manage_articles')

# Edit Article View
def edit_article(request, id):
    article = get_object_or_404(LegalArticle, id=id)
    if request.method == 'POST':
        form = LegalArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, "Article updated successfully!")
            return redirect('manage_articles')
    else:
        form = LegalArticleForm(instance=article)
    return render(request, 'manage_articles.html', {'form': form})
