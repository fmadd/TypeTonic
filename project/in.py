import eel

eel.init('web')

@eel.expose
def get_data():
    return 'Get data from python'

eel.start('indexx.html')