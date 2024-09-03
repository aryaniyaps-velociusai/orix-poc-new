import copy
import json


def transform_array_data_to_json(data, subcategory):
    formatted_json_response = {}
    formatted_json_response[subcategory] = {}

    for key, values in data[subcategory].items():
        # print('start')
        fields = []
        if isinstance(values, list):
            # print(values)
            for field in values:
                # if isinstance(field, list):
                fields.append({
                "field_name": field[0],
                "value": field[1],
                "page_number": field[2]
                })
        formatted_json_response[subcategory][key] = {
            "fields": fields
        }

    print("subcategory: ", subcategory)

    return formatted_json_response[subcategory]


def format_os_response(json_response):
    new_json_response = copy.deepcopy(json_response)
    # print(balance_sheet)
    if new_json_response["is_balance_sheet_present"] == "Yes":
        balance_sheet = new_json_response["balance_sheet"]
        balance_sheet["assets"] = transform_array_data_to_json(balance_sheet, "assets")
        balance_sheet["liabilities"] = transform_array_data_to_json(balance_sheet, "liabilities")

    if new_json_response["is_income_statement_present"] == "Yes":
        income_statement = new_json_response["income_statement"]
        income_statement["revenue_income"] = transform_array_data_to_json(income_statement, "revenue_income")
        income_statement["expenses"] = transform_array_data_to_json(income_statement, "expenses")

    # print(json.dumps(balance_sheet, indent=2))

    return new_json_response



     


