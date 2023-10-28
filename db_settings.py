SECRET_KEY = 'django-insecure-+=(9s^!4diw3*iy^%=w1fzelu%^@f^)_l25+t#6r5=5wbco=y('

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ssavi_db',
        'USER': 'root',
        # PASSWORD는 반드시 본인 sql PASSWORD로 진행
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'PORT': '3306'
    }
}