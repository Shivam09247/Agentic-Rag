"""
Quick Setup Script for Agentic RAG

This script helps you quickly set up and test the Agentic RAG system.
"""

import os
import sys
from pathlib import Path


def print_banner():
    """Print welcome banner."""
    print("\n" + "="*70)
    print("  🤖 AGENTIC RAG - Quick Setup")
    print("="*70 + "\n")


def check_env_file():
    """Check if .env file exists."""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists():
        print("⚠️  .env file not found!")
        
        if env_example.exists():
            print("\n📝 Creating .env from .env.example...")
            env_example.read_text()
            with open(env_file, 'w') as f:
                f.write(env_example.read_text())
            print("✓ .env file created")
        else:
            print("❌ .env.example not found either!")
            return False
    else:
        print("✓ .env file exists")
    
    # Check for OpenAI API key
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        print("\n⚠️  WARNING: OPENAI_API_KEY not set!")
        print("   Please edit .env and add your OpenAI API key")
        print("   Get your key from: https://platform.openai.com/api-keys")
        return False
    else:
        print("✓ OpenAI API key configured")
    
    return True


def check_dependencies():
    """Check if required packages are installed."""
    print("\n📦 Checking dependencies...")
    
    required = [
        "langchain",
        "langgraph",
        "langchain_openai",
        "chromadb",
        "openai",
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ❌ {package} - NOT INSTALLED")
            missing.append(package)
    
    if missing:
        print("\n⚠️  Missing packages detected!")
        print(f"   Run: pip install -r requirements.txt")
        return False
    
    return True


def check_data_directory():
    """Check data directory setup."""
    print("\n📁 Checking data directories...")
    
    docs_dir = Path("data/documents")
    if not docs_dir.exists():
        print("  Creating data/documents/...")
        docs_dir.mkdir(parents=True, exist_ok=True)
    
    # Check for documents
    doc_files = list(docs_dir.glob("*.txt"))
    if doc_files:
        print(f"  ✓ Found {len(doc_files)} document(s)")
        for doc in doc_files:
            print(f"    - {doc.name}")
    else:
        print("  ⚠️  No documents found in data/documents/")
        print("     Sample documents have been created for you")
    
    return True


def run_test_query():
    """Run a test query to verify system works."""
    print("\n🧪 Running test query...")
    
    try:
        from src.graph.rag_graph import run_agentic_rag
        
        result = run_agentic_rag("What is 2 + 2?")
        
        print("\n" + "-"*70)
        print("Test Result:")
        print("-"*70)
        print(f"Query: {result.get('original_query')}")
        print(f"Answer: {result.get('answer')}")
        print("-"*70)
        print("\n✓ System is working!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False


def main():
    """Main setup function."""
    print_banner()
    
    all_ok = True
    
    # Check environment
    if not check_env_file():
        all_ok = False
    
    # Check dependencies
    if not check_dependencies():
        all_ok = False
    
    # Check data directory
    check_data_directory()
    
    if not all_ok:
        print("\n" + "="*70)
        print("⚠️  Setup incomplete - please fix the issues above")
        print("="*70 + "\n")
        return
    
    # Run test
    print("\n" + "="*70)
    print("✓ Setup complete! Running test...")
    print("="*70)
    
    if run_test_query():
        print("\n" + "="*70)
        print("🎉 SUCCESS! Your Agentic RAG system is ready!")
        print("="*70)
        print("\nNext steps:")
        print("  1. Add your documents to data/documents/")
        print("  2. Run: python main.py --index")
        print("  3. Run: python main.py (interactive mode)")
        print("  4. Or: python main.py --query 'Your question here'")
        print("\n" + "="*70 + "\n")
    else:
        print("\n⚠️  Test failed - please check the error above")


if __name__ == "__main__":
    main()
