from pysaprpa.utils.validation._validate import ValidUtils as valid_utils
from pysaprpa.utils.add_func._button import SAPGUIButtonUtils as button_utils
import pandas as pd

class SAPGUIParameterUtils:
    def __init__(self, session, sap_fields_dict, vkey_map, variant, date_format: str):
        self.session = session
        self.sap_fields_dict = sap_fields_dict
        self.vkey_map = vkey_map
        self.variant = variant
        self.date_format = date_format
    
    def _set_variant(self):
        if self.vkey_map != None:
            vkey = self.vkey_map.get('B_VARI', None)
            if vkey:
                self.session.FindById("wnd[0]").sendVKey(int(vkey))
                
    def _set_text_field(self, user_input, object_ids, object_name):
        """
        Sets the text field of one or more objects based on the user input.

        Parameters
        ----------
        user_input : list or str or None
            The input value to set the text field(s) to.
        object_ids : list
            A list of object IDs to set the text field for.
        object_name : str
            The name of the object being set.

        Raises
        ------
        ValueError
            If the length of user_input is greater than the length of object_ids, or if user_input is not a list, string, or None.

        Notes
        -----
        If user_input is a list, it sets the text field of each object in object_ids to the corresponding value in user_input. If user_input is shorter than object_ids, it fills in the remaining objects with empty strings.

        If user_input is a string, it sets the text field of the first object in object_ids to the input string, and sets the text field of any remaining objects to empty strings.

        If user_input is None, it sets the text field of all objects in object_ids to empty strings.

        The `variant` attribute of the class instance is used to determine whether to fill in remaining objects with empty strings or not.
        """
        if isinstance(user_input, list):
            if len(user_input) > len(object_ids):
                raise ValueError(f"Too many parameters. Expect {len(object_ids)} args for {object_name.split('_')[:-1]}")
            
            while len(user_input) < len(object_ids) and self.variant == '':
                user_input.append('')

            for i in range(len(user_input)):
                self.session.FindById(object_ids[i]).text = user_input[i]
        
        elif isinstance(user_input, (str, int)):
            self.session.FindById(object_ids[0]).text = user_input

            if len(object_ids) > 1 and self.variant == '':
                for i in range(1, len(object_ids)):
                    self.session.FindById(object_ids[i]).text = ''

        elif user_input is None:
            if self.variant == '':
                for i in range(len(object_ids)):
                    self.session.FindById(object_ids[i]).text = ''
        
        else:
            raise ValueError(f'Invalid text input')
    
    def _set_date_field(self, user_input, object_ids, object_name):
        """
        Sets the date field of one or more objects based on the user input.

        Parameters
        ----------
        user_input : str or tuple or list or None
            The input value to set the date field(s) to.
        object_ids : list
            A list of object IDs to set the date field for.
        object_name : str
            The name of the object being set.

        Raises
        ------
        ValueError
            If user_input is not a string, tuple, list, or None, or if the format is invalid.

        Notes
        -----
        If user_input is a string, it sets the date field of the first object in object_ids to the input string.

        If user_input is a tuple, it sets the date field of the first two objects in object_ids to the input tuple.

        If user_input is a list, it sets the date field of each object in object_ids to the corresponding value in user_input.

        The `variant` attribute of the class instance is used to determine whether to set the date field to empty strings if user_input is None.
        """
        if user_input is None:
            if self.variant == '':
                for ind in range(len(object_ids)):
                    self.session.FindById(object_ids[ind]).text = ''    
            return

        if isinstance(user_input, str):
            date = valid_utils._check_date_valid(user_input, i=0, date_format=self.date_format)
            self.session.findbyid(object_ids[0]).text = date

        elif isinstance(user_input, tuple):
            # If single tuple given, set both dates
            date = valid_utils._check_date_valid(user_input, i=0, date_format=self.date_format)
            self.session.findbyid(object_ids[0]).text = date
            date = valid_utils._check_date_valid(user_input, i=1, date_format=self.date_format)
            self.session.findbyid(object_ids[1]).text = date

        # IF user gives list, check if list contains string or tuple
        elif isinstance(user_input, list):
            # if tuple: if ind == 0 -> grab first date of that month and year, if ind == 1 -> grab last date of that month and year
            for ind in range(len(user_input)):
                val = user_input[ind]
                date = valid_utils._check_date_valid(val, i=ind, date_format=self.date_format)
                self.session.findbyid(object_ids[ind]).text = date
        else:
            raise ValueError('Invalid date input.')

    def _set_button(self, user_input, object_ids, object_name):
        """
        Sets the button value of one or more objects based on the user input.

        Parameters
        ----------
        user_input : list or pd.Series or None
            The input value to set the button value(s) to.
        object_ids : list -> should only contain one value
            A list of object ID (singluar) to set the button value for.
        object_name : str
            The name of the object being set.

        Raises
        ------
        ValueError
            If user_input is not a list or pd.Series.

        Notes
        -----
        If user_input is a list or pd.Series, it sets the button value of the object in object_ids to the corresponding value in user_input.
        """
        if user_input is None:
            return
        if isinstance(user_input, (list, pd.Series)):
            button_utils(self.session)._button_func(user_input, object_ids, object_name)
        else:
            raise ValueError('Button value MUST be pd.Series or list')
    
    def _set_flag(self, user_input, object_ids, object_name):
        """
        Sets the flag value of one or more objects based on the user input.

        Parameters
        ----------
        user_input : bool or None
            The input value to set the flag value(s) to.
        object_ids : list
            A list of object IDs to set the flag value for.
        object_name : str
            The name of the object being set.

        Raises
        ------
        ValueError
            If user_input is not a bool.

        Notes
        -----
        If user_input is a bool, it sets the flag value of the first object in object_ids to the input bool.

        The `variant` attribute of the class instance is used to determine whether to set the flag value to False if user_input is None.
        """
        if user_input is None:
            if self.variant == '':
                self.session.findById(object_ids[0]).selected = False
            return

        if isinstance(user_input, bool):
            self.session.findById(object_ids[0]).selected = user_input

        else:
            raise ValueError(f'{object_name}_FLAG value must be bool')
    
    def _set_selection(self, user_input: bool, object_ids: str, object_name: str):
        """
        Sets the selection value of one or more objects based on the user input.

        Parameters
        ----------
        user_input : bool or None
            The input value to set the selection value(s) to.
        object_ids : str
            The object ID to set the selection value for.
        object_name : str
            The name of the object being set.

        Raises
        ------
        ValueError
            If user_input is not a bool.

        Notes
        -----
        If user_input is a bool, it sets the selection value of the object in object_ids to the input bool.
        """
        if user_input is None:
            return
        
        if isinstance(user_input, bool):
            if user_input:
                self.session.findById(object_ids[0]).select()
            return
        
        else:
            raise ValueError(f'{object_name}_FLAG values must be bool')