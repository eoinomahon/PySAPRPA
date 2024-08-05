**Example Usage**

Here's an example of how to use the `ObjectTree` class to set the parameters in the screenshot:
```python
import pysaprpa as pysap

session = pysap.connect_SAP()  # Connect to SAP
conn = pysap.ObjectTree(session)

# Note, if you want to use a different date_format, it must be passed upon initialization of ObjectTree. 
(e.g. ObjectTree(session, date_format='%d/%m/%Y') for 'DD/MM/YYYY' format
 
conn.start_transaction("KSB1")  # Start transaction KSB1

conn.get_objects()  # Get objects in the current screen

# Set material and material type fields
conn.set_parameters(controlling_area_TEXT="*",
                    cost_center_BUTTON=['100', '200', '300'],
                    posting_date_TEXT=(7, 2024),
                    layout_TEXT='EXAMPLE',
                    more_settings_MORE={'output_in_alv_grid_FLAG'=True, 'maximum_no_of_hits'='999999'})
  
conn.execute()  # Execute the transaction

conn.get_objects() # VERY IMPORTANT AND EASY TO FORGET STEP. Need to get objects for new screen.

conn.export(how="spreadsheet", directory="C:\\Exports", file_name="KSB1_EXPORT.XLSX")  # Export

conn.end_transaction() # Takes user back to home screen and clears cache with object names and ids. If forgotten, can bug next transaction if chaining
```
This example finds line item data in SAP using transaction KSB1. It sets parameters, executes the transaction, and exports data to an excel file.
