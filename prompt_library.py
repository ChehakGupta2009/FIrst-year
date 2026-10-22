import os
import json
from collections import Counter
from groq import Groq

api_key = os.getenv("GROQ_API_KEY")
try:
    client = Groq(api_key=api_key) if api_key else None
except Exception as error:
    # Invalid client configuration should be reported when a request is attempted.
    print(f"Could not initialize the Groq client: {error}")
    client = None


def _complete(messages, temp):
    """Make one Groq request and return None when configuration or the request fails."""
    if not isinstance(temp, (int, float)) or not 0 <= temp <= 2:
        raise ValueError("temp must be a number between 0 and 2")
    if client is None:
        print("Groq API key is missing. Set the GROQ_API_KEY environment variable.")
        return None

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=temp,
        )
        return response.choices[0].message.content
    except Exception as error:
        # Keep a failed network/API request from stopping the rest of the script.
        print(f"Groq request failed: {error}")
        return None


def ask(user_prompt, temp=1.0, system_prompt=None):
    """Send a prompt using the default assistant role or a supplied system prompt."""
    system_prompt = system_prompt or "Assume the role of an AI assistant who is demure and polite and answers questions respectfully without being morally judgy or diplomatic"
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    return _complete(messages, temp)

def askas(user_prompt,role,temp=1.0):
    """Send a prompt with a system role supplied by the caller."""
    messages = [
        {"role": "system", "content": f"you are an ai assistant having the role:{role}"},
        {"role": "user", "content": user_prompt},
    ]
    return _complete(messages, temp)

def cot(problem,steps="",temp=1.0):
    """Ask for a concise, step-by-step solution to a problem."""
    prompt = f"For the problem {problem} think through it carefully and list out all the steps in less than 50 words to solve this problem in step by step format.Keep the answer crisp no starting line and final summary is required "
    return ask(prompt, temp=temp)

def fewshot(exampleList,question,temp=1.0):
    """Answer a question using the supplied examples as guidance."""
    messages = [{
        "role": "user",
        "content": f"answer the question {question}. Taking inspiration from the given examples:{exampleList}",
    }]
    return _complete(messages, temp)

def self_consistency(user_prompt,runs=5,temp=0.2):
    """Generate several answers and return the most common successful one."""
    if not isinstance(runs, int) or isinstance(runs, bool) or runs < 1:
        raise ValueError("runs must be a positive integer")

    answers=[]
    for _ in range(runs):
        answer=ask(user_prompt, temp=temp)
        if answer is not None:
            answers.append(answer)
    if not answers:
        return None, 0, []

    # Use the most frequent successful response as the consensus answer.
    best,count=Counter(answers).most_common(1)[0]
    confidence = round(count / len(answers) * 100)
    return best,confidence,answers

def askjson(paragraph,json_data,temp=1.0):
    """Extract structured data and return parsed JSON, or None if invalid."""
    prompt = f"Extract the information about the student from the given paragraph:{paragraph} and fill it in given json format :{json_data}.Make sure that the result contains only json format values and nothing else"
    response = ask(prompt, temp=temp)
    if response is None:
        return None

    try:
        return json.loads(response)
    except json.JSONDecodeError as error:
        # Model output is not guaranteed to follow the requested JSON format.
        print(f"The response was not valid JSON: {error}")
        return None

def chaining(topic,temp=0.2):
    """Run topic research, keyword extraction, and question generation in order."""
    context=ask(f"Tell me about the topic:{topic}")
    if context is None:
        return None, None, None

    highlight=ask(f"Highlight keywords from {context}")
    if highlight is None:
        return context, None, None

    questions=ask(f"generate question and answers from the {highlight}")
    return context,highlight,questions
def study_assistant(request, mode="explain"):
    """Respond in one of the supported tutoring modes."""
    if mode == "explain":
        role = "You are a patient tutor who uses simple analogies."
        prompt = f"Explain {request} to a beginner in under 100 words with one analogy."
        return ask(prompt, temp=0.5, system_prompt=role)
    elif mode == "quiz":
        questions = ask(f"Write 3 quiz questions about: {request}", temp=0.4)
        if questions is None:
            return None
        return ask(f"Add a one-line answer to each:\n{questions}", temp=0.3)
    elif mode == "decide":
        cot_prompt = f"""{request} Think step by step: Step 1: What are the key trade-offs? Step 2: What matters most for a beginner? Step 3: What would an expert recommend? Final: Give a clear yes/no recommendation."""
        return ask(cot_prompt, temp=0.5)
    elif mode == "define":
        examples = """Gradient descent: Rolling a ball downhill blindfolded hoping it finds the exit. Overfitting: Memorising every past exam but freezing when a new question appears."""
        return ask(f"Define in the same short funny style:Examples:\n{examples}\nNow define: {request}", temp=0.9)
    else:
        raise ValueError("mode must be one of: explain, quiz, decide, define")

def main():
    """Run the sample prompts; helper functions remain safe to import elsewhere."""
    json_data = '[{"studentid": null, "name": null, "subjects": []}]'
    examples = [
        ("chain-of-thought", lambda: cot("There are 50 guests and each table seats 4. How many guests are left standing, and how many tables are required?")),
        ("few-shot", lambda: fewshot("(Color:red,Personality:Angry),(Color:blue,Personality:cool)", "Describe purple's personality in this format: (color:purple,personality:_).")),
        ("self-consistency", lambda: self_consistency("Is the weather today sunny or rainy? Answer yes or no only.")),
        ("JSON extraction", lambda: askjson("Ram is a student at ABC School, where he studies English, maths, and EVS.", json_data)),
        ("prompt chain", lambda: chaining("neural networks")),
        ("tutor explain", lambda: study_assistant("neural networks", mode="explain")),
        ("tutor quiz", lambda: study_assistant("Python loops", mode="quiz")),
        ("tutor decision", lambda: study_assistant("Should I learn PyTorch or TensorFlow?", mode="decide")),
        ("tutor definition", lambda: study_assistant("loss function", mode="define")),
    ]

    for label, example in examples:
        try:
            print(f"{label}: {example()}")
        except (ValueError, TypeError) as error:
            print(f"Could not run {label}: {error}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Let users stop a long-running set of API examples cleanly.
        print("\nStopped by user.")
