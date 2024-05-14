from ca_vntl_helper import error_tracking_decorator

@error_tracking_decorator
def test_function_1():
    a = 1
    b = 0
    c = a / b
    return f"Test function 1, c"

if __name__ == "__main__":
    test_function_1()