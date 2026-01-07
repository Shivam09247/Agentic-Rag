"""
Agentic RAG - Main Entry Point

This module provides the main entry point for the Agentic RAG system.
Run this file to start an interactive RAG session or process queries.
"""

import argparse
import sys
from pathlib import Path

# Ensure src is in path
sys.path.insert(0, str(Path(__file__).parent))

from src.graph.rag_graph import run_agentic_rag
from src.retrieval.vector_store import get_vector_store_manager
from src.utils.logging import setup_logger

logger = setup_logger(__name__)


def initialize_system():
    """Initialize the RAG system components."""
    logger.info("Initializing Agentic RAG system...")
    
    # Initialize vector store
    try:
        vsm = get_vector_store_manager()
        vsm.initialize_vector_store()
        logger.info("Vector store initialized")
    except Exception as e:
        logger.warning(f"Vector store initialization failed: {e}")
        logger.warning("System will work in limited mode without vector database")


def process_query(query: str):
    """
    Process a single query through the Agentic RAG system.
    
    Args:
        query: User query to process
    """
    logger.info(f"\n{'='*60}")
    logger.info(f"Processing query: {query}")
    logger.info(f"{'='*60}\n")
    
    # Run the workflow
    result = run_agentic_rag(query)
    
    # Display results
    print("\n" + "="*60)
    print("AGENTIC RAG RESULTS")
    print("="*60)
    print(f"\nOriginal Query: {result.get('original_query', 'N/A')}")
    print(f"Rewritten Query: {result.get('rewritten_query', 'N/A')}")
    print(f"Retrieval Used: {result.get('needs_retrieval', False)}")
    
    if result.get('needs_retrieval'):
        print(f"Source: {result.get('selected_source', 'N/A')}")
    
    print(f"\nIterations: {result.get('iteration', 0)}")
    print(f"Answer Quality: {'✓ Relevant' if result.get('answer_is_relevant') else '✗ Not Relevant'}")
    
    print("\n" + "-"*60)
    print("ANSWER:")
    print("-"*60)
    print(result.get('answer', 'No answer generated'))
    print("="*60 + "\n")


def interactive_mode():
    """Run in interactive mode for continuous queries."""
    logger.info("Starting interactive mode...")
    
    print("\n" + "="*60)
    print("AGENTIC RAG - Interactive Mode")
    print("="*60)
    print("\nCommands:")
    print("  - Type your query and press Enter")
    print("  - Type 'quit' or 'exit' to stop")
    print("  - Type 'index' to index documents from data/documents/")
    print("="*60 + "\n")
    
    while True:
        try:
            query = input("\n🤖 Enter your query: ").strip()
            
            if not query:
                continue
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye! 👋")
                break
            
            if query.lower() == 'index':
                print("\nIndexing documents...")
                vsm = get_vector_store_manager()
                vsm.load_and_index_documents()
                print("✓ Documents indexed successfully")
                continue
            
            process_query(query)
            
        except KeyboardInterrupt:
            print("\n\nInterrupted. Goodbye! 👋")
            break
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            print(f"\n❌ Error: {e}\n")


def main():
    """Main entry point with CLI support."""
    parser = argparse.ArgumentParser(
        description="Agentic RAG - Advanced Retrieval-Augmented Generation System"
    )
    parser.add_argument(
        "-q", "--query",
        type=str,
        help="Process a single query and exit"
    )
    parser.add_argument(
        "--index",
        action="store_true",
        help="Index documents from data/documents/ before processing"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive mode (default if no query provided)"
    )
    
    args = parser.parse_args()
    
    # Initialize system
    initialize_system()
    
    # Index documents if requested
    if args.index:
        logger.info("Indexing documents...")
        vsm = get_vector_store_manager()
        vsm.load_and_index_documents()
        logger.info("Documents indexed successfully")
    
    # Process query or run interactive mode
    if args.query:
        process_query(args.query)
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
