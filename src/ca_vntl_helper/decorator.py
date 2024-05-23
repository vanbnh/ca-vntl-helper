import traceback
import sys
import inspect
import linecache
import logging

def create_message_detail(error_detail, params, limit_param_char=32,root_cause=None):
    text_code = linecache.getline(error_detail.filename, error_detail.lineno)
    text_code = text_code.replace("\n", "")
    if root_cause:
        root_cause = f"\t-->ROOT CAUSE: {root_cause} \n"
    else:
        root_cause = ""
    # check file contain site-packages or pyt
    if "site-packages" in error_detail.filename:
        note_message = "site-packages"
    else:
        note_message = "your code"

    # except self, and crop value too long
    params = {key: value if len(str(value)) < limit_param_char else str(value)[:limit_param_char] + "..." for key, value in params.items() if key != "self"}
    message = f"===================================================\n" \
              f"Filename: {error_detail.filename},\n" \
              f"Function name: {error_detail.name}, params: {params}\n" \
              f"\t-----\n" \
              f"\tLine: {error_detail.lineno}, {text_code}\n {root_cause}" \
              f"\t-----\n" \
              f"\tNote: This error is from {note_message}\n"
    return message


def error_tracking_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if sys.version_info >= (3, 10):
                _, exc, _ = sys.exc_info()
            else:
                exc = sys.exception()

            errors_detail = traceback.extract_tb(exc.__traceback__)
            formatted_lines = traceback.format_exc().splitlines()
            frames = inspect.trace()
            messages = f"Error in function {func.__name__} \n"
            for idx, (frame, error_detail) in enumerate(zip(frames, errors_detail)):
                if idx == 0:
                    continue
                argvalues = inspect.getargvalues(frame[0])
                params = argvalues.locals
                if idx == len(frames) - 1:
                    message = create_message_detail(error_detail, params, limit_param_char=32, root_cause=formatted_lines[-1])
                else:
                    message = create_message_detail(error_detail, params, limit_param_char=32, root_cause=None)
                messages += message
            logging.error(messages)
            # raise e
    return wrapper

class ErrorTrackerWithCallBacks:
    def __init__(self, callback_functions=None, is_raise_error=False, limit_param_char=32):
        self.callback_functions = callback_functions
        self.is_raise_error = is_raise_error
        self.limit_param_char = limit_param_char
    def error_tracking_decorator(self, func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # if python version >= 3.10, use sys.exc_info() instead of sys.exception()

                if sys.version_info >= (3, 10):
                    _, exc, _ = sys.exc_info()
                else:
                    exc = sys.exception()
                errors_detail = traceback.extract_tb(exc.__traceback__)
                formatted_lines = traceback.format_exc().splitlines()
                frames = inspect.trace()
                messages = f"Error in function {func.__name__} \n"
                for idx, (frame, error_detail) in enumerate(zip(frames, errors_detail)):
                    if idx == 0:
                        continue
                    argvalues = inspect.getargvalues(frame[0])
                    params = argvalues.locals
                    if idx == len(frames) - 1:
                        message = create_message_detail(error_detail, params, self.limit_param_char, formatted_lines[-1])
                    else:
                        message = create_message_detail(error_detail, params, self.limit_param_char, root_cause=None)
                    messages += message
                if self.callback_functions:
                    for callback_function in self.callback_functions:
                        callback_function(messages)
                else:
                    logging.error(messages)
                if self.is_raise_error:
                    raise e

        return wrapper

