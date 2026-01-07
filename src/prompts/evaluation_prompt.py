"""Prompt templates for answer generation and evaluation."""

from langchain_core.prompts import ChatPromptTemplate

ANSWER_GENERATION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful assistant that answers questions accurately and concisely.

Use the provided context to answer the user's question. If the context doesn't contain enough information to answer fully, say so clearly.

Guidelines:
- Be accurate and cite the context when possible
- Be concise but comprehensive
- If uncertain, acknowledge limitations
- Maintain a professional, helpful tone"""),
    ("human", """Question: {query}

Context:
{context}

Answer:"""),
])

ANSWER_GENERATION_NO_CONTEXT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful assistant that answers questions accurately and concisely based on your general knowledge.

Answer the user's question directly without requiring external context."""),
    ("human", "Question: {query}"),
])

ANSWER_EVALUATION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert evaluator assessing answer quality and relevance.

Evaluate if the answer properly addresses the query and is relevant to the provided context (if any).

Consider:
1. Does the answer directly address the question?
2. Is the answer consistent with the context?
3. Is the answer complete and not cut off?
4. Is the answer factually sound?

Respond with ONLY 'YES' if the answer is relevant and satisfactory, or 'NO' if it needs improvement."""),
    ("human", """Query: {query}

Context: {context}

Answer: {answer}

Is this answer relevant and satisfactory?"""),
])
