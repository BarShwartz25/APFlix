import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    user_checks = event['user_checks']
    score_limit = event['score_limit']
    text = event['user_input']
    comprehend = boto3.client("comprehend",region_name = "us-east-1")
    pii_detection_string_output = (json.dumps(comprehend.detect_pii_entities(Text = text , LanguageCode = 'en'), sort_keys=True, indent= 4))

    pii_json = json.loads(pii_detection_string_output)
    detected_types = []
    for element in pii_json["Entities"]:
        if element["Score"] > float(score_limit):
            print(element["Type"])
            if element["Type"] not in detected_types:
                if element["Type"] in user_checks:
                    detected_types.append(element["Type"])

    print(detected_types)
    
   # print(response)
    return {
        'statusCode': 200,
        'body': detected_types
    }
