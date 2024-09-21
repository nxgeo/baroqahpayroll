from calendar import month_name

from django.contrib import admin
from django.contrib.humanize.templatetags.humanize import intcomma
from django.db import models
from django.utils import timezone

from payrolls.utils import normalize_or_quantize


class Position(models.Model):
    position_id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=20, unique=True)
    base_salary = models.DecimalField(max_digits=11, decimal_places=2)
    bonus_percentage = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = "position"

    def __str__(self):
        return self.name

    @property
    @admin.display(description="Base Salary")
    def formatted_base_salary(self):
        return f"Rp{intcomma(self.base_salary)}"

    @property
    @admin.display(description="Bonus (%)")
    def formatted_bonus_percentage(self):
        return f"{normalize_or_quantize(self.bonus_percentage)}%"


class Employee(models.Model):
    employee_id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=70)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    address = models.TextField()
    date_of_birth = models.DateField()
    start_date = models.DateField()

    class Meta:
        db_table = "employee"

    def __str__(self):
        return self.name

    @property
    @admin.display(description="Base Salary")
    def formatted_base_salary(self):
        return f"Rp{intcomma(self.position.base_salary)}"


def get_month_choices():
    return [(i, month_name[i]) for i in range(1, 13)]


def get_year_choices():
    current_year = timezone.now().year
    return [(current_year - i, current_year - i) for i in range(1, -1, -1)]


class SalaryReport(models.Model):
    report_id = models.SmallAutoField(primary_key=True)
    report_month = models.SmallIntegerField(choices=get_month_choices)
    report_year = models.SmallIntegerField(choices=get_year_choices)
    employees = models.ManyToManyField(Employee, through="Salary")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "salary_report"
        constraints = [
            models.UniqueConstraint(
                fields=["report_month", "report_year"],
                name="unique_report_per_month_year",
            )
        ]

    @property
    def report_month_name(self):
        return month_name[self.report_month]


class Salary(models.Model):
    salary_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    salary_report = models.ForeignKey(SalaryReport, on_delete=models.CASCADE)
    base_salary = models.DecimalField(max_digits=11, decimal_places=2)
    bonus_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    bonus_amount = models.DecimalField(max_digits=11, decimal_places=2)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=11, decimal_places=2)
    net_salary = models.DecimalField(max_digits=11, decimal_places=2)
    salary_month = models.SmallIntegerField(choices=get_month_choices)
    salary_year = models.SmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "salary"
        verbose_name_plural = "salaries"
        constraints = [
            models.UniqueConstraint(
                fields=["employee", "salary_month", "salary_year"],
                name="unique_salary_per_month_year",
            )
        ]

    @property
    @admin.display(description="Base Salary")
    def formatted_base_salary(self):
        return f"Rp{intcomma(self.base_salary)}"

    @property
    @admin.display(description="Bonus (%)")
    def formatted_bonus_percentage(self):
        return f"{normalize_or_quantize(self.bonus_percentage)}%"

    @property
    @admin.display(description="Bonus Amount")
    def formatted_bonus_amount(self):
        return f"Rp{intcomma(self.bonus_amount)}"

    @property
    @admin.display(description="Tax (%)")
    def formatted_tax_percentage(self):
        return f"{normalize_or_quantize(self.tax_percentage)}%"

    @property
    @admin.display(description="Tax Amount")
    def formatted_tax_amount(self):
        return f"Rp{intcomma(self.tax_amount)}"

    @property
    @admin.display(description="Net Salary")
    def formatted_net_salary(self):
        return f"Rp{intcomma(self.net_salary)}"

    @property
    def salary_month_name(self):
        return month_name[self.salary_month]
