import jwt
import datetime as dt
from flask import current_app as app
from flask import Blueprint

jwt_algorithm = 'HS256'
secret_key = app.config.get('SECRET_KEY')

# Blueprint Configuration
api_bp = Blueprint('api_bp', __name__,
    url_prefix='/api',
    template_folder='templates',
    static_folder='static')

def encode_token(user_id):
    """ Generates token for authorization"""

    # Generates testing token
    if app.config.get('TESTING') == True:
        return TestToken(user_id)
    
    payload = {
        'exp': dt.datetime.utcnow() + dt.timedelta(minutes=1),
        # 'exp': dt.datetime.utcnow() + dt.timedelta(seconds=5),
        'iat': dt.datetime.utcnow(),
        'sub': user_id
    }

    # Returns auth token containing user id
    return jwt.encode(
        payload,
        secret_key,
        jwt_algorithm
    )

def decode_token(token):
    """Returns token payload"""

    # Decodes testing token
    if app.config.get('TESTING') == True:
        if token in ['Expired Signature','Invalid Token']:
            return TokenPayload(
                valid=False,
                value=token
            )
        else:
            return TokenPayload(
                valid=True,
                value=token
            )
    
    try:
        payload = jwt.decode(
            token,
            secret_key
        )
        # Returns decoded user id in TokenPayload
        return TokenPayload(
            valid=True,
            value=payload['sub']
        )
    except jwt.ExpiredSignatureError:
        return TokenPayload(
            valid=False,
            value='Expired Signature'
        )
    except jwt.InvalidTokenError:
        return TokenPayload(
            valid=False,
            value='Invalid Token'
        )

class TokenPayload:
    """TokenPayload object used by decode_token"""
    def __init__(self,valid,value):
        self.valid = valid
        self.value = value


class TestToken:
    """ A token used during testing

    TestToken replaces token generation by jwt due to
    the library not working in a testing framework.
    """
    def __init__(self,id):
        self.token = id
    
    def decode(self):
        """ replaces decode method in jwt tokens """
        return self.token # returns user id