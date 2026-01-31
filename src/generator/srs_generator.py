from google import genai
from dotenv import load_dotenv
import os
load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))

user_input=input("enter the requirement :")

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=f'''You are a Software Requirements Engineer experienced in Agile methodology by default but if user is mentioning for IEEE format then give in IEEE format.

            Generate a Extensive Software Requirements Specification (SRS) document in given format for the following system:
            [Insert Project Title & Short Description Here]

            Follow respective principles (iterative development, customer focus, adaptability).

            The SRS should be clear, structured, and suitable for academic submission and real-world development.

            {user_input}

            Include the following sections:

            1. Introduction

            Purpose of the document

            Scope of the system

            Definitions, acronyms, and abbreviations

            References
            
            2. Agile Overview

            Agile approach used (Scrum / Kanban / Hybrid)

            Product vision

            Stakeholders

            Agile roles (Product Owner, Scrum Master, Development Team)

            3. User Personas

            Description of different user types

            4. Product Backlog (User Stories)

            User stories in the format:
            As a [user], I want [feature], so that [benefit]

            Priority (High / Medium / Low)

            Acceptance criteria for each user story

            5. Functional Requirements

            Derived from user stories

            Clearly numbered and traceable

            6. Non-Functional Requirements

            Performance

            Security

            Usability

            Scalability

            Reliability

            7. Sprint Planning Overview

            Sprint duration

            Sample sprint backlog

            Release planning summary

            8. System Constraints and Assumptions

            Technical constraints

            Business constraints

            Assumptions

            9. Requirement Traceability Matrix (RTM)

            Mapping user stories to functional requirements

            10. Future Enhancements

            Features planned for later iterations

            Use simple language, bullet points, and tables where appropriate.
            Do not include UML diagrams unless explicitly asked.

            Ensure the output follows an Agile mindset, not a traditional waterfall SRS.''')


print(response.text if hasattr(response, 'text') else str(response))