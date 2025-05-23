import openai
from pathlib import Path
import pandas as pd

CATEGORIES = ["Download", "Clean", "Comments", "Caption", "Figure", "Sentence", "Total"]

### READING IN ###

#get key
with open('key.txt', 'r') as file:
    my_key = file.read().strip()

#reads in python data cleaning file as string so api can proccess
def read_python_file():
    file_path = Path(__file__).parent.parent / "rep/data_cleaning.py"
    with open(file_path, "r", encoding="utf-8") as f:
        code_text = f.read()
    return code_text

#reads in quarto paper file as string so api can proccess
def read_paper_file():
    file_path = Path(__file__).parent.parent / "rep/paper/paper.qmd"
    with open(file_path, "r", encoding="utf-8") as f:
        paper_text = f.read()
    return paper_text

#reads in rubric for code
def read_code_rubric():
    file_path = Path(__file__).parent / "rubric/code_rubric.txt"
    with open(file_path, "r", encoding="utf-8") as f:
        rubric_text = f.read()
    return rubric_text

#reads in rubric for paper
def read_paper_rubric():
    file_path = Path(__file__).parent / "rubric/paper_rubric.txt"
    with open(file_path, "r", encoding="utf-8") as f:
        rubric_text = f.read()
    return rubric_text

### GRADING FILES ###
#grade code
def grade_code(code, rubric):
    client = openai.OpenAI(api_key = my_key)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", 
             "content": "You are a TA grading a Python assignment. Use the rubric to assign grades and write brief comments. "
                "Be consistent, objective, and concise. Only use the rubric criteria."
            },
            {"role": "user",
             "content": f"""
                code: {code}
                rubric: {rubric}
                For each category, return first the rubric category, the score and a comment of your justification each seperated by a semicolon.
                To seperate categories use "\n\n". """
            }
        ]
    )
    return response.choices[0].message.content

#grade paper
def grade_paper(paper, rubric):
    client = openai.OpenAI(api_key = my_key)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", 
             "content": "You are a TA grading a visualization assignment. Use the rubric to assign grades and write brief comments. "
                "Be consistent, objective, and concise. Only use the rubric criteria."
            },
            {"role": "user",
             "content": f"""
                paper: {paper}
                rubric: {rubric}
                For each category, return first the rubric category, the score and a comment of your justification each seperated by a semicolon.
                To seperate categories use "\n\n". """
            }
        ]
    )
    return response.choices[0].message.content

### OUTPUTTING RESULTS ###
#helper function to format result
def get_data(response):
    lines = response.strip().split("\n\n")
    data = [line.split(";") for line in lines]
    data = [[col.strip() for col in row] for row in data]
    return data

#putting singular response into a csv
def to_response_csv(response):
    #format
    data = get_data(response)

    # Create DataFrame
    df = pd.DataFrame(data, columns=["Category", "Grade", "Comment"])
    df["Grade"] = df["Grade"].astype(int)

    #save response
    file_path = Path(__file__).parent / "output/response.csv"
    df.to_csv(file_path, index = False)

#instantiates hitsory csv if needed
def instantiate_csv():
    dic = dict()
    for category in CATEGORIES:
        dic[category] = []
    file_path = Path(__file__).parent / "output/history.csv"
    df = pd.DataFrame(dic)
    df.to_csv(file_path, index = False)

#updates history for ratings in each category
def update_history(response):
    file_path = Path(__file__).parent / "output/history.csv"
    df = pd.read_csv(file_path)
    df = df.to_dict(orient = 'list')

    data = get_data(response)
    total = 0
    for category in data:
        title = category[0]
        score = int(category[1])

        df[title].append(score)
        total += score
    df["Total"].append(total)

    df = pd.DataFrame(df)
    df.to_csv(file_path, index = False)

#gets five entries for history
def get_five_history(code, paper, code_rubric, paper_rubric):
    for i in range(5):
        paper_response = grade_paper(paper, paper_rubric)
        code_response = grade_code(code, code_rubric)
        response = code_response + "\n\n" + paper_response
        update_history(response)


if __name__ == "__main__":
    #instantiate history file if needed
    instantiate_csv()
    
    #reads in the files needed
    code = read_python_file()
    paper = read_paper_file()
    code_rubric = read_code_rubric()
    paper_rubric = read_paper_rubric()

    #grades files & gets responses
    paper_response = grade_paper(paper, paper_rubric)
    code_response = grade_code(code, code_rubric)
    response = code_response + "\n\n" + paper_response

    #outputs responses to csv and updates
    update_history(response)
    to_response_csv(response)

    #get_five_history(code, paper, code_rubric, paper_rubric)
 
