from django.shortcuts import render,HttpResponse

from .models import Employee,Role,Department
from datetime import datetime
from django.db.models import Q  # Import Q for complex queries

# Create your views here.
def index(request):
    return render(request,'index.html')

def view_employee(request):
    emp=Employee.objects.all() # Fetch all Employee records
    context={
        'emp':emp,
    }
    print(context) #to print context in terminal
    return render(request,'view_employee.html',context) #to route context with html file

def add_employee(request):
    if(request.method=='POST'): 
        first_name=request.POST['first_name'] #request.POST is used to get the data from the form
        #request.POST is a dictionary-like object that contains all the data submitted in the form
        last_name=request.POST['last_name']
        department=int(request.POST['department'])
        role=int(request.POST['role'])
        phone=int(request.POST['phone']) #phone is an integer field, so we need to convert it to int
        salary=int(request.POST['salary'])
        bonus=int(request.POST['bonus'])
        date=request.POST['date']  #writing all these on the basis of name of the input fields in the form

        
        #to save details of new employee in database
        new_employee=Employee(first_name=first_name,last_name=last_name,dept_id=department,role_id=role,phone=phone,salary=salary,bonus=bonus,hiring_date=datetime.now())
        new_employee.save()

       # return HttpResponse("Employee added successfully") #to show success message after adding employee
        return render(request, 'add_employee.html', {'success': True})

    elif request.method == 'GET':
        return render(request, 'add_employee.html')
    else:
        return HttpResponse("Invalid request method")


def filter_employee(request):
    if request.method == 'POST':
        # Get user input from form
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        dept = request.POST.get('dept', '')
        role = request.POST.get('role', '')
        hiring_date = request.POST.get('hiring_date', '')

        # Start with all employees
        emp = Employee.objects.all()

        # Filter employees based on the provided criteria
        if first_name:
            emp = emp.filter(first_name__icontains=first_name)

        if last_name:
            emp = emp.filter(last_name__icontains=last_name)

        if dept:
            emp = emp.filter(Q(dept__name__icontains=dept))

        if role:
            emp = emp.filter(Q(role__name__icontains=role))

        if hiring_date:
            emp = emp.filter(hiring_date__icontains=hiring_date)

        context = {
            'emp': emp,
            'success': True  # add success flag here
        }

        # Return filtered employees to the same template
        return render(request, 'view_employee.html', context)

    elif request.method == 'GET':
        
        return render(request, 'filter_employee.html')

    else:
        return HttpResponse("Invalid request method")


def delete_employee(request, emp_id=0):
    if emp_id:
        try:
            emp_to_delete = Employee.objects.get(id=emp_id)
            emp_to_delete.delete()

            emps = Employee.objects.all()
            context = {
                'emps': emps,
                'success': True  # add success flag here
            }
            return render(request, 'delete_employee.html', context)

        except Employee.DoesNotExist:
            return HttpResponse("Employee not found")

    # If no emp_id is provided, just show the list
    emps = Employee.objects.all()
    return render(request, 'delete_employee.html', {'emps': emps})



