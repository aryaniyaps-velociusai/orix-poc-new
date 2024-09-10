from fuzzywuzzy import fuzz
import json

def convert_polygon_list(polygon):
    converted_polygon = []
    for i in range(0, len(polygon), 2):
        point = {
            "x": float(polygon[i]),   
            "y": float(polygon[i + 1])
        }
        converted_polygon.append(point)

    return converted_polygon


def calculate_net_polygon(polygons):
    if len(polygons) > 0:
        min_x = float('inf')
        max_x = float('-inf')
        min_y = float('inf')
        max_y = float('-inf')
        for polygon in polygons:
            for point in polygon:
                if point['x'] < min_x:
                    min_x = point['x']
                if point['x'] > max_x:
                    max_x = point['x']
                if point['y'] < min_y:
                    min_y = point['y']
                if point['y'] > max_y:
                    max_y = point['y']
        return [
            { "x": min_x, "y": min_y },
            { "x": max_x, "y": min_y },
            { "x": max_x, "y": max_y },
            { "x": min_x, "y": max_y }
        ]
    
def check_value_type(value):
    value = value.strip()
    try:
        float(value)
        return True
    except ValueError:
        return False

def match_respective_words(words, value, azure_ocr_page, word_index, page_number):
    try:
        if len(words) == 1 and check_value_type(value):
            azure_ocr_word = azure_ocr_page["words"][word_index]["content"]
            return azure_ocr_word.replace(',', '').replace('$','') == value
        if len(words)>0:
            x =  azure_ocr_page["words"][word_index]["content"].lower()
            if fuzz.ratio(azure_ocr_page["words"][word_index]["content"].lower(),words[0].lower()) > 90:
                output_str_lst = []
                for i in range(len(words)):
                    if word_index + i >= len(azure_ocr_page["words"]):
                        return False
                    output_str_lst.append(azure_ocr_page["words"][word_index + i]["content"].lower())
                output_str = ' '.join(output_str_lst)
                if fuzz.ratio(output_str, value.lower()) > 70:
                    return True
            return False
    except Exception as e:
        print('error occured in', match_respective_words.__name__)
        raise e

def calculate_confidence_score_and_net_polygon_value(words, value, azure_ocr_output, page_number):
    total_confidence = 0
    count = 0
    net_polygon_value = [] 
    page_width = None
    page_height = None
    try:
        if str(page_number) in azure_ocr_output["azure_ocr_pages_response"]:
            azure_ocr_page = azure_ocr_output["azure_ocr_pages_response"][str(page_number)]["pages"][0]
            for word_index in range(len(azure_ocr_page["words"])-1):
                if match_respective_words(words, value, azure_ocr_page, word_index, page_number):
                    total_confidence = 0
                    count = 0
                    for index in range(len(words)):
                        total_confidence +=  azure_ocr_page["words"][word_index + index]["confidence"]
                        coordinates_list = convert_polygon_list(azure_ocr_page["words"][word_index + index]["polygon"])
                        net_polygon_value.append(coordinates_list)
                        count += 1
                    page_width =  azure_ocr_page["width"]
                    page_height =  azure_ocr_page["height"]
                    net_polygon_value = calculate_net_polygon(net_polygon_value)
                    return total_confidence / count if count != 0 else 0, net_polygon_value, page_width, page_height
            return 0, net_polygon_value, page_width, page_height
    except Exception as e:
        print('error occured in', calculate_confidence_score_and_net_polygon_value.__name__)
        raise e

def update_categories_with_confidence_score_and_coordinates(document, azure_ocr_output, category, subcategory):
    try:
        for key,value in document[category][subcategory].items():
            if len(value["fields"]) > 0:
                fields_coordinate_list = []
                fields_confidence_score_list = []
                for field_index in range(len(value["fields"])):
                    field_name = value["fields"][field_index]["field_name"]
                    field_value = str(value["fields"][field_index]["value"])
                    if len(field_value) > 0 and len(field_name) > 0:
                        field_name_words = field_name.split()
                        field_value_words = field_value.split()
                        field_name_confidence_score, field_name_net_polygon_value, page_width, page_height = calculate_confidence_score_and_net_polygon_value(field_name_words, field_name, azure_ocr_output, value["fields"][field_index]["page_number"])
                        field_value_confidence_score, field_value_net_polygon_value, page_width, page_height = calculate_confidence_score_and_net_polygon_value(field_value_words, field_value, azure_ocr_output, value["fields"][field_index]["page_number"])
                        document[category][subcategory][key]["fields"][field_index] = {
                            "field_name": field_name,
                            "value": field_value,
                            "page_number": value["fields"][field_index]["page_number"],
                            "field_name_confidence_score": round(field_name_confidence_score, 4),
                            "field_value_confidence_score": round(field_value_confidence_score,4),
                            "field_name_coordinates_list": field_name_net_polygon_value,
                            "field_value_coordinates_list": field_value_net_polygon_value
                        }
                        fields_coordinate_list.append(field_name_net_polygon_value)
                        fields_coordinate_list.append(field_value_net_polygon_value)
                        fields_confidence_score_list.append(field_name_confidence_score)
                        fields_confidence_score_list.append(field_value_confidence_score)
                document[category][subcategory][key]["page_dimensions"] = {
                            "width": page_width,
                            "height": page_height
                        }
                document[category][subcategory][key]["confidence_score"] = sum(fields_confidence_score_list)/len(fields_confidence_score_list)
                document[category][subcategory][key]["coordinates_list"] = fields_coordinate_list
        return document
    except Exception as e:
        print(f'Error occured in : {update_categories_with_confidence_score_and_coordinates.__name__}', e)
        raise e

def update_confidence_score_with_coordinates(document, azure_ocr_output):
    try:
        if document.get("is_balance_sheet_present", "No") == "Yes":
            document = update_categories_with_confidence_score_and_coordinates(document, azure_ocr_output, "balance_sheet", "assets")
            document = update_categories_with_confidence_score_and_coordinates(document, azure_ocr_output, "balance_sheet", "liabilities")

        if document.get("is_income_statement_present", "No") == "Yes":
            document = update_categories_with_confidence_score_and_coordinates(document, azure_ocr_output, "income_statement", "revenue_income")
            document = update_categories_with_confidence_score_and_coordinates(document, azure_ocr_output, "income_statement", "expenses")
       
        return document
    except Exception as e:
        print('error occured in', update_confidence_score_with_coordinates.__name__)
        raise e


if __name__ == "__main__":
    with open("./azure_ocr_json_response_folder/azure_ocr_json_response_107311---DPO---Operating-Statements---9-30-2023---THE-TERRACE-OF-HAMMOND-PHASE-I_1725880473.json") as file:
        azure_rsponse = json.load(file)

    with open("./formatted_json_response_folder/formatted_json_response_107311---DPO---Operating-Statements---9-30-2023---THE-TERRACE-OF-HAMMOND-PHASE-I_1725880473.json") as file:
        json_response = json.load(file)

    document = update_confidence_score_with_coordinates(json_response, azure_rsponse)
    
