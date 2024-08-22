from typing import List

import langchain
from langchain.agents import initialize_agent, AgentType
from langchain.chains import LLMChain
from langchain.chains.summarize.refine_prompts import prompt_template
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
from langchain_core.runnables import (
    RunnableLambda,
    ConfigurableFieldSpec,
    RunnablePassthrough,
)


# class Chain:
llm = ChatOpenAI(base_url="https://one.aiskt.com/v1")

def create_chain(model=llm, prompt_1='', prompt_2='', context=''):
    # Create an user story
    # context = "I want to be able to easily create and track my wish lists on a retail website " \
    # "so that I can save products I'm interested in for later purchase and easily share my lists with friends and family."
    # 需求优化这个感觉可以和chain1并在一起
    # prompt_1 = "Analyze requirement：{context}，and enrich with additional context"

    # 完整需求
    context = "As a frequent online shopper," \
              " I want to be able to easily create and track my wish lists on a retail website " \
              "so that I can save products I'm interested in for later purchase and easily share my lists with friends and family." \
              "Create a jira user story with enough detailed description" \
              "Jira type:story, task, spike, sub-task"
    prompt_1 = "analyze the requirement：{context},and enrich with additional context"
    prompt1 = PromptTemplate.from_template(prompt_1)
    chain = prompt1 | model | StrOutputParser()
    res = chain.invoke({"context": context})
    print("User Story")
    print(res)
    print()
    prompt_2 = ("{context}，creating tasks throughout the development process based the user story"
                " involves breaking down the high-level functionality or requirement into smaller, "
                "actionable steps that can be completed by developer and for tester."
                "Create task with What，How，Why，Accept Criteria with：task1...task2..."
                "Create test scope and test case for tester with: Test Case")
    prompt2 = PromptTemplate.from_template(prompt_2)
    chain2 = prompt2 | model | StrOutputParser()
    res2 = chain2.invoke({"context": res})
    print("Tasks")
    print(res2)


if __name__ == '__main__':
    langchain.verbose = True
    langchain.debug = False
    create_chain()
