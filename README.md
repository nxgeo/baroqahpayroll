# Employee Payroll Management System

Welcome to the Employee Payroll Management System. This project is a payroll management system built using Django's built-in admin interface for managing employee salaries.

## Tech Stack
- **Python**
- **Django**
- **PostgreSQL**

## Features

### Role-Based Access Control (RBAC)
Uses Django's built-in authentication system to manage user roles and permissions.

![RBAC Feature Screenshot](https://github.com/user-attachments/assets/11e4f164-eca5-4de0-8c6c-90ad12b68d57)

![RBAC Feature Screenshot](https://github.com/user-attachments/assets/c63ff7c1-c0b9-4c11-8d0f-7bacb9dec985)

### Manage Employee Positions
CRUD operations for handling employee positions.

![Manage Positions Screenshot](https://github.com/user-attachments/assets/2039243d-7c11-4ad0-9436-e604054e525c)

### Manage Employees
CRUD operations for managing employee records.

![Manage Employees Screenshot](https://github.com/user-attachments/assets/e9428b18-26a3-4392-8ed6-cfcd2ffd3249)

### Monthly Salary Calculation
Calculates employee salaries based on base salary, bonus percentage, and income tax percentage.

$bonusamount=basesalary\times\frac{bonuspercentage}{100}$

$taxamount=(basesalary+bonusamount)\times\frac{INCOMETAXPERCENTAGE}{100}$

$netsalary=basesalary+bonusamount-taxamount$

![Salary Calculation Screenshot](https://github.com/user-attachments/assets/4c6879b2-1d1b-45c2-a35f-1395cc785fb8)

### Generate Monthly Payslip
Generate a payslip for an individual employee for a specific month.

![Generate Payslip Screenshot](https://github.com/user-attachments/assets/7a97ea6b-abcd-499c-adcd-dc58b005cf3a)

### Generate Monthly Salary Reports
Generate and export monthly salary reports to Excel. Reports can cover one or multiple months.

![Generate Salary Reports Screenshot](https://github.com/user-attachments/assets/4c229ebd-b052-46ed-b24c-df4cef5d08ac)

![Salary Reports Screenshot](https://github.com/user-attachments/assets/88bc8001-9878-49ab-8a64-0e06bca0ec51)


