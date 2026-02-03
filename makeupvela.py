from tempfile import template
from Flask import Flask, rendertemplate,url_for

makeupvelaApp=Flask (__name__)

@makeupvelaApp.route('/')
def home():
return '<h1> Consigue tu maquillaje con precio accesible <h1>'

if __name__ == '_main_':
    makeupvelaApp.run(port=2200,debug=True)