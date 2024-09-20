import copy
import json

from utils.json_to_xlsx import operating_statement_excel_field_mapping


def transform_array_data_to_json(data, subcategory, subcategory_feedback):
    try:
        formatted_json_response = {}
        formatted_json_response[subcategory] = {}



        for key, values in data[subcategory].items():
            # print('start')
            fields = []
            if isinstance(values, list):
                # print(values)
                for field in values:
                    # if isinstance(field, list):
                    if (subcategory == "revenue_income" and field[3] == "expenses") or (subcategory == "expenses" and field[3] == "income"):
                        fields.append({
                        "field_name": field[0],
                        "value": -float(str(field[1]).replace(',', '')),
                        "page_number": field[2],
                        "pdf_subheader_category": field[3]
                        })
                    else:
                        fields.append({
                        "field_name": field[0],
                        "value": float(str(field[1]).replace(',', '')),
                        "page_number": field[2]
                        })

            
            coa_label = None
            user_feedback = ""

            if subcategory == "assets":
                coa_label = operating_statement_excel_field_mapping["balance_sheet"]["assets"][key]
            elif subcategory == "liabilities":
                coa_label = operating_statement_excel_field_mapping["balance_sheet"]["liabilities"][key]
            elif subcategory == "revenue_income":
                coa_label = operating_statement_excel_field_mapping["income_statement"]["revenue_income"][key]
            elif subcategory == "expenses":
                coa_label = operating_statement_excel_field_mapping["income_statement"]["expenses"][key]

            if subcategory_feedback.get(key, None):
                user_feedback = subcategory_feedback[key].get("user_feedback", "")

            formatted_json_response[subcategory][key] = {
                "fields": fields,
                "label": coa_label,
                "user_feedback": user_feedback
            }

        print("subcategory: ", subcategory)

        return formatted_json_response[subcategory]
    except Exception as e:
        print(f"Error occured in : {transform_array_data_to_json.__name__} ", e)
        raise e


def format_os_response(json_response, balance_sheet_user_feedback, income_statement_user_feedback):
    try:
        new_json_response = copy.deepcopy(json_response)
        # print(balance_sheet)
        if new_json_response["is_balance_sheet_present"] == "Yes":
            balance_sheet = new_json_response["balance_sheet"]
            balance_sheet["assets"] = transform_array_data_to_json(balance_sheet, "assets", balance_sheet_user_feedback.get("assets", {}))
            balance_sheet["liabilities"] = transform_array_data_to_json(balance_sheet, "liabilities", balance_sheet_user_feedback.get("liabilities", {}))

        if new_json_response["is_income_statement_present"] == "Yes":
            income_statement = new_json_response["income_statement"]
            income_statement["revenue_income"] = transform_array_data_to_json(income_statement, "revenue_income", income_statement_user_feedback.get("revenue_income", {}))
            income_statement["expenses"] = transform_array_data_to_json(income_statement, "expenses", income_statement_user_feedback.get("expenses", {}))

        # print(json.dumps(balance_sheet, indent=2))

        return new_json_response
    except Exception as e:
        print(f"Error occured in : {format_os_response.__name__} ", e)
        raise e



     


