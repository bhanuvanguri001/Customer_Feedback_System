from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail

from .models import Company, Feedback
from .forms import CompanyForm, FeedbackForm
from .fusioncharts import FusionCharts


# =====================================
# HOME PAGE – ROLE BASED DASHBOARD
# =====================================
@login_required
def home(request):
    user = request.user
    companies = Company.objects.all()

    if user.is_superuser:
        return render(request, 'feedback/admin_index.html', {
            'companies': companies
        })

    elif user.is_staff:
        return render(request, 'feedback/manager_index.html', {
            'companies': companies
        })

    else:
        return render(request, 'feedback/customer_index.html', {
            'companies': companies
        })


# =====================================
# COMPANY DETAIL PAGE
# =====================================
@login_required
def detail(request, company_id):
    company = get_object_or_404(Company, pk=company_id)
    company_list = Company.objects.all()

    return render(request, 'feedback/detail.html', {
        'company': company,
        'company_list': company_list,
    })


# =====================================
# ADD FEEDBACK (CUSTOMER ONLY)
# =====================================
@login_required
def add_feedback(request, company_id):
    # ❌ Staff & Admin cannot submit feedback
    if request.user.is_staff or request.user.is_superuser:
        return redirect('home')

    company = get_object_or_404(Company, pk=company_id)

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.company = company
            feedback.user = request.user
            feedback.save()

            # Optional Email Notification
            if hasattr(company, 'employee') and company.employee and company.employee.email:
                send_mail(
                    subject='New Feedback Received',
                    message=f'New feedback received for {company.name}',
                    from_email='admin@example.com',
                    recipient_list=[company.employee.email],
                    fail_silently=True,
                )

            return redirect('detail', company_id=company.id)
    else:
        form = FeedbackForm()

    return render(request, 'feedback/add_feedback.html', {
        'form': form,
        'company': company
    })


# =====================================
# FUSION CHART (ADMIN / MANAGER ONLY)
# =====================================
@login_required
def fusion_chart(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('home')

    chart_data = []

    for company in Company.objects.all():
        chart_data.append({
            "label": company.name,
            "value": Feedback.objects.filter(company=company).count()
        })

    data_source = {
        "chart": {
            "caption": "Company Feedback Analysis",
            "theme": "fusion"
        },
        "data": chart_data
    }

    pie_chart = FusionCharts(
        "pie2d",
        "feedback_chart",
        "600",
        "400",
        "chart-container",
        "json",
        data_source
    )

    return render(request, 'feedback/fusion_chart.html', {
        'chart': pie_chart.render()
    })
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import FeedbackForm

@login_required
def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            return redirect('/')
    else:
        form = FeedbackForm()

    return render(request, 'feedback/submit_feedback.html', {'form': form})
