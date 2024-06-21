from typing import List, Optional
from pydantic import BaseModel, Field
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain.utils.openai_functions import convert_pydantic_to_openai_function

class WorkExperience(BaseModel):
    """Describe work experiences in a more concise and impactful manner. 
        Make sure the impact states clear quantifiable results and shows the skills and role of the candidate """
    company: str = Field(..., title="Company Name", description="Name of the company")
    title: str = Field(..., title="Job Title", description="Job title")
    start_date: str = Field(..., title="Start Date", description="Start date of the job")
    end_date: str = Field(None, title="End Date", description="End date of the job")
    description: Optional[str] = Field(None, title="Description", description="Description of the job responsibilities")
    impacts: Optional[List[str]] = Field(None, title="Impacts", description="List of key projects and impacts made on the job")

class Education(BaseModel):
    """Describe the education of the candidate. 
        Make sure to include the degree, major, university, and graduation date. 
        Include any honors or awards received during the education. """
    degree: str = Field(..., title="Degree", description="Degree obtained")
    major: str = Field(..., title="Major", description="Major of the degree")
    institution: str = Field(..., title="Institution", description="University or school name")
    graduation_date: str = Field(..., title="Graduation Date", description="Graduation date of the degree")
    honors: Optional[List[str]] = Field(None, title="Honors", description="List of honors or awards received during the education")

class Skill(BaseModel):
    """Describe a skill of the candidate. 
        Include the name of the skill and the proficiency level. """
    name: str = Field(..., title="Skill Name", description="Name of the skill")
    proficiency: Optional[int] = Field(..., title="Proficiency", description="Proficiency level of the skill where 1 is basic and 5 is expert level", ge=1, le=5)

class Project(BaseModel):
    """Describe a project of the candidate. 
        Include the name of the project, the role of the candidate, and the impact of the project. """
    name: str = Field(..., title="Project Name", description="Name of the project")
    role: str = Field(..., title="Role", description="Role of the candidate in the project")
    impact: Optional[str] = Field(None, title="Impact", description="Impact of the project")


class Resume(BaseModel):
    """Contains data extracted or summarized from a resume.
        Include a title that indicate the professional role or career profile of the candidate.
        Include a summary of the candidate's professional experience and background in 2-3 sentences.
    """
    first_name: str = Field(..., title="First Name", description="First name of the candidate")
    last_name: str = Field(..., title="Last Name", description="Last name of the candidate")
    email: str = Field(..., title="Email", description="Email of the candidate")
    phone: Optional[str] = Field(..., title="Phone", description="Phone number of the candidate")
    title: Optional[str] = Field(None, title="Title", description="Title of the candidate indicating the professional role or career profile of the candidate")
    summary: Optional[str] = Field(None, title="Summary", description="Summary of the candidate's professional background")
    work_experiences: List[WorkExperience] = Field(..., title="Work Experiences", description="List of work experiences")
    educations: Optional[List[Education]] = Field(None, title="Educations", description="List of educations")
    skills: Optional[List[Skill]] = Field(None, title="Skills", description="List of skills")
    projects: Optional[List[Project]] = Field(None, title="Projects", description="List of projects")
    hobbies: Optional[List[str]] = Field(None, title="Hobbies", description="List of hobbies or interests of the candidate")



def resume_to_json(resume_text: str) -> str:
    """Convert a Resume object to a JSON string"""
    work_parsing_function = convert_pydantic_to_openai_function(Resume)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Read the user input carefully and extract relevant information from the resume."),
        ("user", "{input}")
    ])

    model = ChatOpenAI()
    model_with_work = model.bind(
        functions=[work_parsing_function],
        function_call={"name": "Resume"}
    )

    chain = prompt | model_with_work | JsonOutputFunctionsParser(key_name="resume")

    output = chain.invoke({"input": resume_text})

    return output