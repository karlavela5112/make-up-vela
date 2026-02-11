class Config:
    SECRET_KEY  ='OJITOFHUFflgnnfgnjfdotriodj255555'
    DEBUG   =True

class DevelopmentConfig(Config):
    MYSQL_HOST      ='localhost'
    MYSQL_USER      ='root'
    MYSQL_PASSWORD  ='mysql'
    MYSQL_DB        ='makeupvela'     

config ={
    'development':DevelopmentConfig
} 