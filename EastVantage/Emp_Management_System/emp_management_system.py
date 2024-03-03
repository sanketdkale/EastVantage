import json


class Employee(object):
    def __init__(self, name, emp_id, title, department):
        self.name = name
        self.emp_id = emp_id
        self.title = title
        self.department = department

    def display_details(self):
        print(f"Name: {self.name}")
        print(f"ID: {self.emp_id}")
        print(f"Title: {self.title}")
        print(f"Department: {self.department}")

    def __str__(self):
        return f"{self.name} - {self.emp_id}"


class Department(object):
    def __init__(self, name):
        self.name = name
        self.employees = []

    def add_employee(self, employee):
        self.employees.append(employee)

    def remove_employee(self, emp_id):
        for employee in self.employees:
            if employee.emp_id == emp_id:
                self.employees.remove(employee)
                return
        print("Employee not found in this department.")

    def list_employees(self):
        if self.employees:
            print(f"Employees in {self.name} department:")
            for employee in self.employees:
                print(employee)
        else:
            print("No employees in this department.")


class Company(object):
    def __init__(self):
        self.departments = {}

    def add_department(self, department_name):
        if department_name not in self.departments:
            self.departments[department_name] = Department(department_name)
        else:
            print("Department already exists.")

    def remove_department(self, department_name):
        if department_name in self.departments:
            del self.departments[department_name]
        else:
            print("Department not found.")

    def display_departments(self):
        print("Departments:")
        for department in self.departments.values():
            print(department.name)


def save_data(company):
    with open('company_data.json', 'w') as file:
        data = {
            "departments": {dept.name: [str(emp) for emp in dept.employees] for dept in company.departments.values()}
        }
        json.dump(data, file)


def load_data():
    try:
        with open('company_data.json', 'r') as file:
            data = json.load(file)
            company = Company()
            for dept_name, emp_list in data['departments'].items():
                department = Department(dept_name)
                for emp_str in emp_list:
                    emp_data = emp_str.split(' - ')
                    employee = Employee(emp_data[0], emp_data[1], "", dept_name)
                    department.add_employee(employee)
                company.departments[dept_name] = department
            return company
    except FileNotFoundError:
        return None


def menu():
    print("\nEmployee Management System Menu:")
    print("1. Add Department")
    print("2. Remove Department")
    print("3. Add Employee")
    print("4. Remove Employee")
    print("5. List Employees in a Department")
    print("6. List Departments")
    print("7. Exit")


def main():
    company = load_data()
    if company is None:
        company = Company()

    while True:
        menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            department_name = input("Enter department name: ")
            company.add_department(department_name)
            save_data(company)
        elif choice == '2':
            department_name = input("Enter department name: ")
            company.remove_department(department_name)
            save_data(company)
        elif choice == '3':
            department_name = input("Enter department name: ")
            if department_name in company.departments:
                name = input("Enter employee name: ")
                emp_id = input("Enter employee ID: ")
                title = input("Enter employee title: ")
                employee = Employee(name, emp_id, title, department_name)
                company.departments[department_name].add_employee(employee)
                save_data(company)
            else:
                print("Department not found.")
        elif choice == '4':
            department_name = input("Enter department name: ")
            if department_name in company.departments:
                emp_id = input("Enter employee ID: ")
                company.departments[department_name].remove_employee(emp_id)
                save_data(company)
            else:
                print("Department not found.")
        elif choice == '5':
            department_name = input("Enter department name: ")
            if department_name in company.departments:
                company.departments[department_name].list_employees()
            else:
                print("Department not found.")
        elif choice == '6':
            company.display_departments()
        elif choice == '7':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
