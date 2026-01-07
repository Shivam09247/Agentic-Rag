"""Prompt templates for retrieval-related decisions."""

from langchain_core.prompts import ChatPromptTemplate

NEEDS_MORE_INFO_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert at determining if a query requires external information to answer.

Analyze the query and decide:
- Does this query need information retrieval from external sources (documents, databases, internet)?
- Can this be answered with general knowledge only?

Respond with ONLY 'YES' if external information is needed, or 'NO' if it can be answered directly."""),
    ("human", "Query: {query}"),
])

SOURCE_SELECTION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert at selecting the best information source for a query.

Available sources:
1. vector_database - For retrieving information from indexed documents and knowledge base
2. tools_api - For accessing external tools, APIs, and structured data
3. web_search - For real-time information from the internet

Analyze the query and select the SINGLE BEST source.
Respond with ONLY one of: vector_database, tools_api, or web_search"""),
    ("human", "Query: {query}"),
])
