import os
import json
from getpass import getpass
from groq import Groq
from pypdf import PdfReader
import wikipedia

# Prefer the environment variable; otherwise request the key without echoing it.
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    try:
        api_key = getpass("Enter your Groq API key: ").strip()
    except (EOFError, OSError):
        api_key = None

client = Groq(api_key=api_key) if api_key else None


def ask(user_prompt,temp=1.0):
        if client is None:
            print("Add a new Groq API key to API_KEY or set GROQ_API_KEY.")
            return None

        msg=([
            {
                "role": "system",
                "content": "Assume the role of an AI assistant who is demure and polite and answers questions respectfully without being morally judgy or diplomatic"
            } 
        ])
        
        msg+= [{
                        "role": "user",
                        "content": user_prompt
                    }]
        try:
            respo = client.chat.completions.create(
            model="allam-2-7b",messages=msg,temperature=temp)
            return respo.choices[0].message.content
        except Exception as error:
            # Network, authentication, and rate-limit errors should not crash the script.
            print(f"Groq request failed: {error}")
            return None

def fact_checker(statement,runs=3):
    if runs < 1:
        raise ValueError("runs must be at least 1")

    yes_count = 0
    valid_count = 0
    for _ in range(runs):
        prompt=ask(f"""For the given statement{statement} check whether the claim made is correct or not.Check the answer factually and return the claim value in yes or no format.Also add a confidence score of the answer in percentage format between 1% to 100%.Moreover suggest two credible sources for factually checking the statement.Return this information always only in json format.Example:(("claim":"yes/no"),("score":"30%")),(("source":"wikipedia.com,encylclopledia.com")).You are strictly instructed to not write anything else except this format.Only and only give json format responses.""")
        if prompt is None:
            continue
        print("reposnse is:",prompt)

        try:
            result = json.loads(prompt)
        except json.JSONDecodeError as error:
            print(f"Could not parse the fact-check response as JSON: {error}")
            continue

        if not isinstance(result, dict) or not isinstance(result.get("claim"), str):
            print('Fact-check response is missing a string "claim" field.')
            continue

        valid_count += 1
        print("answer:",result["claim"])
        if result["claim"].strip().upper() == "YES":
            yes_count += 1

    if valid_count == 0:
        print("No valid fact-check responses were received.")
    elif yes_count >= max(1, valid_count - 1):
        print("The statement is factually correct")
    else:
        print("To be checked")
'''
fact_checker()
'''
def articlefactfinder():
    article='''Amer Fort: A Blend of Rajput and Mughal Architecture.Amer Fort, also known as Amber Fort, is a blend of Rajput and Mughal architecture, showcasing the architectural prowess of Rajasthan. The fort is a UNESCO World Heritage Site and is a major tourist attraction in Jaipur.Amer Fort is located in Amer, Rajasthan, India, near Jaipur, approximately 11 kilometers from the capital city.The fort was constructed by Raja Man Singh I in 1592 CE and expanded by successive Kachhwaha rulers.The fort is known for its large ramparts, series of gates, and cobbled paths, overlooking Maota Lake. It features the Diwan-e-Aam, Diwan-e-Khas, Sheesh Mahal, Jai Mandir, and Sukh Niwas. Amer Fort was the capital of the Dhundhar state before Jaipur was built and has a rich history involving the Meenas and Rajputs.UNESCO World Heritage  Amer Fort was declared a UNESCO World Heritage Site in 2013, highlighting its cultural and historical importance. Amer Fort is a must-visit for those interested in Rajasthan's history, architecture, and culture. The fort's blend of Rajput and Mughal styles, along with its historical significance, makes it a unique and fascinating destination for visitors.'''
    facts=ask(f"From the article {article} extracts all the important facts and return them in ONLY AND ONLY IN JSON FORMAT. No markdown.No explanation.Example:{{facts}}.Dont add any line before or after the json.")
    if facts is not None:
        fact_checker(facts)
articlefactfinder()



def promptimprover(weakprompt,context):
    prompts=ask(f"""Rewrite the given prompt {weakprompt} based on the context {context} as a professional-grade plain text prompt adding all elements of a well formed prompt like context,instruction,formatting,constraints and examples in it.Do not add any extra formatting text or explanation text.""")
    return prompts

def promptevaluator(weakprompt,context):
    rating=ask(f"""For the prompt {weakprompt} and context {context} analyse this prompt.Rate this prompt on the basis of given parameters: (context/instruction/format/constraints/examples) out of 5.Return a final rating out of 25.Return the response strictly as a well formed json format as given.\
    Return:{{
            "context_rating": _ out of 5,
            "instruction_rating": _ out of 5,
            "format_rating": _ out of 5,
            "constraints_rating": _ out of 5,
            "examples_rating": _ out of 5,
            "Final Rating":final rating out of 25
  }}.Do not add any extra formatting text or explanation text before and after the json.""")
    return rating


test_prompts = [
    (
        "summarise this article",
        "Earthquake in japan",)]
'''       
for i,j in test_prompts:
    b=promptimprover(i,j)
    print("******************************************************************************************************************")
    print("OLD PROMPT:",i)
    print("******************************************************************************************************************") 
    print("RESPONSE OF OLD PROMPT:",ask(f"{i}{j}"))
    print("******************************************************************************************************************")
    print("NEW PROMPT IS:",b)
    print("******************************************************************************************************************")
    print("RESPONSE OF NEW PROMPT:",ask(b))
    print("******************************************************************************************************************")
    c=promptevaluator(i,j)
    print(c)
    d=json.loads(c)
    print("RATING OF THE OLD PROMPT:",d["Final Rating"])
    print("******************************************************************************************************************")
'''
