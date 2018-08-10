import os
from enum import Enum
from mycloud.logger import log
from mycloud.mycloudapi.auth.bearer_token import get_bearer_token
from mycloud.constants import USE_TOKEN_CACHE, TOKEN_CACHE_FOLDER, CACHED_TOKEN_IDENTIFIER


class AuthMode(Enum):
    Password = 0
    Token = 1


class MyCloudAuthenticator:

    def __init__(self):
        self.current_token = None
        self.auth_mode = None
        self.user_name = None
        self.password = None
        self.tried_cached_token = False
        self.token_refresh_required = True
        self.bearer_token = None

    def set_password_auth(self, user_name: str, password: str):
        self.auth_mode = AuthMode.Password
        self.user_name = user_name
        self.password = password
        self.token_refresh_required = True
        self.tried_cached_token = False

    def set_bearer_auth(self, bearer_token):
        self.auth_mode = AuthMode.Token
        if bearer_token == CACHED_TOKEN_IDENTIFIER:
            success = self._load_cached_token()
            if success:
                self.bearer_token = self.current_token
            else:
                raise ValueError('No cached token available')
        else:
            self.bearer_token = bearer_token

    def invalidate_token(self):
        self.token_refresh_required = True

    def get_token(self):
        if self.auth_mode == AuthMode.Token:
            return self.bearer_token
        elif self.auth_mode == AuthMode.Password:
            if self.user_name is None or self.password is None:
                raise ValueError('Username and password needs to be set')

            if self.current_token is None or self.token_refresh_required:
                if USE_TOKEN_CACHE and self._load_cached_token() and not self.tried_cached_token:
                    log('Trying to use cached token...')
                    self.tried_cached_token = True
                    self.token_refresh_required = False
                    return self.current_token

                self.current_token = get_bearer_token(
                    self.user_name, self.password)
                if USE_TOKEN_CACHE:
                    self.tried_cached_token = False
                    self._save_token()
                self.token_refresh_required = False
            return self.current_token

    def _load_cached_token(self):
        token_file = self._get_token_file_path()
        if os.path.isfile(token_file):
            self.current_token = open(token_file, 'r').read()
            return True
        return False

    def _save_token(self):
        if not os.path.isdir(TOKEN_CACHE_FOLDER):
            os.makedirs(TOKEN_CACHE_FOLDER)
        token_file = self._get_token_file_path()
        with open(token_file, 'w') as f:
            f.write(self.current_token)

    def _get_token_file_path(self):
        return os.path.join(TOKEN_CACHE_FOLDER, 'token')
