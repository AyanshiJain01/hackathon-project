# jobs/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import JobPost, JobApplication
from .forms import JobPostForm, JobApplicationForm, CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def home(request):
    jobs = JobPost.objects.filter(is_active=True).order_by('-created_at')
    job_types = JobPost.JOB_TYPES
    
    job_type = request.GET.get('job_type')
    location = request.GET.get('location')
    search = request.GET.get('search')

    if job_type:
        jobs = jobs.filter(job_type=job_type)
    if location:
        jobs = jobs.filter(location__icontains=location)
    if search:
        jobs = jobs.filter(title__icontains=search) | jobs.filter(description__icontains=search)

    context = {
        'jobs': jobs,
        'job_types': job_types,
    }
    return render(request, 'jobs/home.html', context)

@login_required
def post_job(request):
    if request.user.user_type != 'employer':
        messages.error(request, 'Only employers can post jobs.')
        return redirect('home')

    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('job_detail', job.id)
    else:
        form = JobPostForm()
    
    return render(request, 'jobs/post_job.html', {'form': form})

@login_required
def job_detail(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    is_applied = False
    
    if request.user.is_authenticated and request.user.user_type == 'jobseeker':
        is_applied = JobApplication.objects.filter(job=job, applicant=request.user).exists()
    
    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'is_applied': is_applied
    })

@login_required
def apply_job(request, job_id):
    if request.user.user_type != 'jobseeker':
        messages.error(request, 'Only job seekers can apply for jobs.')
        return redirect('home')

    job = get_object_or_404(JobPost, id=job_id)
    
    # Check if user has already applied
    if JobApplication.objects.filter(job=job, applicant=request.user).exists():
        messages.info(request, 'You have already applied for this job.')
        return redirect('job_detail', job_id=job_id)

    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            messages.success(request, 'Application submitted successfully!')
            return redirect('job_detail', job_id=job_id)
    else:
        form = JobApplicationForm()
    
    return render(request, 'jobs/apply_job.html', {
        'form': form,
        'job': job
    })

@login_required
def profile(request):
    return render(request, 'jobs/profile.html', {
        'user': request.user
    })

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    return render(request, 'jobs/edit_profile.html', {'form': form})

@login_required
def my_applications(request):
    if request.user.user_type != 'jobseeker':
        messages.error(request, 'Only job seekers can view applications.')
        return redirect('home')
        
    applications = JobApplication.objects.filter(applicant=request.user).order_by('-applied_at')
    return render(request, 'jobs/my_applications.html', {'applications': applications})

@login_required
def my_jobs(request):
    if request.user.user_type != 'employer':
        messages.error(request, 'Only employers can access this page.')
        return redirect('home')
        
    jobs = JobPost.objects.filter(employer=request.user).order_by('-created_at')
    return render(request, 'jobs/my_jobs.html', {'jobs': jobs})


@login_required
def manage_job_applications(request, job_id):
    if request.user.user_type != 'employer':
        messages.error(request, 'Only employers can manage job applications.')
        return redirect('home')
    
    job = get_object_or_404(JobPost, id=job_id, employer=request.user)
    applications = JobApplication.objects.filter(job=job).order_by('-applied_at')
    
    if request.method == 'POST':
        application_id = request.POST.get('application_id')
        status = request.POST.get('status')
        
        try:
            application = JobApplication.objects.get(id=application_id, job=job)
            application.status = status
            application.save()
            messages.success(request, f'Application {status} successfully.')
            return redirect('manage_job_applications', job_id=job_id)
        except JobApplication.DoesNotExist:
            messages.error(request, 'Invalid application.')
    
    return render(request, 'jobs/manage_job_applications.html', {
        'job': job,
        'applications': applications
    })


def explore_schemes(request):
    # You can add any additional context data if needed
    return render(request, 'jobs/explore_schemes.html')