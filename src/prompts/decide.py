"""
Decision Prompts - Prompts for agent decision making
"""

RETRIEVAL_DECISION_PROMPT = """You are a retrieval decision assistant. Analyze the query and decide if retrieval from a knowledge base is needed.

Query: {query}

Consider:
1. Is this a factual question that needs specific information?
2. Can this be answered from general knowledge?
3. Does this require recent or specific data?
4. Is this a conversational/greeting message?

Respond with a JSON object:
{{
    "needs_retrieval": true/false,
    "reasoning": "explanation of your decision",
    "query_type": "factual/conversational/procedural/opinion"
}}

Decision:"""


SOURCE_SELECTION_PROMPT = """You are a source selection assistant. Based on the query, decide which sources to use for retrieval.

Query: {query}
Query Intent: {intent}

Available sources:
1. vector_db: Internal knowledge base with documents
2. web_search: Internet search for current/external information
3. tools: Calculators, APIs, and other utilities

For each source, consider:
- vector_db: Good for domain-specific knowledge, documentation
- web_search: Good for current events, general knowledge, external facts
- tools: Good for calculations, data lookups, real-time data

Respond with a JSON object:
{{
    "sources": ["source1", "source2"],
    "reasoning": "explanation of source selection"
}}

Selection:"""


TOOL_DECISION_PROMPT = """You are a tool selection assistant. Based on the query and available tools, decide which tools to use.

Query: {query}
Available Context: {context}

Available Tools:
{available_tools}

Consider:
1. What additional information is needed?
2. Can any tools help answer this query?
3. What is the most efficient approach?

Respond with a JSON object:
{{
    "use_tools": true/false,
    "selected_tools": ["tool1", "tool2"],
    "reasoning": "explanation of selection"
}}

Decision:"""


COMPLETENESS_CHECK_PROMPT = """Analyze whether the current context is sufficient to answer the query.

Query: {query}
Current Context: {context}

Consider:
1. Does the context contain relevant information?
2. Are there gaps in the information?
3. Would additional retrieval help?

Respond with a JSON object:
{{
    "is_sufficient": true/false,
    "missing_information": ["list of missing info"],
    "suggestion": "what to do next"
}}

Analysis:"""
