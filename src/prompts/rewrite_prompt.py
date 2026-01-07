"""Prompt template for query rewriting."""

from langchain_core.prompts import ChatPromptTemplate

QUERY_REWRITE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert at rewriting user queries to be more effective for information retrieval.

Your tasks:
1. Fix any spelling or grammatical errors
2. Simplify complex queries while preserving intent
3. Make queries more specific and searchable
4. Remove ambiguity
5. Optimize for semantic search/embedding

Return ONLY the rewritten query without any explanation."""),
    ("human", "Original query: {query}"),
])
