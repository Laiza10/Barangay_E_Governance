from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import staff_only
from .models import Complaint, DocumentRequest, Announcement, Notification
from .forms import RegisterForm, ComplaintForm, DocumentRequestForm, AnnouncementForm

# -------------------- ROOT --------------------
def home_redirect(request):
    """
    Redirect users from the root URL to the correct dashboard.
    """
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('staff_dashboard')
        else:
            return redirect('resident_dashboard')
    return redirect('login')


# -------------------- AUTH --------------------
def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Account registered successfully. Please log in.")
        return redirect('login')
    return render(request, 'auth/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            if user.is_superuser:
                return redirect('staff_dashboard')
            else:
                return redirect('resident_dashboard')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')
    return render(request, 'auth/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You have logged out successfully.")
    return redirect('login')


# -------------------- RESIDENT --------------------
@login_required
def resident_dashboard(request):
    complaints = Complaint.objects.filter(user=request.user)
    requests = DocumentRequest.objects.filter(user=request.user)
    return render(request, 'resident/dashboard.html', {
        'complaints': complaints,
        'requests': requests
    })

@login_required
def submit_complaint(request):
    form = ComplaintForm(request.POST or None)
    if form.is_valid():
        complaint = form.save(commit=False)
        complaint.user = request.user
        complaint.save()
        Notification.objects.create(
            user=request.user,
            message="Your complaint has been submitted."
        )
        messages.success(request, "Complaint submitted successfully.")
        return redirect('resident_dashboard')
    return render(request, 'resident/complaint.html', {'form': form})

@login_required
def request_document(request):
    form = DocumentRequestForm(request.POST or None)
    if form.is_valid():
        doc = form.save(commit=False)
        doc.user = request.user
        doc.save()
        Notification.objects.create(
            user=request.user,
            message=f"Your document request '{doc.document_type}' has been submitted."
        )
        messages.success(request, f"Document request '{doc.document_type}' submitted successfully.")
        return redirect('resident_dashboard')
    return render(request, 'resident/request_document.html', {'form': form})

@login_required
def view_announcements(request):
    announcements = Announcement.objects.all().order_by('-date_posted')
    return render(request, 'resident/announcements.html', {'announcements': announcements})


# -------------------- STAFF --------------------
@staff_only
def staff_dashboard(request):
    complaints = Complaint.objects.all().order_by('-created_at')
    requests = DocumentRequest.objects.all().order_by('-requested_at')
    return render(request, 'staff/dashboard.html', {
        'complaints': complaints,
        'requests': requests
    })

@staff_only
def respond_complaint(request, id):
    complaint = get_object_or_404(Complaint, id=id)
    if request.method == 'POST':
        complaint.response = request.POST.get('response')
        complaint.status = 'Responded'
        complaint.save()
        Notification.objects.create(
            user=complaint.user,
            message="Your complaint has been responded."
        )
        messages.success(request, f"Responded to complaint: {complaint.subject}")
        return redirect('staff_dashboard')
    return render(request, 'staff/respond_complaint.html', {'complaint': complaint})

@staff_only
def update_request_status(request, id, status):
    doc = get_object_or_404(DocumentRequest, id=id)
    doc.status = status
    doc.save()
    Notification.objects.create(
        user=doc.user,
        message=f"Your document request '{doc.document_type}' was {status}."
    )
    messages.success(request, f"Document request '{doc.document_type}' updated to {status}.")
    return redirect('staff_dashboard')

@staff_only
def add_announcement(request):
    form = AnnouncementForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Announcement posted successfully.")
        return redirect('staff_dashboard')
    return render(request, 'staff/add_announcement.html', {'form': form})
