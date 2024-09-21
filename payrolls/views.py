from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET

from payrolls.models import Salary


@login_required
@require_GET
def payslip_view(request, salary_id):
    salary = get_object_or_404(
        Salary.objects.select_related("employee__position"), pk=salary_id
    )
    return render(request, "payrolls/payslip.html", {"salary": salary})
