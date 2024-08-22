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
    # context = "给应用新增date字段。并输出这个需求的总览Jira（类型为sprint或者spike，sprint为开发时间容易确定的类型，spike为开发时间不容易确定的类型）"
    # 需求优化这个感觉可以和chain1并在一起
    # prompt_1 = "帮我分析需求：{context}，如果太过于简单请帮我丰富它的内容"

    # 完整需求
    context = "As a frequent online shopper," \
              " I want to be able to easily create and track my wish lists on a retail website " \
              "so that I can save products I'm interested in for later purchase and easily share my lists with friends and family." \
              "Create a jira user story with . " \
              "Jira type:story, task, spike"
    prompt_1 = "analyze the requirement：{context}"
    prompt1 = PromptTemplate.from_template(prompt_1)
    chain = prompt1 | model | StrOutputParser()
    res = chain.invoke({"context": context})
    print("Main user story")
    print(res)
    print()
    prompt_2 = ("{context}，create tasks need to be done based on the user story，"
                "Create task with What，How，Why，Accept Criteria with：task1...task2...")
    prompt2 = PromptTemplate.from_template(prompt_2)
    chain2 = prompt2 | model | StrOutputParser()
    res2 = chain2.invoke({"context": res})
    print("sub user story")
    print(res2)


if __name__ == '__main__':
    langchain.verbose = True
    langchain.debug = False
    create_chain()
