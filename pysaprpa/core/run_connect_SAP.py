import win32com.client


def connect_SAP():
    """
    Returns
    ----------
    session: The session object is neccessary to interact with SAP.
    """ 
    SapGuiAuto = win32com.client.GetObject('SAPGUI')
    application = SapGuiAuto.GetScriptingEngine
    connection = application.Children(0)
    session = connection.Children(0)
    return session