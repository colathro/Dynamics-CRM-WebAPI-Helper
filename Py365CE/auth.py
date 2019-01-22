from adal import *
from datetime import datetime



class user_context(AuthenticationContext):
    '''Implements AuthenticationContext from Python Adal Library
    Adds additional functionality for Executing Py365CE Request Classes'''

    default_headers = {'Content-Type': 'application/json; charset=utf-8',
                            'OData-MaxVersion': '4.0',
                            'OData-Version': '4.0',
                            'Accept': 'application/json'}
    api_query_stem = '/api/data/v9.0/'

    @property
    def is_authed(self):
        if len(self.cache._cache) >= 1:
            if not (datetime.strptime(self.get_auth_value('expiresOn'), '%Y-%m-%d %H:%M:%S.%f') < datetime.now()):
                self.default_headers.update({'Authorization':'Bearer ' + self.get_auth_value('accessToken')})
                return True
            else:
                return False
        else:
            return False

    def get_auth_value(self, val, item=0):
        if len(self.cache._cache) >= 1:
            try:
                return list(self.cache._cache.values())[item][val]
            except:
                raise AttributeError(f'{val} is not in the token cache. ' +
                                     f'Verify items: {list(list(self.cache._cache.values())[item].keys())}')
        else:
            raise AttributeError(f'Have you forgotten to acquire a token?.')

    def lazy_acquire_token_with_username_password(self, resource, username, password):
        '''Gets a token for a given resource via user credentails.
        Does not require clientId, we user another embedded clientId.
        
        :param str resource: A URI that identifies the resource for which the 
            token is valid.
        :param str username: The username of the user on behalf this
            application is authenticating.
        :param str password: The password of the user named in the username
            parameter.
        :returns: dict with several keys, include "accessToken" and
            "refreshToken".
        '''
        return super(user_context, self).acquire_token_with_username_password(resource, username, password, '51f81489-12ee-4a9e-aaae-a2591f45987d')
    
    