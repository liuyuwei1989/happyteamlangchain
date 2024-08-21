from typing import List

import langchain
from langchain.agents import initialize_agent, AgentType
from langchain.chains import LLMChain
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (ChatPromptTemplate, SystemMessagePromptTemplate,
                                    HumanMessagePromptTemplate, PromptTemplate, FewShotPromptTemplate,
                                    MessagesPlaceholder)
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI, OpenAI
from langchain_core.pydantic_v1 import BaseModel, Field


def test_messages():
    llm = ChatOpenAI(base_url="https://one.aiskt.com/v1")
    chat_template = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template("You are a Jira generator, designed to create Jira tasks based on requirements. "
                                                  "The Jira task should include the sections: What, Why, How, and Acceptance Criteria. The requirement is "),
        HumanMessagePromptTemplate.from_template("{input}")
    ])

    chain = LLMChain(llm=llm, prompt=chat_template)
    # chat_template | llm
    res = chain.invoke(input={
        'Add a new column labeled "NOV" (Net Present Value) to the table in the dashboard feature of the EWT system.'
    })
    print(res["text"])

if __name__ == '__main__':
    langchain.verbose = False
    langchain.debug = False
    test_messages()