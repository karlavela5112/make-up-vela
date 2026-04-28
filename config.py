class Config:
    SECRET_KEY  ='OJITOFHUFflgnnfgnjfdotriodj255555'
    DEBUG   =True

class DevelopmentConfig(Config):
    MYSQL_HOST      ='localhost'
    MYSQL_USER      ='root'
    MYSQL_PASSWORD  ='mysql'
    MYSQL_DB        ='makeupvela' 
class MailConfig(Config):
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'karla.vela5112@alumnos.udg.mx'
    MAIL_PASSWORD = 'rijs cpum qmxn egbp'
    MAIL_DEFAULT_SENDER = 'karla.vela5112@alumnos.udg.mx'
    MAIL_ASCII_ATTACHMENTS = True

config ={
    'development':DevelopmentConfig,
    'mail':MailConfig
} 