"""
Agentic RAG - Root Entry Point

This module provides the root entry point for the Agentic RAG system.
It delegates to the main module in the src directory.
"""

import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))


def main():
    """Main entry point."""
    from src.main import main as run_main
    run_main()


if __name__ == "__main__":
    main()
