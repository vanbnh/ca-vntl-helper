## CA VNTL Helper
This is a simple helper for the CA Techlab project. It is designed to help you track errors and do some actions when errors occur.
**It will help you to track, log, and alert when an error occurs in your code. It can show the parameters you passed, so you can easily simulate the error.**
### Installation
Install the package using pip:
```bash
pip install ca-vntl-helper
```
### Usage
#### The decorator function
Import the decorator function from the package and use it to decorate your function. The message will be through when an error occurs.
```python
from ca_vntl_helper import error_tracking_decorator

@error_tracking_decorator
def example_function():
    # Your code here
    pass
```
#### Example
Some nested functions and an error will be raised in the innermost function. The error message will be printed out.

**You just place the decorator on the top of the function you want to track.**
```python
from ca_vntl_helper import error_tracking_decorator

def divide(a, b):
    return a / b

def second_inner_function(second_inner_a, second_inner_b):
    return divide(second_inner_a, second_inner_b)
    
def first_inner_function(first_inner_a, first_inner_b):
    return second_inner_function(first_inner_a, first_inner_b)

@error_tracking_decorator # Just place the decorator here
def outer_function(outer_a, outer_b):
    return first_inner_function(outer_a, outer_b)

if __name__ == "__main__":
    # The process will get an error when dividing by 0
    outer_function(1, 0)
```
```text
ERROR:root:Error in function outer_function 
===================================================
Filename: /Users/abc/Documents/projects/packaging_helper/src/test.py,
Function name: outer_function, params: {'outer_a': 1, 'outer_b': 0}
	-----
	Line: 20,     return first_inner_function(outer_a, outer_b)
 	-----
===================================================
Filename: /Users/abc/Documents/projects/packaging_helper/src/test.py,
Function name: first_inner_function, params: {'first_inner_a': 1, 'first_inner_b': 0}
	-----
	Line: 15,     return second_inner_function(first_inner_a, first_inner_b)
 	-----
===================================================
Filename: /Users/abc/Documents/projects/packaging_helper/src/test.py,
Function name: second_inner_function, params: {'second_inner_a': 1, 'second_inner_b': 0}
	-----
	Line: 11,     return divide(second_inner_a, second_inner_b)
 	-----
===================================================
Filename: /Users/abc/Documents/projects/packaging_helper/src/test.py,
Function name: divide, params: {'a': 1, 'b': 0}
	-----
	Line: 7,     return a / b
 	-->ROOT CAUSE: ZeroDivisionError: division by zero 
	-----
```
As you can see, the error message is printed out with the function name, parameters, the filename, and the line number. The root cause of the error is also shown.

### The class with callback functions
In case you want **to do some actions like alert to Slack or save error logs to S3**, you can use the class with callback functions.  
```python
from ca_vntl_helper import ErrorTrackerWithCallBacks

# Define your callback functions, notice that those functions must have a parameter to receive the message
def send_message_to_slack(message):
    # Your code here
    print("Message sent to slack:")
    print(message)
    
def save_message_to_logfile_on_s3(message):
    # Your code here
    print("Message saved to logfile on S3:")
    print(message)

error_tracker = ErrorTrackerWithCallBacks(callback_functions=[send_message_to_slack, save_message_to_logfile_on_s3])
error_tracking_decorator_with_callbacks = error_tracker.error_tracking_decorator

def divide(a, b):
    return a / b

def second_inner_function(second_inner_a, second_inner_b):
    return divide(second_inner_a, second_inner_b)

def first_inner_function(first_inner_a, first_inner_b):
    return second_inner_function(first_inner_a, first_inner_b)

@error_tracking_decorator_with_callbacks  # Just place the decorator here
def outer_function(outer_a, outer_b):
    return first_inner_function(outer_a, outer_b)

if __name__ == "__main__":
    # The process will get an error when dividing by 0
    outer_function(1, 0)
```
```text
Message sent to slack:
Error in function outer_function 
===================================================
Filename: /Users/abc/Documents/projects/packaging_helper/src/test.py,
Function name: outer_function, params: {'outer_a': 1, 'outer_b': 0}
	-----
	Line: 28,     return first_inner_function(outer_a, outer_b)
 	-----
===================================================
Filename: /Users/abc/Documents/projects/packaging_helper/src/test.py,
Function name: first_inner_function, params: {'first_inner_a': 1, 'first_inner_b': 0}
	-----
	Line: 23,     return second_inner_function(first_inner_a, first_inner_b)
 	-----
===================================================
Filename: /Users/abc/Documents/projects/packaging_helper/src/test.py,
Function name: second_inner_function, params: {'second_inner_a': 1, 'second_inner_b': 0}
	-----
	Line: 19,     return divide(second_inner_a, second_inner_b)
 	-----
===================================================
Filename: /Users/abc/Documents/projects/packaging_helper/src/test.py,
Function name: divide, params: {'a': 1, 'b': 0}
	-----
	Line: 15,     return a / b
 	-->ROOT CAUSE: ZeroDivisionError: division by zero 
	-----

Message saved to logfile on S3:
Error in function outer_function 
===================================================
Filename: /Users/abc/Documents/projects/packaging_helper/src/test.py,
Function name: outer_function, params: {'outer_a': 1, 'outer_b': 0}
	-----
	Line: 28,     return first_inner_function(outer_a, outer_b)
 	-----
===================================================
Filename: /Users/abc/Documents/projects/packaging_helper/src/test.py,
Function name: first_inner_function, params: {'first_inner_a': 1, 'first_inner_b': 0}
	-----
	Line: 23,     return second_inner_function(first_inner_a, first_inner_b)
 	-----
===================================================
Filename: /Users/abc/Documents/projects/packaging_helper/src/test.py,
Function name: second_inner_function, params: {'second_inner_a': 1, 'second_inner_b': 0}
	-----
	Line: 19,     return divide(second_inner_a, second_inner_b)
 	-----
===================================================
Filename: /Users/abc/Documents/projects/packaging_helper/src/test.py,
Function name: divide, params: {'a': 1, 'b': 0}
	-----
	Line: 15,     return a / b
 	-->ROOT CAUSE: ZeroDivisionError: division by zero 
	-----

```