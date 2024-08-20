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
from langchain_core.runnables import (
    RunnableLambda,
    ConfigurableFieldSpec,
    RunnablePassthrough,
)


def test_response_from_open_ai_chat():
    llm = ChatOpenAI(base_url="https://one.aiskt.com/v1")
    res = llm.invoke("给我讲一个小马过河的故事")
    print(res.content)


def test_response_from_open_ai():
    llm = OpenAI(base_url="https://one.aiskt.com/v1/")
    res = llm.invoke("给我讲一个小马过河的故事")
    print(res)


def test_chat_models():
    llm = ChatOpenAI(base_url="https://one.aiskt.com/v1")
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant that translates {input_language} to {output_language}."),
            ("human", "{input}")
        ]
    )

    chain = prompt | llm
    res = chain.invoke({
        "input_language": "English",
        "output_language": "German",
        "input": "I love programming.",
    })

    print(res.content)


def test_messages():
    llm = ChatOpenAI(base_url="https://one.aiskt.com/v1")
    chat_template = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template("You are a helpful assistant that "
                                                  "translates {input_language} to {output_language}."),
        HumanMessagePromptTemplate.from_template("{input}")
    ])

    chain = LLMChain(llm=llm, prompt=chat_template)
    # chat_template | llm
    res = chain.invoke(input={
        "input_language": "English",
        "output_language": "中文",
        "input": "I love programming."
    })
    print(res["text"])


def test_few_shot():
    examples = [
        {"word": "big", "antonym": "saa"},
        {"word": "up", "antonym": "daa"},
        {"word": "left", "antonym": "raa"}
    ]
    example_template = """antonym for word {word} is {antonym}"""
    example_prompt = PromptTemplate(input_variables=["word"], template=example_template)
    few_shot_template = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        prefix="Flowing we know some antonym of some words, please remember those I give you, "
               "if the word I asked contains, please answer the antonym what I gave you, or you can judge by yourself:",
        suffix="So, what is the antonym for word: {input} ",
        input_variables=["input"],
        example_separator=","
    )
    prompt_text = few_shot_template.format(input="up")
    llm = ChatOpenAI(base_url="https://one.aiskt.com/v1")
    res = llm.invoke(prompt_text)
    print(res.content)


def test_two_chains():
    llm = ChatOpenAI(base_url="https://one.aiskt.com/v1")
    prompt1 = PromptTemplate.from_template(template="""
    生成一部有关于{topic}的小说大纲，小说的主角是{character}。返回的答案按照如下格式
    小说名字:《(这里放小说名字)》\n
    小说大纲: (这里放大纲)
    """)
    first_chain = prompt1 | llm | StrOutputParser()
    prompt2 = PromptTemplate.from_template("""
    你现在作为一名书评人，根据以下给定的小说简介，生成你对这部小说的评价，要包括正面的评价跟负面的评价。\n
    {description}
    """)
    second_chain = prompt2 | llm | StrOutputParser()
    overall_chain = {"description": first_chain} | second_chain
    catchphrase = overall_chain.invoke({
        "character": "冷无算",
        "topic": "校园爱情"

    })
    print(catchphrase)


def test_agents():
    llm = ChatOpenAI(base_url="https://one.aiskt.com/v1")
    tools = load_tools(["llm-math", "wikipedia"], llm=llm)
    agent = initialize_agent(tools=tools,
                             llm=llm,
                             agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION
                             )
    prompt = PromptTemplate.from_template("{country}有多少人口")
    chain = prompt | agent
    result = chain.invoke({"country": "中国"})
    print(result)


def test_chat_history():
    history = ChatMessageHistory()
    history.add_user_message("Who are you?")
    history.add_ai_message("I'm GenAI assistant")
    print(history)


def test_conversation_chain():
    # https://api.python.langchain.com/en/latest/runnables/langchain_core.runnables.history.RunnableWithMessageHistory.html
    class InMemoryHistory(BaseChatMessageHistory, BaseModel):
        """In memory implementation of chat message history."""

        messages: List[BaseMessage] = Field(default_factory=list)

        def add_messages(self, messages: List[BaseMessage]) -> None:
            """Add a list of messages to the store"""
            self.messages.extend(messages)

        def clear(self) -> None:
            self.messages = []

    # Here we use a global variable to store the chat message history.
    # This will make it easier to inspect it to see the underlying results.
    store = {}

    def get_by_session_id(session_id: str) -> BaseChatMessageHistory:
        if session_id not in store:
            store[session_id] = InMemoryHistory()
        return store[session_id]

    history = get_by_session_id("1")
    history.add_message(AIMessage(content="hello"))
    print(store)  # noqa: T201
    llm = ChatOpenAI(base_url="https://one.aiskt.com/v1")

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You're an assistant who's good at {ability}"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ])
    chain = prompt | llm
    chain_with_history = RunnableWithMessageHistory(
        chain,
        # Uses the get_by_session_id function defined in the example
        # above.
        get_by_session_id,
        input_messages_key="question",
        history_messages_key="history",
    )

    print(chain_with_history.invoke(  # noqa: T201
        {"ability": "math", "question": "What does cosine mean?"},
        config={"configurable": {"session_id": "foo"}}
    ))

    # Uses the store defined in the example above.
    print(store)  # noqa: T201

    print(chain_with_history.invoke(  # noqa: T201
        {"ability": "math", "question": "What's its inverse"},
        config={"configurable": {"session_id": "foo"}}
    ))

    print(store)  # noqa: T201


if __name__ == '__main__':
    langchain.verbose = True
    langchain.debug = False
    test_conversation_chain()
