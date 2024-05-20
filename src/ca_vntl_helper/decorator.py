import traceback
import sys
import inspect
import linecache
import logging

def create_message_detail(error_detail, params, root_cause=None):
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
                    message = create_message_detail(error_detail, params, formatted_lines[-1])
                else:
                    message = create_message_detail(error_detail, params)
                messages += message
            logging.error(messages)
            raise e
    return wrapper

class ErrorTrackerWithCallBacks:
    def __init__(self, callback_functions=None):
        self.callback_functions = callback_functions

    def error_tracking_decorator(self, func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                exc = sys.exception()
                # print(exc.__traceback__)
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
                        message = create_message_detail(error_detail, params, formatted_lines[-1])
                    else:
                        message = create_message_detail(error_detail, params)
                    messages += message
                if self.callback_functions:
                    for callback_function in self.callback_functions:
                        callback_function(messages)
                else:
                    logging.error(messages)
                raise e

        return wrapper

