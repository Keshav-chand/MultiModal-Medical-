from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

from app.components.llm import load_llm
from app.components.vector_store import load_vector_store

from app.config.config import HUGGINGFACE_REPO_ID,HF_TOKEN
from app.common.logger import get_logger
from app.common.custom_exception import CustomException


logger=get_logger(__name__)

CUSTOM_PROMPT_TEMPLATE = """Use the provided medical context to answer the following question. Structure your answer to include the key information available in the text, focusing on:
1. Definition/Description: What is the condition or substance?
2. Causes & Symptoms: What causes it and what are the signs?
3. Treatment & Management: How is it treated or managed?
4. Key Details: Include any important precautions, risks, prognosis, or diagnostic methods mentioned.

**If any of these details are not found in the context, do not invent them. Simply omit that part and continue with the information that is available.**

Context:
{context}

Question:
{question}

Answer:
"""

def set_custom_prompt():
    return PromptTemplate(template=CUSTOM_PROMPT_TEMPLATE,input_variables=["context","question"])

def create_qa_chain():
    try:
        logger.info("Loading vector store for context")
        db=load_vector_store()

        if db is None:
            raise CustomException("Vector store not present or empty")

        llm = load_llm()

        if llm is None:
            raise CustomException("LLM not loaded")
        
        qa_chain= RetrievalQA.from_chain_type( #building chain on the following commands
            llm=llm,
            chain_type="stuff",
            retriever=db.as_retriever(search_kwargs={'k':1}),
            return_source_documents=False,
            chain_type_kwargs={'prompt': set_custom_prompt()}
        )
        logger.info("Successfully created the qa chain")
        return qa_chain
    
    except Exception as e:
        error_message=CustomException("Failed to make a QA chain",e)
        logger.error(str(error_message))