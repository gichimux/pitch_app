from flask import render_template
from . import if __name__ == '__main__':
    
@main.app_errorhandler(404)
def four_Ow_four(error):
    '''
    function to render 404
    '''
    return render_template('fourOwfour.html'),404    