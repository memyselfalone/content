#!/usr/bin/env python3
"""
Test script for the AI Article Rewriter API
"""

import asyncio
import aiohttp
import json

async def test_api():
    """Test the article rewriting API"""
    
    # Test article content
    test_article = {
        "content": """
        Artificial intelligence has revolutionized the way we approach content creation. 
        Modern AI systems can generate human-like text that is increasingly difficult to distinguish 
        from content written by actual humans. This technological advancement has created both 
        opportunities and challenges in various industries, particularly in content marketing, 
        journalism, and academic writing.
        
        The key to effective AI content generation lies in understanding the nuances of human 
        communication patterns. By analyzing vast amounts of text data, AI models learn to 
        replicate not just the structure and grammar of human writing, but also the subtle 
        stylistic elements that make content engaging and authentic.
        """,
        "source_urls": ["https://example.com/ai-content"],
        "title": "The Future of AI Content Generation",
        "target_style": "professional"
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            # Test health endpoint
            print("Testing health endpoint...")
            async with session.get("http://localhost:8000/health") as response:
                health_data = await response.json()
                print(f"Health check: {health_data}")
            
            # Test article rewriting
            print("\nTesting article rewriting...")
            async with session.post(
                "http://localhost:8000/rewrite",
                json=test_article,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    print("✅ Article rewriting successful!")
                    print(f"Original length: {len(result['original_content'])} chars")
                    print(f"Rewritten length: {len(result['rewritten_content'])} chars")
                    print(f"Processing time: {result['total_processing_time']:.2f} seconds")
                    print(f"Processing steps: {len(result['processing_steps'])}")
                    
                    # Show first 200 chars of rewritten content
                    print(f"\nRewritten content preview:")
                    print(result['rewritten_content'][:200] + "...")
                    
                else:
                    error_data = await response.json()
                    print(f"❌ Error: {error_data}")
                    
        except Exception as e:
            print(f"❌ Test failed: {e}")
            print("Make sure the API server is running on http://localhost:8000")

if __name__ == "__main__":
    asyncio.run(test_api())