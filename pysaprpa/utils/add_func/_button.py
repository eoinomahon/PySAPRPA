import pandas as pd
class SAPGUIButtonUtils():
    def __init__(self, session):
        self.session = session
    
    def _clear_and_paste(self):
        self.session.FindById("wnd[1]").sendVKey(16) # Delete
        self.session.FindById("wnd[1]").sendVKey(24) # Paste from clipboard
        self.session.FindById("wnd[1]").sendVKey(0) # Confirm
        self.session.FindById("wnd[1]").sendVKey(8) # Execute

    def _button_func(self, user_input, object_id, object_name):
        if isinstance(user_input, (pd.Series, list)):
            # Convert to series if list
            if isinstance(user_input, list):
                user_input = pd.Series(user_input)
            
            # Copy to clipboard
            user_input.to_clipboard(excel=True, header=False, index=False)
            # Press the SAP GUI button
            self.session.FindById(object_id[0]).press()
            # Clear and paste the clipboard contents into the field
            SAPGUIButtonUtils._clear_and_paste(self)
        else:
            raise ValueError('Group must be pd.Series or list')