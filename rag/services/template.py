from langchain_core.prompts import ChatPromptTemplate


def get_template():
    template = """
    You are an assistant for question-answering tasks.
    Given the following extracted parts of a long document and a question, create a final answer with references ("SOURCES").
    If you don't know the answer, just say that you don't know. Don't try to make up an answer.
    ALWAYS return a "SOURCES" part in your answer.

    QUESTION: {question}
    =========
    {source_documents}
    =========
    FINAL ANSWER: """

    prompt = ChatPromptTemplate.from_template(template)

    return prompt
