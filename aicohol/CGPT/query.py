import os

os.environ["OPENAI_API_KEY"] = "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"

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAI as OpenAI
from openai import OpenAI as OpenAI2
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.retrieval_qa.base import RetrievalQA

current_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(current_dir, "../db/data/log.txt")
persist_directory = os.path.join(current_dir, "../db/db")

embedding = OpenAIEmbeddings()
client = OpenAI2(api_key="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")


def get_info_from_db(query):
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})

    qa_chain = RetrievalQA.from_chain_type(
        llm=OpenAI(),
        chain_type="stuff",
        retriever=retriever,
    )

    llm_response = qa_chain.invoke(query)
    return llm_response["result"]


def recommend(query):
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)
    retriever = vectordb.as_retriever(search_kwargs={"k": 2})

    qa_chain = RetrievalQA.from_chain_type(
        llm=OpenAI(temperature=0),
        chain_type="stuff",
        retriever=retriever,
    )

    query = (
        "백틱 세 개로 구분된 문장을 분석해서 관련된 정보를 알려줘.\
            만약 분석할 수 없다면, 단 하나의 어떤 술과 관련된 정보를 추천해줘.\
            \
            ```"
        + query
        + "```"
    )

    llm_response = qa_chain.invoke(query)
    save_to_txt(llm_response["result"])
    return llm_response["result"]


def save_to_txt(log):
    # 로그 txt 파일에 저장
    with open(log_dir, "a") as file:
        file.write(log + "\n")


def reference():
    with open(log_dir, "r") as file:
        refer = file.read()

    query = client.chat.completions.create(
        model="ft:gpt-3.5-turbo-0125:personal::9W1oRdbd",
        messages=[
            {
                "role": "assistant",
                "content": "백틱 세개로 구분된 문장을 요약해서 설명해주세요. \
                    ```"
                + refer
                + "```",
            }
        ],
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0,
    )
    response = query.choices[0].message.content
    return response


def reference_recommend(query):
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)
    retriever = vectordb.as_retriever(search_kwargs={"k": 2})

    with open(log_dir, "r") as file:
        refer = file.read()

    qa_chain = RetrievalQA.from_chain_type(
        llm=OpenAI(temperature=0, max_tokens=1024),
        chain_type="stuff",
        retriever=retriever,
    )

    query = (
        "백틱 세 개로 구분된 문장은 술과 관련된 정보를 추천해달라는 의미입니다.\
        술과 관련된 어떤 키워드를 찾을 수 없다면, 단 하나의 임의의 술에 대한 정보로 추천해주세요.\
        또한 백틱 2개로 구분된 문장은 이제까지 추천을 받았던 술들에 대한 정보입니다. 이 정보가 의미가 있다면, \
        해당 정보도 답변에 요약해서 넣어주세요.\
        최종적으로, 모든 답변은 문장으로 끝나야합니다.\
            ```"
        + query
        + "``` ``"
        + refer
        + "``"
    )

    llm_response = qa_chain.invoke(query)
    save_to_txt(llm_response["result"])
    return llm_response["result"]


def prompt_research(prompt):
    # 프롬프트 프로그래밍과 openai api를 통해 사용자 쿼리 분석
    query = client.chat.completions.create(
        model="gpt-3.5-turbo-0613",
        messages=[
            {
                "role": "assistant",
                "content": '백틱 세 개로 구분된 문장을 분석해주세요.\
                    만약 문장이 "술을 추천해줘"와 같은 의미를 가진다면 1,\
                    문장이 "지금까지 추천해준 술들을 알려줘"와 같은 의미를 가진다면 2,\
                    문장이 "지금까지 추천해준 술들이랑 비슷한 술을 추천해줘"와 같은 의미를 가진다면 3,\
                    앞의 3가지 문장과 같은 의미를 가지지 않는다면 4로 답변해주세요\
                    ```'
                + prompt
                + "```",
            }
        ],
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0,
    )
    res = query.choices[0].message.content
    return int(res)
