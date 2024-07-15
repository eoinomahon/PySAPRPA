import os
import re
from unidecode import unidecode

class HelperUtils():
    @staticmethod
    def _check_path_valid(how: str, directory: str, file_name: str) -> bool:
        '''
        Checks if path given in export() is valid.
            Args:
                directory (str): directory path
                file_name (str): desired file_name
                how (str): which export option: spreadsheet, text, etc...
            Returns:
                bool: True if file with same path already exists.
                Reason is that SAP gives options: generate and replace when
                saving file. Need to replace if file already exists. 
        '''
        if not os.path.isdir(directory):
            raise ValueError(f"Directory: {directory} does not exist")
        
        directory = os.path.abspath(directory)

        file_ext = os.path.splitext(file_name)[1]
        if how == 'spreadsheet':
            if file_ext.lower() != '.xlsx':
                raise ValueError("File extension should be '.xlsx'")
        elif how == 'local_file':
            pass # Add validation check

        elif how == 'word_processing':
            pass # Add validation check

        file_path = os.path.join(directory, file_name)
        file_exists = os.path.exists(file_path)

        return file_exists
    
    @staticmethod
    def _clean_field_text(name: str) -> str:
        cleaned_name = re.sub(r'[-/&]+', ' ', name)
        cleaned_name = unidecode(string=cleaned_name).lower()
        cleaned_name = re.sub(r'[^A-Za-z0-9 ]', '', cleaned_name)
        return cleaned_name.replace(' ', '_')
        
    @staticmethod
    def _modify_repeat_name(field_text: str, repeat_name_dict: dict):
        """Modify a field text to add a frequency suffix if it's repeated"""
        repeat_name_dict[field_text] = repeat_name_dict.get(field_text, 0) + 1
        name_freq = repeat_name_dict[field_text]
        if name_freq > 1:
            field_text = field_text + f'_{name_freq}'
        
        return field_text, repeat_name_dict
    
    @staticmethod
    def _find_shell_export(session, sap_shell_id):
        try:
            session.findById(sap_shell_id).pressToolbarContextButton("&NAVIGATION_PROFILE_TOOLBAR_EXPAND")
        except Exception:
            pass # Expand button already expanded or doesn't exist

        try:
            session.findById(sap_shell_id).pressToolbarContextButton("&MB_EXPORT")
            session.findById(sap_shell_id).SelectContextMenuItem("&XXL")

        except Exception:
            raise ValueError('Export not option')