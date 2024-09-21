from django.db.models.signals import post_save
from django.dispatch import receiver

from payrolls.constants import INCOME_TAX_PERCENTAGE
from payrolls.models import Employee, SalaryReport, Salary


@receiver(post_save, sender=SalaryReport)
def create_salaries_for_report(sender, instance, created, **kwargs):
    if created:
        employees = Employee.objects.select_related("position")
        salaries = []
        for employee in employees:
            base_salary = employee.position.base_salary
            bonus_percentage = employee.position.bonus_percentage
            bonus_amount = base_salary * (bonus_percentage / 100)
            tax_amount = (base_salary + bonus_amount) * (INCOME_TAX_PERCENTAGE / 100)
            net_salary = base_salary + bonus_amount - tax_amount
            salaries.append(
                Salary(
                    employee=employee,
                    salary_report=instance,
                    base_salary=base_salary,
                    bonus_percentage=bonus_percentage,
                    bonus_amount=bonus_amount,
                    tax_percentage=INCOME_TAX_PERCENTAGE,
                    tax_amount=tax_amount,
                    net_salary=net_salary,
                    salary_month=instance.report_month,
                    salary_year=instance.report_year,
                )
            )

        Salary.objects.bulk_create(salaries)
