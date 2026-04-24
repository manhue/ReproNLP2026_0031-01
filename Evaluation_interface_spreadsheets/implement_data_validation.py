from openpyxl import load_workbook
from openpyxl.worksheet.datavalidation import DataValidation

def add_readability_validation(file_path, column_letter):  # Adjust column if needed
    wb = load_workbook(file_path)
    ws = wb.active

    # Create data validation: only integers 1 to 5
    dv = DataValidation(type="whole", operator="between", formula1=1, formula2=5, showErrorMessage=True)
    dv.error = "Please enter an integer between 1 and 5."
    dv.errorTitle = "Invalid Input"

    # Apply to entire column (e.g., J2:J1000)
    dv.ranges.add(f"{column_letter}2:{column_letter}1000")
    ws.add_data_validation(dv)

    wb.save(file_path)

for idx in range(0, 5):
    add_readability_validation(f"qa_labeller_{idx}.xlsx", column_letter='E')
