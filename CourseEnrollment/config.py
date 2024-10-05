import os


class Config(object):
    SECRET_KEY=os.environ.get('SEVRET_KEY') or "secret_string"
    MONGODB_SETTINGS= {'db': 'U_Enrollment',
                      'host':'mongodb://localhost:27017/U_Enrollment'}