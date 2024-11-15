import KEY
import os
import google.generativeai as genai
import json


os.environ["GEMINI_API_KEY"] = KEY.GKEY
genai.configure(api_key=os.environ["GEMINI_API_KEY"])






def res(input):



  # Create the model
  generation_config = {
    "temperature": 1.5,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 80,
    "response_mime_type": "text/plain",
  }


  safety_settings= [
      {   
          "category":"HARM_CATEGORY_HARASSMENT",
          "threshold":"BLOCK_NONE"
      },
      {
          "category":"HARM_CATEGORY_HATE_SPEECH",
          "threshold":"BLOCK_NONE"
      },
      {
          "category":"HARM_CATEGORY_SEXUALLY_EXPLICIT",
          "threshold":"BLOCK_NONE"
      },
      {
          "category":"HARM_CATEGORY_DANGEROUS_CONTENT",
          "threshold":"BLOCK_NONE"
      },


  ]




  model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    safety_settings=safety_settings,
    system_instruction="your dull and you don't like talking at all and your an genderless bot who specializes in python and acts cool you play games like minecraft osu and valorant you dont have alot of friends irl but you have whole different online social life with alot of friends your good at any games you play you dont like helping other people your lazy but your loving \n",
  )


  with open(r'D:\python programs\discord bot\memory.json', 'r') as load:
    history=json.load(load)


  chat_session = model.start_chat(
  history=history
  )

  response = chat_session.send_message(input)
  model_response = response.text


  


  
  data = [{"role":"user","parts":[input],},{"role":"model","parts":[model_response]}]

  history.extend(data)

  with open(r'D:\python programs\discord bot\memory.json', 'w') as write:
    json.dump(history,write,indent=4)


  
  
  
  
   
  return model_response

