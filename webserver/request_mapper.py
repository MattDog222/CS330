ERROR_KEY = "error"


class PageNotFoundException(Exception):
    pass


class RequestMapper:
    def __init__(self):
        self._uri_map = {}
        self._init()

    def _init(self):
        self._uri_map[ERROR_KEY] = 'html/error.mttml'
        self._uri_map[''] = 'html/index.html'
        self._uri_map['/'] = 'html/index.html'
        self._uri_map['home'] = 'html/index.html'
        self._uri_map['index'] = 'html/index.html'
        self._uri_map['index.html'] = 'html/index.html'
        self._uri_map['matts_grade'] = 'html/bonus.html'
        self._uri_map['hello'] = 'html/hello.mttml'

    def get_page(self, path):
        if path.endswith(".css") or path.endswith(".js"):
            return open(path).read()
        try:
            if '?' in path:
                pure_path, query = path.split('?')
                if self.is_template(pure_path):
                    args = {}
                    for arg in query.split('&'):
                        name, value = arg.split('=')
                        args[name] = value
                    return self.render_template(pure_path, args)
                return open(self._uri_map.get(pure_path)).read()
            return open(self._uri_map.get(path)).read()
        except Exception:
            raise PageNotFoundException

    def get_error_page(self, error_code):
        return self.render_template(ERROR_KEY, {'error_code': f'{error_code}'})

    def is_template(self, path):
        return self._uri_map[path].endswith(".mttml")

    def render_template(self, path, args_map):
        template = open(self._uri_map.get(path)).read()
        for name, value in args_map.items():
            symbol = '@__{' + name + '}__'
            template = template.replace(symbol, value)
        return template



