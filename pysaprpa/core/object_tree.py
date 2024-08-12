import json
from typing import Union
from pysaprpa.utils import HelperUtils as helper_utils, SAPGUIParameterUtils
from pysaprpa.core.run_connect_SAP import connect_SAP 

class ObjectTree:
    def __init__(self, session: object = None, date_format: str = '%m/%d/%Y'):
        """
        Initialize the ObjectTree class.

        Parameters
        ----------
        session : object, optional
            The SAP session object. If not provided, a new connection to SAP is established.
        date_format : str, optional
            The date format to be used. Default is '%m/%d/%Y'.

        Attributes
        ----------
        session : object
            The SAP session object.
        date_format : str
            The date format used.
        info_retrieved_list : list
            List of information to be retrieved from SAP objects.
        object_tree : None
            The object tree retrieved from SAP.
        sap_fields_dict : dict
            Dictionary to store SAP fields.
        vkey_map : dict
            Dictionary to store virtual key mappings.
        repeat_field_label_dict : dict
            Dictionary to store repeat field labels.
        object_left_label : list
            List to store left labels of objects.
        export_options_dict : dict
            Dictionary to store export options.

        Raises
        ------
        Exception
            If failed to connect to SAP.

        Notes
        -----
        If `session` is not provided, a new connection to SAP is established using the `connect_SAP` function.
        The `info_retrieved_list` contains the information to be retrieved from SAP objects.
        The other attributes are initialized as empty dictionaries, lists, or None.

        Example
        -------
        >>> object_tree = pysaprpa.ObjectTree(session, date_format='%d/%m/%Y')
        >>> ObjectTree instance created with european date format.
        """
        self.session = session
        if session is None:
            self.session = connect_SAP()
            if self.session is None:
                raise Exception("Failed to connect to SAP")
        self.date_format = date_format
        self.info_retrieved_list = ['Id', 'Text', 'Type', 'Changeable', 'Name', 'IconName']
        self.object_tree = None
        self.sap_fields_dict = {}
        self.vkey_map = {}
        self.repeat_field_label_dict = {}
        self.object_left_label = []
        self.export_options_dict = {}

    def start_transaction(self, t_code: str = None):
        """
        Parameters
        ----------
        t_code : str, optional
            The T-code to start the transaction with. Default is None.

        Returns
        -------
        ObjectTree
            The updated instance of the class.

        Description
        -----------
        This method starts a new transaction in the SAP system using the specified T-code. If no T-code is provided, a ValueError is raised.

        Notes
        -----
        The method uses the `StartTransaction` method of the SAP session object to start the transaction. It then returns the updated instance of the class.

        Example
        -------
        >>> object_tree.start_transaction('MB51')
        >>> Now you are on the parameter screen for MB51
        """
        if t_code is None:
            raise ValueError('Need T-Code to run')
        
        try:
            self.session.StartTransaction(t_code)
        except Exception:
            raise ValueError('Invalid T-Code')
        
        return self

    def end_transaction(self):
        """
        Returns
        -------
        ObjectTree
            The updated instance of the class.

        Description
        -----------
        This method ends the current transaction in the SAP system and backs the user out to the menu.

        Notes
        -----
        The method uses the `EndTransaction` method of the SAP session object to end the transaction. It then returns the updated instance of the class.

        Example
        -------
        >>> object_tree.end_transaction()
        >>> Now you are back on the menu
        """
        # Reset the mentioned attributes to their original value
        self.object_tree = None
        self.sap_fields_dict = {}
        self.vkey_map = {}
        self.repeat_field_label_dict = {}
        self.object_left_label = []
        self.export_options_dict = {}
        
        self.session.EndTransaction()
        return self

    def get_objects(self, window: int = 0) -> 'ObjectTree':
        """
        Parameters
        ----------
        window : int, optional
            The window number to retrieve the object tree from. Default is 0.

        Returns
        -------
        ObjectTree
            The updated instance of the class.

        Description
        -----------
        This method retrieves the object tree from the SAP system using the specified window number. It then parses the object tree and extracts relevant field information.

        Notes
        -----
        The method uses the `GetObjectTree` method of the SAP session object to retrieve the object tree. It then iterates through the object tree, extracting field properties and storing them in instance variables. The method also uses dictionaries to store repeat field labels, SAP fields, and virtual key mappings.

        The method is recursive, meaning it calls itself to parse nested object trees. It uses a separate method, `_get_field_properties`, to extract field properties from each object in the object tree. The method also uses separate methods to process different types of objects, such as text, button, select, and flag objects.

        The method returns the updated instance of the class, which contains the parsed object tree and relevant field information.

        Example
        -------
        >>> object_tree.get_objects()
        >>> Parsed and named SAP objects. Stored labels and object ids (where objects are) in sap_fields_dict
        """
        try:
            object_tree = self.session.GetObjectTree(f'wnd[{window}]', self.info_retrieved_list)
            parsed_data = json.loads(object_tree)
            self.object_tree = parsed_data['children']
        
        except Exception:
            raise ValueError('User does not have permission to use session.GetObjectTree. Speak to your SAP admins')

        # Move the parsing logic here
        self.FIELD_TYPE_MAP = {
            'GuiTextField': 'TEXT',
            'GuiCTextField': 'TEXT',
            'GuiLabel': 'TEXT',
            'GuiButton': 'BUTTON',
            'GuiRadioButton': 'SELECT',
            'GuiCheckBox': 'FLAG',
            'GuiMenu': 'MENU',
            'GuiShell': 'SHELL',
            '_': 'MORE' # Because BUTTON has MORE as well, '_' won't trip false gui type
        }

        self.COMMON_BUTTONS = {
            'B_EXEC': 'execute',
            'B_VARI': 'variant'
        }

        def _get_field_properties(object) -> tuple:
            """
            Extracts field properties from the object.

            Args:
                object (dict): The object to extract properties from.

            Returns:
                tuple: A tuple containing the field properties.
            """
            return (
                object['properties'].get('Id', None).split('ses[0]/')[1],
                helper_utils._clean_field_text(object['properties'].get('Text', None)),
                object['properties'].get('Type', None),
                object['properties'].get('Changeable', None),
                object['properties'].get('Name', None),
                object['properties'].get('IconName', None),
            )

        def _parse_object_tree(
                tree=self.object_tree, 
                repeat_field_label_dict=self.repeat_field_label_dict, 
                object_left_label=self.object_left_label, 
                sap_fields_dict=self.sap_fields_dict, 
                vkey_map=self.vkey_map, 
                session=self.session, 
                export_options_dict=self.export_options_dict):
            """
            Parses the object tree and extracts relevant field information.

            Args:
                tree (list[dict]): The object tree to parse.
                repeat_field_label_dict (dict): A dictionary to store repeat field labels.
                last_label_list (list[str]): A list to store the last label encountered.
                sap_fields_dict (dict): A dictionary to store SAP fields.
                vkey_map (dict): A dictionary to store virtual key mappings.
                session (object): The SAP session object.
                export_options_dict (dict): A dictionary to store export options.

            Returns:
                ObjectTree: The updated instance of the class.
            """
            for object in tree:
                if 'children' in object:
                    _parse_object_tree(object['children'], repeat_field_label_dict, object_left_label, sap_fields_dict, vkey_map, session, export_options_dict)

                object_id, object_text, object_type, object_changable, object_name, object_icon_name = _get_field_properties(object)
                object_type = self.FIELD_TYPE_MAP.get(object_type, None)

                if object_type is None:
                    continue
                if object_type == 'TEXT':
                    self._process_text_object(object_id, object_text, object_changable)
                elif object_type in ['BUTTON', 'MORE']:
                    self._process_button_object(object_id, object_text, object_name, object_icon_name)
                elif object_type in ['SELECT', 'FLAG']:
                    self._process_select_or_flag_object(object_id, object_text, object_type)
                elif object_type == 'MENU':
                    self._process_menu_object(object_id, object_text)
                elif object_type == 'SHELL':
                    self._process_shell_object(object_id, object_name)
                else:
                    dict_key = object_left_label[-1] + '_' + object_type
                    sap_fields_dict.setdefault(dict_key, []).append(object_id)

            return self

        return _parse_object_tree()
    
    def _process_text_object(self, object_id, object_text, object_changable):
        if object_changable == 'false':
            field_text, self.repeat_field_label_dict = helper_utils._modify_repeat_name(object_text, self.repeat_field_label_dict)
            if self.session.FindById(object_id).LeftLabel is None:
                self.object_left_label.append(field_text)

        else:
            dict_key = self.object_left_label[-1] + '_' + 'TEXT'
            self.sap_fields_dict.setdefault(dict_key, []).append(object_id)

    def _process_button_object(self, object_id, object_text, object_name, object_icon_name):
        if object_icon_name in self.COMMON_BUTTONS:
            button_num = object_name.split('[')[-1][:-1]
            self.vkey_map[object_icon_name] = button_num
        elif object_icon_name == 'B_MORE':  # B_MORE is filter button name
            dict_key = self.object_left_label[-1] + '_' + 'BUTTON'
            self.sap_fields_dict.setdefault(dict_key, []).append(object_id)
        elif object_text != '':
            dict_key = object_text + '_' + 'MORE'
            self.sap_fields_dict.setdefault(dict_key, []).append(object_id)
    
    def _process_select_or_flag_object(self, object_id, object_text, object_type):
        field_text, self.repeat_field_label_dict = helper_utils._modify_repeat_name(object_text, self.repeat_field_label_dict)
        dict_key = field_text + '_' + object_type
        self.sap_fields_dict.setdefault(dict_key, []).append(object_id)

    def _process_menu_object(self, object_id, object_text):
        parent_text = helper_utils._clean_field_text(self.session.FindById(object_id).parent.text)

        if parent_text == 'export':
            # Don't add label to repeat_field_name_dict unless we're actually using label
            field_text, self.repeat_field_label_dict = helper_utils._modify_repeat_name(object_text, self.repeat_field_label_dict)
            self.export_options_dict.setdefault(field_text, object_id)
    
    def _process_shell_object(self, object_id, object_name):
        if object_name == 'shell':
            self.sap_shell_id = object_id

    def set_parameters(
            self,
            variant: str = '',
            **kwargs
    ) -> 'ObjectTree':
        
        """
        Set Parameters for an ObjectTree Instance

        Parameters
        ----------
        variant : str, optional
            The variant to set.
        \*\*kwargs : dict
            Additional parameters to set.

        Kwargs Notes
        ------------
        Dynamic Naming:

            Labels/field names are creating by cleaning object labels (by replacing special characters and replacing spaces with underscores), and appending input types to the end of the cleaned label:
                cleaned names:
                    - Máterial -> material
                    - Cómpany Code -> company_code
                    - Incl. all items -> incl_all_items
                    - Database -> database
                    - Morè Settings -> more_settings

                
                input types:
                    - Text Field: label_TEXT
                    - Button Field: label_BUTTON
                    - Radio Button: label_SELECT
                    - Flag: label_FLAG
                    - More: label_MORE

                combined:
                    - material_TEXT
                    - company_code_BUTTON
                    - incl_all_items_SELECT
                    - database_FLAG
                    - more_settings_MORE

        Exception: Repeated Field Names:
            When a field name is repeated, the library appends a frequency suffix to distinguish between occurrences. For example:
                - First occurrence: sold_by_TEXT
                - Second occurrence: sold_by_2_TEXT
                - Third occurrence: sold_by_3_TEXT
                - Etc…

        Variants:
            Variants determine how keyword arguments (kwargs) are treated. If a variant is given, user-passed kwargs take priority over variant values, but if a kwarg is not passed (omitted from the function call), the variant value remains unchanged. Thus, if a variant is given but a user passes a kwarg with a blank value, the blank value takes priority.

        Acceptable Kwargs by Input Type:
            - _TEXT: Accepts either a string or a list of strings.
            - _BUTTON: Accepts a list or a pandas Series.
            - _SELECT: Accepts a boolean.
            - _FLAG: Accepts a boolean.
            - _MORE: Accepts a dictionary.

        Special Case: Date Values:
            - String date values must follow format given in ObjectTree init.
            - Date values can also be provided as tuples (month, year) in the format (MM: int, YYYY: int).

        Returns
        -------
        ObjectTree
            The ObjectTree instance with the set parameters.

        Example
        -------
        >>> obj.set_parameters(cost_center_BUTTON=['100', '200', '300'], posting_date_TEXT=(7,2024), layout_TEXT='/EOIN', more_settings_MORE={'maximum_no_of_hits_TEXT': '999999', 'output_in_alv_grid_FLAG': True})
        >>> PICTURE OF RESULT IN docs
        """
        VALID_INPUT_TYPES = {value: 0 for value in self.FIELD_TYPE_MAP.values()}

        set_parameter_utils = SAPGUIParameterUtils(self.session, self.sap_fields_dict, self.vkey_map, variant, self.date_format)

        if variant != '':
            set_parameter_utils._set_variant()
            temporary_tree = ObjectTree(self.session)
            temporary_tree.get_objects(window=1).set_parameters(variant_TEXT=variant).execute(vkey=8)

        for object_name, object_ids in self.sap_fields_dict.items():
            object_name_list = object_name.split('_')
            object_input_type = object_name_list[-1]
            if object_input_type not in VALID_INPUT_TYPES:
                raise ValueError('Invalid input type')

            user_input = kwargs.get(object_name, None)

            if object_input_type == 'TEXT':
                if object_name_list[-2] == 'date':
                    set_parameter_utils._set_date_field(user_input, object_ids, object_name)
                else:
                    set_parameter_utils._set_text_field(user_input, object_ids, object_name)

            elif object_input_type == 'BUTTON':
                set_parameter_utils._set_button(user_input, object_ids, object_name)

            elif object_input_type == 'MORE':
                if user_input is not None:
                    self.session.FindById(object_ids[0]).press()
                    temporary_tree = ObjectTree(self.session)
                    temporary_tree.get_objects(window=1).set_parameters(**user_input).execute(vkey=0)

            elif object_input_type == 'FLAG':
                set_parameter_utils._set_flag(user_input, object_ids, object_name)

            elif object_input_type == 'SELECT':
                set_parameter_utils._set_selection(user_input, object_ids, object_name)

        return self

    def execute(self, vkey: Union[int, str] = '') -> 'ObjectTree':
        """
        Parameters
        ----------
        how : str
            The export method.
        directory : str
            The directory to export to.
        file_name : str
            The file name to export as.

        Returns
        -------
        ObjectTree
        
        Notes
        -------
        After execution, `self.object_tree` attribute is set to `None`. 
        This is because execution often results in a new screen, and users must call `get_objects()` again to retrieve the updated objects.

        Example
        -------
        >>> object_tree.execute()
        >>> Told SAP to execute
        """
        if vkey == '':
            if self.vkey_map is not None:
                vkey = self.vkey_map.get('B_EXEC', None)
            else:
                raise ValueError('Vkey objects not found')

        self.session.FindById("wnd[0]").sendVKey(int(vkey))
        self.object_tree = None

        return self

    def export(self, how: str, directory: str, file_name: str) -> str:
        """
        Parameters
        ----------
        how : str
            The export method.
        directory : str
            The directory to export to.
        file_name : str
            The file name to export as.

        Returns
        -------
        str
            The exported file path.

        Notes
        -----
        This function exports data from the SAP system using the specified export method, and saves it to the specified directory with the specified file name.

        Example
        -------
        >>> object_tree.export(how='spreadsheet', directory='/fake/path', file_name='EXAMPLE.XLSX')
        >>> Exported SAP data as spreadsheet
        """
        import os

        file_exists = helper_utils._check_path_valid(how, directory, file_name)
        
        if file_name.split('.')[-1].upper() not in ['XLSX', 'XLS']:
            raise ValueError('Library only supports exporting excel files for the time being')
        
        if self.export_options_dict:
            export_option_id = self.export_options_dict.get(how, None)
            self.session.FindById(export_option_id).select()

        elif self.sap_shell_id:
            helper_utils._find_shell_export(self.session, self.sap_shell_id)

        else:
            raise ValueError('Export option not found')

        self.session.FindById("wnd[1]").sendVKey(0)  # Enter

        temp_tree = ObjectTree(self.session)
        temp_tree.get_objects(window=1).set_parameters(directory_TEXT=directory, file_name_TEXT=file_name)

        if file_exists:
            self.session.findById("wnd[1]").sendVKey(11)  # Replace
        else:
            self.session.findById("wnd[1]").sendVKey(0)  # Generate

        self.path = os.path.join(directory, file_name)
        return self

