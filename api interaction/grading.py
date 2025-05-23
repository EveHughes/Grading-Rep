import openai
from pathlib import Path

with open('key.txt', 'r') as file:
    my_key = file.read().strip()

def read_python_file():
    file_path = Path(__file__).parent.parent / "/data_cleaning.py"
    with open(file_path, "r", encoding="utf-8") as f:
        code_text = f.read()
    return code_text

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
                for each category, return first the score and a comment of your justification."""
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
                for each category, return first the score and a comment of your justification."""
            }
        ]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    code = read_python_file()
    paper = read_paper_file()
    code_rubric = read_code_rubric()
    paper_rubric = read_paper_rubric()
    paper_response = grade_paper(paper, paper_rubric)
    print(paper_response)

    #code_response = grade_code(code, code_rubric)
