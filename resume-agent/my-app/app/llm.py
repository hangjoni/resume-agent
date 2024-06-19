from typing import List, Optional
from pydantic import BaseModel, Field
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain.utils.openai_functions import convert_pydantic_to_openai_function

class WorkExperience(BaseModel):
    """Describe work experiences in a more concise and impactful manner. 
        Make sure the impact states clear quantifiable results and shows the skills and role of the candidate. 
        Make sure the description is stated in how it is relevant for a job as Data Scientist. """
    company: str = Field(..., title="Company Name", description="Name of the company")
    title: str = Field(..., title="Job Title", description="Job title")
    start_date: str = Field(..., title="Start Date", description="Start date of the job")
    end_date: str = Field(None, title="End Date", description="End date of the job")
    description: Optional[str] = Field(None, title="Description", description="Description of the job responsibilities")
    impacts: Optional[List[str]] = Field(None, title="Impacts", description="List of key projects and impacts made in the job")

class WorkExperienceList(BaseModel):
    """List of work experiences"""
    work_experiences: List[WorkExperience] = Field(..., title="Work Experiences", description="List of work experiences")


def resume_to_json(resume_text: str) -> str:
    """Convert a Resume object to a JSON string"""
    work_parsing_function = convert_pydantic_to_openai_function(WorkExperienceList)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Read the user input carefully and extract the work experiences from the resume"),
        ("user", "{input}")
    ])

    model = ChatOpenAI()
    model_with_work = model.bind(
        functions=[work_parsing_function],
        function_call={"name": "WorkExperienceList"}
    )

    chain = prompt | model_with_work | JsonOutputFunctionsParser(key_name="work_experiences")

    output = chain.invoke({"input": resume_text})

    return output