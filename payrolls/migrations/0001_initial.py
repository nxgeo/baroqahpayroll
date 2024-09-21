# Generated by Django 5.0.6 on 2024-06-13 16:19

import django.db.models.deletion
import payrolls.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Position",
            fields=[
                (
                    "position_id",
                    models.SmallAutoField(primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=20, unique=True)),
                ("base_salary", models.DecimalField(decimal_places=2, max_digits=11)),
                (
                    "bonus_percentage",
                    models.DecimalField(decimal_places=2, max_digits=5),
                ),
            ],
            options={
                "db_table": "position",
            },
        ),
        migrations.CreateModel(
            name="Employee",
            fields=[
                (
                    "employee_id",
                    models.SmallAutoField(primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=70)),
                ("address", models.TextField()),
                ("date_of_birth", models.DateField()),
                ("start_date", models.DateField()),
                (
                    "position",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="payrolls.position",
                    ),
                ),
            ],
            options={
                "db_table": "employee",
            },
        ),
        migrations.CreateModel(
            name="Salary",
            fields=[
                ("salary_id", models.AutoField(primary_key=True, serialize=False)),
                ("base_salary", models.DecimalField(decimal_places=2, max_digits=11)),
                (
                    "bonus_percentage",
                    models.DecimalField(decimal_places=2, max_digits=5),
                ),
                ("bonus_amount", models.DecimalField(decimal_places=2, max_digits=11)),
                ("tax_percentage", models.DecimalField(decimal_places=2, max_digits=5)),
                ("tax_amount", models.DecimalField(decimal_places=2, max_digits=11)),
                ("net_salary", models.DecimalField(decimal_places=2, max_digits=11)),
                (
                    "salary_month",
                    models.SmallIntegerField(choices=payrolls.models.get_month_choices),
                ),
                (
                    "salary_year",
                    models.SmallIntegerField(choices=payrolls.models.get_year_choices),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="payrolls.employee",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "salaries",
                "db_table": "salary",
            },
        ),
        migrations.CreateModel(
            name="SalaryReport",
            fields=[
                ("report_id", models.SmallAutoField(primary_key=True, serialize=False)),
                (
                    "report_month",
                    models.SmallIntegerField(choices=payrolls.models.get_month_choices),
                ),
                (
                    "report_year",
                    models.SmallIntegerField(choices=payrolls.models.get_year_choices),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "employees",
                    models.ManyToManyField(
                        through="payrolls.Salary", to="payrolls.employee"
                    ),
                ),
            ],
            options={
                "db_table": "salary_report",
            },
        ),
        migrations.AddField(
            model_name="salary",
            name="salary_report",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="payrolls.salaryreport"
            ),
        ),
        migrations.AddConstraint(
            model_name="salaryreport",
            constraint=models.UniqueConstraint(
                fields=("report_month", "report_year"),
                name="unique_report_per_month_year",
            ),
        ),
        migrations.AddConstraint(
            model_name="salary",
            constraint=models.UniqueConstraint(
                fields=("employee", "salary_month", "salary_year"),
                name="unique_salary_per_month_year",
            ),
        ),
    ]
