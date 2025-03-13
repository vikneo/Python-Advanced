import re
import json
import time


class Fresh:

    def __init__(self) -> None:
        self.routes = {}

    def route(self, rule: str, **options):
        def decorator(f):
            count = re.search(r'(<)', rule)
            endpoint = rule[:count.start()] if count is not None else rule
            self.routes[endpoint] = f
            return f

        return decorator

    @staticmethod
    def __check_args_in_path(path: str) -> tuple[bool, str]:
        args = path.split('/')
        return (True, '/'.join(args[2:])) if len(args) > 2 else (False, None)

    def __call__(self, environ, start_response):
        path = environ.get("REQUEST_URI")
        access_to_arg, args = self.__check_args_in_path(path = path)
        cleaned_path = path.replace(args, '') if args else path
        if path == '/long_task':
            time.sleep(80)
            html = ["<!DOCTYPE html>", "<html>", "<body>", '<div style="display: flex; justify-content: center;">'
                                                           '<img src="static/img/504.png" alr="TIME OUT">',
                    "</div>", "</body>", "</html>"]
            start_response("504 TIME OUT", [('Content-Type', 'text/html')])
            return [line.encode("utf-8") for line in html]
        try:
            resp = self.routes[cleaned_path](args) if access_to_arg else self.routes[cleaned_path]()
            start_response("200 OK", [('Content-Type', 'application/json')])
            response = [json.dumps(resp).encode('utf-8')]
        except Exception:
            html = ["<!DOCTYPE html>", "<html>", "<body>", '<div style="display: flex; justify-content: center;">'
                                                           '<img src="static/img/404.webp" alr="Page not found">',
                    "</div>", "</body>", "</html>"]
            start_response("404 NOT FOUND", [('Content-Type', 'text/html')])
            response = [line.encode("utf-8") for line in html]

        return response