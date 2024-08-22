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
    # 简单需求
    # context = "给应用新增date字段。并输出这个需求的总览Jira（类型为sprint或者spike，sprint为开发时间容易确定的类型，spike为开发时间不容易确定的类型）"
    # 需求优化这个感觉可以和chain1并在一起
    # prompt_1 = "帮我分析需求：{context}，如果太过于简单请帮我丰富它的内容"

    # 完整需求
    context = "给应用新增date字段，包括UI，后端和数据库，并且每隔5分钟更新一次。并输出这个需求的总览Jira（类型为sprint或者spike，sprint为开发时间容易确定的类型，spike为开发时间不容易确定的类型）"
    prompt_1 = "帮我分析需求：{context}"
    prompt1 = PromptTemplate.from_template(prompt_1)
    chain = prompt1 | model | StrOutputParser()
    res = chain.invoke({"context": context})
    print("主需求")
    print(res)
    print()
    prompt_2 = ("{context}，请根据上文内容分析需要创建哪一些相应的Jira任务，"
                "并把每个任务及其各自相关的What，How，Why，Accept Criteria等信息按：任务1...任务2...这样的形式输出出来")
    prompt2 = PromptTemplate.from_template(prompt_2)
    chain2 = prompt2 | model | StrOutputParser()
    res2 = chain2.invoke({"context": res})
    print("子需求")
    print(res2)


if __name__ == '__main__':
    langchain.verbose = True
    langchain.debug = False
    create_chain()
