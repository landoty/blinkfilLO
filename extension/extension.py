import uno


# TODO:
# my_extension/
# ├── META-INF/
# │   └── manifest.xml
# ├── script.py
# ├── description.xml
# ├── unopkg.xml
# └── other_resources/
# zip -r blinkfiLO_extension.oxt META-INF/ extension.py description.xml unopkg.xml



def connect_to_calc():
    # Manually allow libreoffice to listen for UNO command
    # (unnecessary once the extension is packaged and installed):
    # soffice --accept="socket,host=localhost,port=2002;urp;"

    # Connect to the running LibreOffice instance
    local_context = uno.getComponentContext()
    resolver = local_context.ServiceManager.createInstanceWithContext(
        "com.sun.star.bridge.UnoUrlResolver", local_context
    )
    ctx = resolver.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
    
    smgr = ctx.ServiceManager
    desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
    
    # Get the current active document (if any)
    document = desktop.getCurrentComponent()  # Get the currently active document
    if not document:
        raise Exception("No document is currently open in LibreOffice Calc.")

    return document
    
def read_from_calc(document):
    # Get the active sheet
    sheet = document.CurrentController.ActiveSheet
    
    # Get the current selection (range of selected cells)
    selection = document.CurrentController.getSelection()
    
    # Check if the selection is a single cell or a range
    if selection.supportsService("com.sun.star.sheet.SheetCellRange"):
        # Get the range of selected cells
        start_column = selection.RangeAddress.StartColumn
        end_column = selection.RangeAddress.EndColumn
        start_row = selection.RangeAddress.StartRow
        end_row = selection.RangeAddress.EndRow

        # Create a list to store the data from the selected range
        selected_data = []

        # Loop through the range and read data from each cell
        for col in range(start_column, end_column + 1):
            col_data = []
            for row in range(start_row, end_row + 1):
                cell = sheet.getCellByPosition(col, row)
                col_data.append(cell.String)  # Or cell.Value for numerical values
            selected_data.append(col_data)

        return selected_data
    else:
        # If a single cell is selected, just return its value
        return [[selection.String]]  # Return as a nested list for consistency
                # Return the string content of the cell

def write_to_calc(document, new_value):
    sheet = document.Sheets.getByIndex(0)
    cell = sheet.getCellByPosition(1, 0)   # Write to cell B1 (1, 0)
    cell.String = new_value                # Set the new value

def main():
    doc = connect_to_calc()
    data = read_from_calc(doc)
    print(f"Read from Calc: {data}")
    
    # # Process the data (for example, convert it to uppercase)
    # new_data = data.upper()
    
    write_to_calc(doc, "Momma")

# Make functions available for LibreOffice Macros
__all__ = ['main']