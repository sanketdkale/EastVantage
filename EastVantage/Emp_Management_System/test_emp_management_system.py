from Emp_Management_System.emp_management_system import Company, Employee


class TestEmployeeManagementSystem:
    @staticmethod
    def test_add_department():
        company = Company()
        company.add_department("HR")
        company.add_department("IT")

        assert "HR" in company.departments
        assert "IT" in company.departments
        company.add_department("Finance")
        assert "Finance" in company.departments

    @staticmethod
    def test_remove_department():
        company = Company()
        company.add_department("HR")
        company.add_department("IT")

        assert company.remove_department("HR") is None
        assert "HR" not in company.departments

        assert company.remove_department("Finance") is None

    @staticmethod
    def test_add_employee():
        company = Company()
        company.add_department("HR")
        company.add_department("IT")

        emp1 = Employee("John Doe", "123", "HR Manager", "HR")
        emp2 = Employee("Jane Smith", "456", "Software Engineer", "IT")

        company.departments["HR"].add_employee(emp1)
        assert len(company.departments["HR"].employees) == 1
        assert emp1 in company.departments["HR"].employees

        company.departments["IT"].add_employee(emp2)
        assert len(company.departments["IT"].employees) == 1
        assert emp2 in company.departments["IT"].employees

    @staticmethod
    def test_remove_employee():
        company = Company()
        company.add_department("HR")
        company.add_department("IT")

        emp1 = Employee("John Doe", "123", "HR Manager", "HR")
        emp2 = Employee("Jane Smith", "456", "Software Engineer", "IT")

        company.departments["HR"].add_employee(emp1)
        company.departments["IT"].add_employee(emp2)

        company.departments["HR"].remove_employee("123")
        assert len(company.departments["HR"].employees) == 0
        assert emp1 not in company.departments["HR"].employees

        company.departments["IT"].remove_employee("456")
        assert len(company.departments["IT"].employees) == 0
        assert emp2 not in company.departments["IT"].employees

