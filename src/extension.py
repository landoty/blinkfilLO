import uno
import json

# TODO:
# my_extension/
# ├── META-INF/
# │   └── manifest.xml
# ├── script.py
# ├── description.xml
# ├── unopkg.xml
# └── other_resources/
# zip -r blinkfiLO_extension.oxt META-INF/ extension.py description.xml unopkg.xml

class CalcHandler:
    def __init__(self, host="localhost", port=3000):
        """
        Initialize the LibreOffice Calc handler by connecting to the running LibreOffice instance.
        """
        self.host = host
        self.port = port
        self.document = self.connect_to_calc()
        self.incomplete_cells = []
        self.formula = ""

    def connect_to_calc(self):
        # Manually allow libreoffice to listen for UNO command
        # (unnecessary once the extension is packaged and installed):
        # soffice --accept="socket,host=localhost,port=2002;urp;"

        """
        Connect to the running LibreOffice instance and get the current document.
        """
        local_context = uno.getComponentContext()
        resolver = local_context.ServiceManager.createInstanceWithContext(
            "com.sun.star.bridge.UnoUrlResolver", local_context
        )
        ctx = resolver.resolve(f"uno:socket,host={self.host},port={self.port};urp;StarOffice.ComponentContext")
        
        smgr = ctx.ServiceManager
        desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
        
        # Get the current active document (if any)
        document = desktop.getCurrentComponent()
        if not document:
            raise Exception("No document is currently open in LibreOffice Calc.")

        return document

    def read_selected_data(self):
        """
        Read data from the current selection in the active sheet.
        """
        sheet = self.document.CurrentController.ActiveSheet
        selection = self.document.CurrentController.getSelection()
        
        if selection.supportsService("com.sun.star.sheet.SheetCellRange"):
            start_column = selection.RangeAddress.StartColumn
            end_column = selection.RangeAddress.EndColumn
            start_row = selection.RangeAddress.StartRow
            end_row = selection.RangeAddress.EndRow

            selected_data = []
            for col in range(start_column, end_column + 1):
                col_data = []
                for row in range(start_row, end_row + 1):
                    cell = sheet.getCellByPosition(col, row)
                    if cell.String == "":
                        empty_coord = (col,row + 1)
                        corresponding_input_coord = (col -1, row + 1)
                        pair = {"Input": corresponding_input_coord, "Output": empty_coord}
                        self.incomplete_cells.append(pair) # Save empty cells to write to later
                    col_data.append(cell.String)
                selected_data.append(col_data)

            print("\nEMPTY OUTPUT CELLS: ", self.incomplete_cells)

            return selected_data
        else:
            return [[selection.String]]


    def jsonify_data(self, data):
        """
        Convert selected data to a JSON format.
        """
        json_structure = {"Examples": []}
        for i in range(len(data[0])):
            input = data[0][i]
            output = data[1][i]

            if input == "" or output == "":
                continue

            json_structure["Examples"].append({
                "Input": [input],
                "Output": output,
            })

        json_output = json.dumps(json_structure, indent=2)
        print("\nDATA GATHERED FROM LIBREOFFICE CALC -> JSON: ", json_output)
        return json_output

    def save_json_file(self, jsonified_data, output_file="output.json"):
        """
        Save JSON data to a file.
        """
        if isinstance(jsonified_data, str):
            jsonified_data = json.loads(jsonified_data)

        with open(output_file, "w") as file:
            json.dump(jsonified_data, file, indent=2)
        print(f"JSONified data has been saved to {output_file}")

    def get_synth_input(self):
        data = self.read_selected_data()
        jsonified_data = self.jsonify_data(data)
        self.save_json_file(jsonified_data)

    def get_cell_ref_by_position(self, coord):
        col, row = coord
        
        # convert col index to grid letter 0 -> A, 1 -> B, etc
        col_letter = chr(col + 65)  # 65 is ASCII for 'A'
        
        # convert row index to grid row number 0 -> 1, 1 -> 2
        row_number = row
        
        # return full cell ref
        return f"{col_letter}{row_number}"
    

    def write_string_to_cell(self, new_value, col, row):
        """
        Write a value to a specific cell in the active sheet.
        """
        sheet = self.document.Sheets.getByIndex(0)
        cell = sheet.getCellByPosition(col, row)
        cell.String = new_value

    def write_formula_to_cell(self, formula, col, row):
        """
        Set the formula to the cell without updating its value.
        """
        sheet = self.document.Sheets.getByIndex(0)
        cell = sheet.getCellByPosition(col, row)
        cell.Formula = formula  # Assign the formula to the cell

    def write_to_calc(self):
        for pair in self.incomplete_cells:
            formula = self.formula
            formula = formula.replace("<input>", self.get_cell_ref_by_position( (pair["Input"][0], pair["Input"][1]) ))
            # formula = "=" + formula
            print(f"\nFormula for cell pair {pair}: ", formula)
            self.write_string_to_cell(formula, pair["Output"][0], pair["Output"][1] - 1)
            # self.write_formula_to_cell(formula, pair["Output"][0], pair["Output"][1] - 1)