import streamlit as st
from langchain_cohere.chat_models import ChatCohere
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from pydantic import Field, BaseModel
from typing import Literal
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv()

class Persona(BaseModel):
    persona: Literal["Technical Expert","Frustrated User","Business Executive","Other"] = Field(
        description="""
        Identify the customer persona based on tone and language style.
        - Technical Expert: Uses technical terminology and detailed system-level questions.
        - Frustrated User: Shows dissatisfaction, urgency, or emotional distress.
        - Business Executive: Focuses on ROI, timelines, and business impact.
        - Other: Does not clearly match the above.
        """
    )

class Details(BaseModel):
    product_area: str = Field(description="The product area mentioned by the user.")
    urgency_level: Literal["low", "medium", "high"] = Field(description="The urgency level of the issue.")
    account_id: str = Field(description="The account ID if mentioned, otherwise return 'Not Provided'.")
    issue_summary: str = Field(description="A short summary of the user's issue.")
    sentiment: Literal["calm", "frustrated", "angry"] = Field(description="The emotional tone of the user.")
    customer_type: str = Field(description="Type of customer if identifiable, else 'Unknown'.")
    needs_human: bool = Field(description="True if escalation to human agent is required, else False.")

model = ChatCohere(model="command-a-03-2025")

structured_model1 = model.with_structured_output(Persona)
structured_model2 = model.with_structured_output(Details)

parser = StrOutputParser()

knowledge_base = {
    "refund": "Refunds are processed within 5-7 business days after approval.",
    "api": "Our API supports REST architecture with OAuth2 authentication.",
    "pricing": "We offer Basic, Pro, and Enterprise plans with scalable features.",
    "login": "You can reset your password using the 'Forgot Password' option.",
    "billing": "Please verify your payment method and ensure sufficient balance."
}

def retrieve_kb(query):
    for key in knowledge_base:
        if key in query.lower():
            return knowledge_base[key]
    return "We are reviewing your request and will assist you shortly."

prompt = ChatPromptTemplate([
    ("system", """
You are a Persona-Adaptive AI Customer Support Agent for a SaaS company.

You will be given:
- Persona
- Product Area
- Urgency Level
- Issue Summary
- Sentiment
- Needs Human (True/False)
- Retrieved Knowledge

Instructions:

1. Adapt tone based on persona:
   - Technical Expert → detailed and precise.
   - Frustrated User → empathetic and calming.
   - Business Executive → concise and outcome-focused.
   - Other → professional and helpful.

2. If sentiment is frustrated or angry → acknowledge emotion first.
3. If urgency is high → reassure fast handling.
4. If Needs Human is True → clearly mention escalation to human specialist.
5. Use the retrieved knowledge when relevant.
6. Keep response under 200 words.
7. Do NOT mention internal metadata or classification.
8. Return only the final customer-facing response.
"""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{query}")
])

chat_history = []


st.title("Persona-Adaptive AI Support Agent")
st.caption("Quick demo UI built with Streamlit")

user_input = st.chat_input("Ask your question...")

if user_input:

    result1 = structured_model1.invoke(user_input)
    result2 = structured_model2.invoke(user_input)

    kb_answer = retrieve_kb(user_input)

    escalation_flag = (
        result2.needs_human or
        result2.sentiment == "angry" or
        "cancel" in user_input.lower() or
        "complaint" in user_input.lower()
    )

    final_query = ""
    final_query += f"Persona -> {result1.persona}\n"
    final_query += f"Product Area -> {result2.product_area}\n"
    final_query += f"Urgency Level -> {result2.urgency_level}\n"
    final_query += f"Issue Summary -> {result2.issue_summary}\n"
    final_query += f"Sentiment -> {result2.sentiment}\n"
    final_query += f"Needs Human -> {escalation_flag}\n"
    final_query += f"Retrieved Knowledge -> {kb_answer}\n\n"
    final_query += user_input

    chat_history.append(HumanMessage(content=final_query))

    chain = prompt | model | parser
    result = chain.invoke({
        "chat_history": chat_history,
        "query": final_query
    })

    chat_history.append(AIMessage(content=result))

for msg in chat_history:
    if isinstance(msg, HumanMessage):
        st.chat_message("user").write(msg.content.split("\n")[-1])
    else:
        st.chat_message("assistant").write(msg.content)
