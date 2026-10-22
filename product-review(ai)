import os
import re
from getpass import getpass
from groq import Groq
from pypdf import PdfReader
import wikipedia
client = None


def ask(user_prompt,temp=1.0):
        global client
        if client is None:
            # Prefer an environment variable; ask privately if one is not configured.
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                try:
                    api_key = getpass("Enter your Groq API key: ").strip()
                except (EOFError, OSError):
                    print("Could not read the Groq API key.")
                    return None
            if not api_key:
                print("A Groq API key is required to make requests.")
                return None
            client = Groq(api_key=api_key)

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
            if not respo.choices or respo.choices[0].message.content is None:
                print("Groq returned an empty response.")
                return None
            return respo.choices[0].message.content
        except Exception as error:
            # Catch provider, authentication, and connection errors at the request boundary.
            print(f"Groq request failed: {error}")
            return None
products={"sony digi handicam",
          "apple airpods pro",
          "nokia 3310 cellphone",}
'''
for product in products:
    prompt=f"Write a product description for {product} in a specific format.Format:Product name:<product name>, Star rating:<rating in stars out of 5 in form of emojis>,PROS:<list of pros>,CONS:<list of cons>, user review. Make sure this is well formatted with emojis,highlighted text and looks eye catchy.No need to be positive make the more human ,critical and make sure each product has a different tone  and writing style."
    print(ask(prompt))
'''

def interview(topic,difficulty,n,temp=1.0):
    if n < 1:
        print("The number of questions must be at least 1.")
        return
    for _ in range(n):
        question = ask(f"You are an interviewer who must ask a question on the topic {topic}.make sure that the question is unique and different and as per the difficulty level {difficulty}.")
        if question is None:
            continue
        print(question)
        try:
            answer = input("enter your answer:")
        except (EOFError, KeyboardInterrupt):
            print("Interview ended before an answer was entered.")
            return
        rating = ask(f"You are an unbiased interviewer who asked the question {question} to the interviewee and recieved the answer {answer}.be completely honest and rate this answer out of 10 with feedback and stuff.the chain of thoughts should be :step1-generate an ideal answer for the question,step2-compare it with the given answer and geenrate and display a rating out of 10.stpe3-provide feedback for theanswer and suggest improvements.")
        if rating is not None:
            print(rating)
'''
interview("ai")
'''

def newinterview(topic,difficulty,n,temp=1.0):
    if n < 1:
        print("The number of questions must be at least 1.")
        return
    average = 0
    valid_ratings = 0
    for _ in range(n):
        question = ask(f"You are an interviewer who must ask a question on the topic {topic}.make sure that the question is unique and different and as per the difficulty level {difficulty}.")
        if question is None:
            continue
        print(question)
        try:
            answer = input("enter your answer:")
        except (EOFError, KeyboardInterrupt):
            print("Interview ended before an answer was entered.")
            break
        rating = ask(f"As an interviewer who has recieved and answer {answer} to the question {question} give a strictly numerical one number answer rating out of 10.(Example:(2),(6)etc.).Keep it in mind only the numerical rating is needed nothing else no other text.")
        if rating is None:
            continue
        # Parse only a numeric score; never execute text returned by the model.
        match = re.search(r"\b(10|[0-9])(?:\.\d+)?\b", rating)
        if match is None:
            print(f"Could not read a numeric rating from: {rating}")
            continue
        score = float(match.group(0))
        if not 0 <= score <= 10:
            print(f"Rating is outside the 0-10 range: {score}")
            continue
        average += score
        valid_ratings += 1
    if valid_ratings:
        print(average / valid_ratings)
    else:
        print("No valid ratings were received.")
'''
newinterview("school","easy",2)
'''




def resume():
    try:
        pdfr=PdfReader(r"c:\Users\tweet\Downloads\Administrative-Assistant-Resume-2-converted.pdf")
        text=""
        for page in pdfr.pages:
            text += page.extract_text() or ""
    except Exception as error:
        print(f"Could not read or extract the resume PDF: {error}")
        return
    okay=ask(f"format the resume {text} is a strictyle structed format by extracting the specified details only.The format is:(Name:(given name),Prior experience:(given experience),Skills:(given skills),Education:(given educational qualifications),Contact info:(given contact details).Make to only write in this format and not write anything except this .Keep it short and concise.Return this in a json format.)")
    if okay is None:
        return
    match=ask(f"Match the resume {okay} with the resume of an ideal Junior ML Engineer and provide a numerical rating out of 10.Also give a justified reason for your rating.")
    print(okay,match if match is not None else "Resume comparison could not be completed.")
'''
resume()
'''

def article():
    page = r"Science is a systematic discipline that builds and organises knowledge in the form of testable explanations about nature and society.[1]: 49–71 [2] It is driven by the scientific method: an empirical cycle that typically involves making observations, producing hypotheses, testing them with evidence, and drawing conclusions. Science encompasses this process and the body of knowledge it produces, which the scientific community continuously challenges, validates, and organises.Modern science is typically divided into two – or three – major branches:[3] the natural sciences, which study the physical world, and the social sciences, which study individuals and societies.[4][5] While referred to as the formal sciences, the study of logic, mathematics, and theoretical computer science are typically regarded as separate because they rely on deductive reasoning instead of the scientific method as their main methodology.[6][7][8][9] Meanwhile, applied sciences are disciplines that use scientific knowledge for practical purposes, such as engineering and medicine.[10][11][12]The history of science spans the majority of the historical record, with the earliest identifiable predecessors to modern science dating to the Bronze Age in Egypt and Mesopotamia (c. 3000–1200 BCE). Their contributions to mathematics, astronomy, and medicine entered and shaped the Greek natural philosophy of classical antiquity and later medieval scholarship, whereby formal attempts were made to provide explanations of events in the physical world based on natural causes; while further advances, including the introduction of the Hindu-Arabic numeral system, were made during the Golden Age of India and Islamic Golden Age.The recovery and assimilation of Greek works and Islamic inquiries into Western Europe during the Renaissance revived natural philosophy, which was later transformed by the Scientific Revolution that began in the 16th century[18] as new ideas and discoveries departed from previous Greek conceptions and traditions. The scientific method soon played a greater role in the acquisition of knowledge, and in the 19th century, many of the institutional and professional features of science began to take shape,[19][20] along with the changing of \"natural philosophy\" to \"natural science\".[21] New knowledge in science is advanced by research from scientists who are motivated by curiosity about the world and a desire to solve problem. Contemporary scientific research is often highly collaborative and is frequently carried out by teams in academic and research institutions,[24] government agencies, and companies.[25] At the same time, many major advances—particularly in fundamental science—have come from individual researchers and are widely recognised through major international awards such as the Nobel Prize. The practical results of scientific work have led to the emergence of science policies that seek to prioritise the responsible development of commercial products, health care, public infrastructure, environmental protection, and defense capabilities."
    extract=ask(f"from the article {page} extract the key concepts.Display these concepts keepng them crisp,short and precise. Write in neat and structured format with spaces and points.")
    if extract is None:
        return None
    lesson=ask(f"From the concepts {extract} create a lesson.Write in neat and structured format with spaces and points.")
    if lesson is None:
        return None
    quiz=ask(f"From the lesson {lesson} generate an interactive quiz.Write in neat and structured format with spaces and points..")
    if quiz is None:
        return None
    summary=ask(f"from the key concepts {extract}, lesson {lesson},quiz{quiz} prepare a lesson summary. The summary should be useful and short.Write in neat and structured format with spaces and points..")
    if summary is None:
        return None
    html_=ask(f"Return a well formatted complete html with 4 sections Extract, Lesson, Quiz and Summary  along with their content as given . (Extract:{extract}),(Lesson:{lesson}),(quiz:{quiz}) and (Summary:{summary}).make sure that both the headings and the contents is returned.shorten up the content to less than 1500 tokens.")
    if html_ is None:
        return None
    try:
        with open("chehak.txt","a", encoding="utf-8") as output_file:
            output_file.write(html_)
    except OSError as error:
        print(f"Could not write the article output: {error}")
        return None
    #return extract,lesson,quiz,summary
    return html_
print(article())

def fact_checker(runs=5):
    if runs < 1:
        print("The number of checks must be at least 1.")
        return
    try:
        statement=input("Enter a statement: ")
    except (EOFError, KeyboardInterrupt):
        print("Fact-check cancelled.")
        return
    l=[]
    for i in range (runs):
        prompt=ask(f"For the given statement{statement} check whether the claim made is correct or not.Check the answer factually and only return it in yes or no format.Example:((claim):(yes/no)).")
        if prompt is not None:
            l.append(prompt)
    count=0
    valid_count=0
    for i in l:
        if i.strip().upper() in ("YES", "NO"):
            valid_count += 1
        if i.strip().upper()=="YES":
             count+=1
    if valid_count == 0:
        print("No valid fact-check responses were received.")
    elif count>=max(1, valid_count-1):
        print("The statement is factually correct")
    else:
        print("To be checked")
'''
print(fact_checker())
'''
