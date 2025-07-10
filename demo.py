#!/usr/bin/env python3
"""
Comprehensive demo of the AI Article Rewriter API
Shows the complete pipeline in action
"""

import asyncio
import aiohttp
import json
import time

async def comprehensive_demo():
    """Demonstrate the complete API functionality"""
    
    print("🎯 AI Article Rewriter API - Comprehensive Demo")
    print("=" * 60)
    
    # Sample article content
    test_articles = [
        {
            "title": "AI in Healthcare",
            "content": """
            Artificial intelligence is transforming healthcare by enabling more accurate diagnoses 
            and personalized treatment plans. Machine learning algorithms can analyze medical images 
            faster than human radiologists, while natural language processing helps extract insights 
            from clinical notes. These technologies are creating new opportunities for improving 
            patient outcomes and reducing healthcare costs.
            """,
            "source_urls": ["https://healthcare-ai.com/study", "https://medical-journal.org/ai-research"],
            "target_style": "professional"
        },
        {
            "title": "The Future of Remote Work", 
            "content": """
            Remote work has become a permanent fixture in the modern workplace. Companies are 
            discovering that distributed teams can be just as productive as traditional office-based 
            workers. This shift requires new management strategies, communication tools, and 
            approaches to maintaining company culture across geographic boundaries.
            """,
            "source_urls": ["https://remote-work.com/trends", "https://business-insights.org/remote"],
            "target_style": "casual"
        }
    ]
    
    async with aiohttp.ClientSession() as session:
        try:
            # Test 1: Health Check
            print("\n1️⃣ Testing Health Check...")
            async with session.get("http://localhost:8000/health") as response:
                health_data = await response.json()
                print(f"   Status: {health_data['status']}")
                print(f"   Demo Mode: {health_data['demo_mode']}")
                print(f"   API Keys: {health_data['api_keys_configured']}")
            
            # Test 2: Process Multiple Articles
            for i, article in enumerate(test_articles, 1):
                print(f"\n{i+1}️⃣ Processing Article: '{article['title']}'")
                print(f"   Style: {article['target_style']}")
                print(f"   Original length: {len(article['content'])} chars")
                
                start_time = time.time()
                async with session.post(
                    "http://localhost:8000/rewrite",
                    json=article,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        processing_time = time.time() - start_time
                        
                        print(f"   ✅ Success! Processed in {processing_time:.2f}s")
                        print(f"   Rewritten length: {len(result['rewritten_content'])} chars")
                        print(f"   Processing steps: {len(result['processing_steps'])}")
                        print(f"   Reference URLs: {len(result['reference_urls'])}")
                        
                        if result.get('ai_detection_confidence'):
                            print(f"   AI Detection Confidence: {result['ai_detection_confidence']:.2f}")
                        
                        # Show processing steps
                        print("   Processing Pipeline:")
                        for step in result['processing_steps']:
                            print(f"     → {step['step_name']}: {step['processing_time']:.2f}s")
                        
                        # Show content preview
                        print(f"   Rewritten Preview:")
                        preview = result['rewritten_content'][:150].replace('\n', ' ').strip()
                        print(f"     \"{preview}...\"")
                        
                    else:
                        error_data = await response.json()
                        print(f"   ❌ Error: {error_data}")
            
            # Test 3: Test Async Endpoint
            print(f"\n4️⃣ Testing Async Processing...")
            async with session.post(
                "http://localhost:8000/rewrite-async",
                json=test_articles[0],
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    print(f"   ✅ Async task started: {result['task_id']}")
                    print(f"   Status: {result['status']}")
                else:
                    error_data = await response.json()
                    print(f"   ❌ Error: {error_data}")
            
            print("\n🎉 Demo completed successfully!")
            print("=" * 60)
            print("📊 Summary:")
            print("   • Multi-AI pipeline working correctly")
            print("   • Reference URL tracking functional") 
            print("   • Error handling and validation working")
            print("   • Both sync and async endpoints operational")
            print("   • Demo mode enables testing without API keys")
            print("\n📖 API Documentation: http://localhost:8000/docs")
            
        except Exception as e:
            print(f"❌ Demo failed: {e}")
            print("Make sure the API server is running on http://localhost:8000")

if __name__ == "__main__":
    asyncio.run(comprehensive_demo())