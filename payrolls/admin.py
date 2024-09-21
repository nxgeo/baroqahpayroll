from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import redirect
from pandas import DataFrame, ExcelWriter

from payrolls.models import Position, Employee, SalaryReport, Salary


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = [
        "position_id",
        "name",
        "formatted_base_salary",
        "formatted_bonus_percentage",
    ]
    list_display_links = ["name"]
    ordering = ["-base_salary"]
    search_fields = ["name"]


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = [
        "employee_id",
        "name",
        "position",
        "start_date",
        "formatted_base_salary",
    ]
    list_display_links = ["name"]
    list_filter = ["position"]
    ordering = ["name"]
    search_fields = ["name", "position__name"]


@admin.register(SalaryReport)
class SalaryReportAdmin(admin.ModelAdmin):
    list_display = [
        "report_id",
        "report_month",
        "report_year",
        "created_at",
        "updated_at",
    ]
    list_filter = ["report_month", "report_year"]
    ordering = ["report_month", "report_year"]

    actions = ["export_salary_reports_to_excel"]

    @admin.action(description="Export selected salary reports to Excel")
    def export_salary_reports_to_excel(self, request, queryset):
        filename = "SalaryReports.xlsx"

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = f"attachment; filename={filename}"

        writer = ExcelWriter(response, engine="xlsxwriter")

        workbook = writer.book
        title_format = workbook.add_format(
            {"font_size": 14, "bold": True, "align": "center"}
        )
        header_format = workbook.add_format(
            {"bold": True, "valign": "vcenter", "bg_color": "#D7E4BC", "border": 1}
        )

        for salary_report in queryset:
            salaries = Salary.objects.select_related("employee__position").filter(
                salary_report=salary_report
            )

            data = [
                {
                    "NIP": salary.employee_id,
                    "Nama": salary.employee.name,
                    "Jabatan": salary.employee.position.name,
                    "Gaji Pokok": salary.formatted_base_salary,
                    "Bonus (%)": salary.formatted_bonus_percentage,
                    "Jumlah Bonus": salary.formatted_bonus_amount,
                    "PPh (%)": salary.formatted_tax_percentage,
                    "Jumlah PPh": salary.formatted_tax_amount,
                    "Gaji Bersih": salary.formatted_net_salary,
                }
                for salary in salaries
            ]

            sheet_name = (
                f"{salary_report.report_month_name} {salary_report.report_year}"
            )
            sheet_name = sheet_name[:31]

            df = DataFrame(data)
            df.to_excel(writer, sheet_name, header=False, index=False, startrow=3)

            worksheet = writer.sheets[sheet_name]

            for col_num, value in enumerate(df.columns.values):
                worksheet.write(2, col_num, value, header_format)

            worksheet.merge_range(
                "A1:I1",
                f"Laporan Gaji Bulanan - {salary_report.report_month_name} {salary_report.report_year}",
                title_format,
            )

        writer.close()

        return response


@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    autocomplete_fields = ["employee"]
    list_display = [
        "salary_id",
        "employee",
        "formatted_base_salary",
        "formatted_bonus_percentage",
        "formatted_bonus_amount",
        "formatted_tax_percentage",
        "formatted_tax_amount",
        "formatted_net_salary",
        "salary_month",
        "salary_year",
        "created_at",
        "updated_at",
    ]
    list_display_links = ["employee"]
    list_filter = ["salary_month", "salary_year"]
    ordering = ["employee__name", "salary_month", "salary_year"]
    search_fields = ["employee__name"]

    def has_add_permission(self, request):
        return False

    actions = ["generate_payslip"]

    @admin.action(description="Generate e-PaySlip for selected employee salary")
    def generate_payslip(self, request, queryset):
        if queryset.count() != 1:
            return False
        salary = queryset.get()
        return redirect("payslip", salary_id=salary.pk)
