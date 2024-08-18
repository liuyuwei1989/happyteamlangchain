import langchain
from langchain.agents import initialize_agent, AgentType
from langchain.chains import LLMChain
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (ChatPromptTemplate, SystemMessagePromptTemplate,
                                    HumanMessagePromptTemplate, PromptTemplate, FewShotPromptTemplate)
from langchain_openai import ChatOpenAI, OpenAI


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


if __name__ == '__main__':
    langchain.verbose = True
    langchain.debug = True
    test_agents()
