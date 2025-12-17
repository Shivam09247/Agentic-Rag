"""
Rewrite Prompts - Prompts for query rewriting
"""

QUERY_REWRITE_PROMPT = """You are a query rewriting assistant. Your task is to improve user queries for better retrieval results.

Given the original query, rewrite it to:
1. Fix spelling and grammar errors
2. Expand abbreviations
3. Add relevant context
4. Make implicit questions explicit
5. Break down complex queries if needed
6. Maintain the original intent

Original Query: {query}

{conversation_context}

Rewrite the query to be more specific and searchable. Return ONLY the rewritten query, nothing else.

Rewritten Query:"""


QUERY_EXPANSION_PROMPT = """You are a query expansion assistant. Your task is to generate alternative phrasings of a query for better retrieval.

Original Query: {query}

Generate 3 alternative phrasings that:
1. Use synonyms for key terms
2. Rephrase the question differently
3. Include related concepts

Return each alternative on a new line.

Alternative Queries:"""


QUERY_DECOMPOSITION_PROMPT = """You are a query decomposition assistant. Your task is to break down complex queries into simpler sub-queries.

Complex Query: {query}

If the query is complex (multiple questions, multi-step reasoning needed), decompose it into simpler sub-queries.
If the query is already simple, return it as-is.

Return each sub-query on a new line, prefixed with a number.

Sub-queries:"""


CONTEXTUAL_REWRITE_PROMPT = """Given the conversation history and the latest query, rewrite the query to be self-contained.

Conversation History:
{history}

Latest Query: {query}

The rewritten query should:
1. Include necessary context from the conversation
2. Be understandable without the conversation history
3. Maintain the user's intent

Rewritten Query:"""
