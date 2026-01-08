"""
Production server entry point.
Run with: python main.py
Or: uvicorn src.app:app --host 0.0.0.0 --port 8000
"""

import uvicorn

if __name__ == "__main__":
    port = 8000
    host = "127.0.0.1"
    
    # Print user-friendly URLs before starting
    print("\n" + "="*60)
    print("🚀 Starting Agentic RAG API Server...")
    print("="*60)
    print(f"📍 Server will bind to: {host}:{port}")
    print(f"\n🌐 Access the API at:")
    print(f"   • http://localhost:{port}/")
    print(f"   • http://127.0.0.1:{port}/")
    print(f"\n📚 API Documentation:")
    print(f"   • Swagger UI: http://localhost:{port}/docs")
    print(f"   • ReDoc:      http://localhost:{port}/redoc")
    print(f"\n💚 Health Check: http://localhost:{port}/health")
    print("="*60 + "\n")
    
    uvicorn.run(
        "src.app:app",
        host=host,
        port=port,
        reload=True,  # Disable in production
        log_level="info"
    )
    
    
