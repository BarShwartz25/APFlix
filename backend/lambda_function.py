import json
import openai

with open('data.json' , 'r') as file:
    raw_data = file.read()
data = json.loads(raw_data)
movies_list = data['movies_list']

# TODO: Move to secret
openai.api_key = "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"

def movie_recommendation(user_input, user_engine):
    prompt = f"I want you to match a movie to a person with the next description: [" + user_input +f"]. this is the list of the movies I want you to reply with: [{', '.join(movies_list)}]. if the description part is empty or doesnt look like a logical description , do not replay with a movie name from the list."
    answer = openai.Completion.create(
        engine=user_engine, 
        prompt=prompt, 
#the longest movie name
        max_tokens=30, 
        n=1,
        stop=None,
        temperature=0
    )
    if(user_input == "" or user_input.isspace()):
        return "no movie found"
    return answer.choices[0].text.strip()

def contains_string(string , string_list):
    string = string.rstrip('.')
    matches = [s for s in string_list if s.endswith('.') and string.endswith(s.rstrip('.')) or s in string]
    return matches[0] if matches else "No answer found"

def lambda_handler(event, context):
    answer = movie_recommendation(event['user_input'] , event['user_engine'])
    response_data = contains_string(answer, movies_list)
    
    return {
        'statusCode': 200,
        'body': json.dumps(response_data)
    }
