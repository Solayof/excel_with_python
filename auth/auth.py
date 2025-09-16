

class Auth:
    def require_auth(self, path, excluded_paths):
        pass
    
    def authentication_header(self, request=None):
        pass
    def current_user(self, request=None):
        return None
    
    def session_cookie(self, request=None):
        pass
