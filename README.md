# Class Registration System by Anthony Robbins

The system I create is for a small local gym that offers group fitness classes such as 
yoga and zumba. The prototype will serve as a class registration system, designed to help 
both customers and staff manage class sign-ups more efficiently. Currently, Sunshine 
Fitness relies on in-person and phone-based registration, which often results in overbooked 
classes and customer frustration. The new system will allow users to register for classes
and cancel their registration through a simple gui. The application will collect input data
and store it in a JSON file, providing staff with an organized and up-to-date list of 
participants for each class.

## Demo Video
```
https://youtu.be/U-wOqDPxjfY
```


## Install required libraries
Ensure that you are in the main directory and 
run the following:

_This must be done before you can run the application
if you are not using the included venv._


```shell
$ pip install PILLOW
$ pip install pytest
$ pip install tkinter
```

## To run the program
Click the green triangle run icon in the 
top-right corner of the PyCharm window.
or
```shell
$ python3 arobbi13_project.py
```

#### In the PIN prompt, use the following credentials
* PIN: ``4444``

## Functionality
### Create Registration
A new registration will be added to the registration class
instance list and the customers.json file when
users click on the Add button.

When printing out the registration class instance list,
it has the following information:

Customers information:
Name: Jane Doe, Email: jane@example.com,
Class: Spin, Time: 1:00 PM, Duration: 1.5hrs
Name: Mary Jane, Email: mary@example.com,
Class: Yoga, Time: 9:00 AM, Duration: 1.5hrs

### Delete a Registration
A registration will be deleted from the Registration class
instance list and from the registrations.json file 
when a Delete button is clicked.

### Edit Registration 
Staff can edit registration info and that will overwrite the previous info and be stored in the 
registration.json file when the edit button is clicked.

### Exit
The application will be closed when the Exit
button is clicked.

## Data files
### registrations.json
The file contains the registration data in the 
following format:

| Name      | Email               | Class | Time    | Duration | Fee |
|-----------|---------------------|-------|---------|----------|-----|
| Anthony   | anthony@example.com | Spin  | 1:00 PM | 1.5      | $10 |
| Mary Jane | mary@example.com    | Yoga  | 9:00 AM | 1.5      | $10 |


## Class

### Registration Class

#### Variables
Each Registration instance has the following instance
variables:
1. name: public, string data type
2. email: public, string data type
3. class_name: public, string data type
4. time: public, string data type
5. duration: public, float
6. fee: public, int 

#### Methods
The Registration class has the following methods:
* The dunder__init__(): 
* summary(): 
* to_dict(): 
* from_dict(): 
* def from_dict(): @classmethod 
* load_registrations():
* save_registrations():
* register_customer():
* cancel_registration:
* display_grouped():

## Auto Testing
Run the following command to test the 
test_registration.py file.  There are 3 test cases.

```shell
$ pytest -v test_registration.py
```

