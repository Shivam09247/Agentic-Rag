"""
LLM Client - Unified interface for various LLM providers
"""
from typing import Optional, List, Dict, Any, Union
from functools import lru_cache
import json
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

# Optional providers - import if available
try:
    from langchain_openai import ChatOpenAI
    HAS_OPENAI = True
except ImportError:
    ChatOpenAI = None
    HAS_OPENAI = False

try:
    from langchain_anthropic import ChatAnthropic
    HAS_ANTHROPIC = True
except ImportError:
    ChatAnthropic = None
    HAS_ANTHROPIC = False

from ..config.settings import settings
from ..config.logging import get_logger

logger = get_logger("llm.client")


class LLMClient:
    """Unified LLM client with provider abstraction"""
    
    def __init__(
        self,
        provider: str = None,
        model: str = None,
        temperature: float = None,
        max_tokens: int = None
    ):
        self.provider = provider or settings.LLM_PROVIDER
        self.model = model or settings.LLM_MODEL
        self.temperature = temperature if temperature is not None else settings.LLM_TEMPERATURE
        self.max_tokens = max_tokens or settings.LLM_MAX_TOKENS
        
        self._llm = self._create_llm()
        self._str_parser = StrOutputParser()
        self._json_parser = JsonOutputParser()
    
    def _create_llm(self):
        """Create LLM instance based on provider"""
        if self.provider == "groq":
            api_key = settings.GROQ_API_KEY or os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError("GROQ_API_KEY not configured")
            return ChatGroq(
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                api_key=api_key
            )
        elif self.provider == "openai":
            if not HAS_OPENAI:
                raise ImportError("langchain-openai is not installed. Run: pip install langchain-openai")
            api_key = settings.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not configured")
            return ChatOpenAI(
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                api_key=api_key
            )
        elif self.provider == "anthropic":
            if not HAS_ANTHROPIC:
                raise ImportError("langchain-anthropic is not installed. Run: pip install langchain-anthropic")
            api_key = settings.ANTHROPIC_API_KEY or os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not configured")
            return ChatAnthropic(
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                api_key=api_key
            )
        else:
            raise ValueError(f"Unknown LLM provider: {self.provider}")
    
    def _build_messages(
        self,
        prompt: str,
        system_prompt: str = None,
        history: List[Dict] = None
    ) -> List:
        """Build message list for LLM"""
        messages = []
        
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        
        if history:
            for msg in history:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                if role == "user":
                    messages.append(HumanMessage(content=content))
                elif role == "assistant":
                    messages.append(AIMessage(content=content))
                elif role == "system":
                    messages.append(SystemMessage(content=content))
        
        messages.append(HumanMessage(content=prompt))
        return messages
    
    def invoke(
        self,
        prompt: str,
        system_prompt: str = None,
        history: List[Dict] = None,
        **kwargs
    ) -> str:
        """Invoke LLM and return string response"""
        messages = self._build_messages(prompt, system_prompt, history)
        
        try:
            response = self._llm.invoke(messages)
            return response.content
        except Exception as e:
            logger.error(f"LLM invocation error: {e}")
            raise
    
    async def ainvoke(
        self,
        prompt: str,
        system_prompt: str = None,
        history: List[Dict] = None,
        **kwargs
    ) -> str:
        """Async invoke LLM"""
        messages = self._build_messages(prompt, system_prompt, history)
        
        try:
            response = await self._llm.ainvoke(messages)
            return response.content
        except Exception as e:
            logger.error(f"LLM async invocation error: {e}")
            raise
    
    def invoke_json(
        self,
        prompt: str,
        system_prompt: str = None,
        history: List[Dict] = None,
        **kwargs
    ) -> Dict:
        """Invoke LLM and parse JSON response"""
        response = self.invoke(prompt, system_prompt, history, **kwargs)
        
        try:
            # Try to extract JSON from response
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            
            return json.loads(response.strip())
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse JSON response: {e}")
            # Try to find JSON in the response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except:
                    pass
            return {"error": "Failed to parse JSON", "raw_response": response}
    
    async def ainvoke_json(
        self,
        prompt: str,
        system_prompt: str = None,
        history: List[Dict] = None,
        **kwargs
    ) -> Dict:
        """Async invoke LLM and parse JSON response"""
        response = await self.ainvoke(prompt, system_prompt, history, **kwargs)
        
        try:
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            
            return json.loads(response.strip())
        except json.JSONDecodeError:
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except:
                    pass
            return {"error": "Failed to parse JSON", "raw_response": response}
    
    def stream(
        self,
        prompt: str,
        system_prompt: str = None,
        history: List[Dict] = None,
        **kwargs
    ):
        """Stream LLM response"""
        messages = self._build_messages(prompt, system_prompt, history)
        
        for chunk in self._llm.stream(messages):
            if hasattr(chunk, 'content'):
                yield chunk.content


@lru_cache()
def get_llm(
    provider: str = None,
    model: str = None,
    temperature: float = None
) -> LLMClient:
    """Get cached LLM client instance"""
    return LLMClient(
        provider=provider,
        model=model,
        temperature=temperature
    )


def get_chat_model(
    provider: str = None,
    model: str = None,
    temperature: float = None
):
    """Get raw LangChain chat model"""
    provider = provider or settings.LLM_PROVIDER
    model = model or settings.LLM_MODEL
    temperature = temperature if temperature is not None else settings.LLM_TEMPERATURE
    
    if provider == "groq":
        api_key = settings.GROQ_API_KEY or os.getenv("GROQ_API_KEY")
        return ChatGroq(
            model=model,
            temperature=temperature,
            api_key=api_key
        )
    elif provider == "openai":
        api_key = settings.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")
        return ChatOpenAI(
            model=model,
            temperature=temperature,
            api_key=api_key
        )
    elif provider == "anthropic":
        api_key = settings.ANTHROPIC_API_KEY or os.getenv("ANTHROPIC_API_KEY")
        return ChatAnthropic(
            model=model,
            temperature=temperature,
            api_key=api_key
        )
    else:
        raise ValueError(f"Unknown provider: {provider}")
