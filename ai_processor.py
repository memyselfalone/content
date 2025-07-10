import asyncio
import time
from typing import List
from datetime import datetime

from openai import AsyncOpenAI
import anthropic
import google.generativeai as genai
from anthropic import Anthropic

from config import settings
from models import ProcessingStep

class AIProcessor:
    """Handles AI model interactions for the article rewriting pipeline"""
    
    def __init__(self):
        # Initialize API clients only if keys are provided
        self.openai_client = None
        self.anthropic_client = None
        self.gemini_model = None
        
        if settings.OPENAI_API_KEY:
            self.openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            
        if settings.ANTHROPIC_API_KEY:
            self.anthropic_client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
            
        if settings.GOOGLE_API_KEY:
            genai.configure(api_key=settings.GOOGLE_API_KEY)
            self.gemini_model = genai.GenerativeModel(settings.GEMINI_MODEL)
    
    async def chatgpt_rewrite(self, content: str, title: str = "", style: str = "professional") -> ProcessingStep:
        """Step 1: Initial rewrite using ChatGPT"""
        if not self.openai_client:
            raise Exception("OpenAI API key not configured")
            
        start_time = time.time()
        
        prompt = f"""
        Rewrite the following article to make it unique and engaging while preserving the core information.
        
        Title: {title}
        Target Style: {style}
        
        Requirements:
        - Completely rephrase all sentences
        - Change sentence structure and length variety
        - Use synonyms and alternative expressions
        - Maintain factual accuracy
        - Keep the same general length
        - Make it sound natural and human-written
        
        Original Article:
        {content}
        
        Rewritten Article:
        """
        
        try:
            response = await self.openai_client.chat.completions.create(
                model=settings.CHATGPT_MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert content writer who specializes in rewriting articles to make them unique while maintaining their core message and factual accuracy."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=4000,
                temperature=0.8
            )
            
            output_text = response.choices[0].message.content.strip()
            processing_time = time.time() - start_time
            
            return ProcessingStep(
                step_name="ChatGPT Rewrite",
                model_used=settings.CHATGPT_MODEL,
                timestamp=datetime.now(),
                input_text=content,
                output_text=output_text,
                processing_time=processing_time
            )
            
        except Exception as e:
            raise Exception(f"ChatGPT rewrite failed: {str(e)}")
    
    async def claude_humanize(self, content: str) -> ProcessingStep:
        """Step 2: Humanize content using Claude"""
        if not self.anthropic_client:
            raise Exception("Anthropic API key not configured")
            
        start_time = time.time()
        
        prompt = f"""
        Take this AI-generated content and make it sound more human and natural. Focus on:
        
        1. Adding subtle imperfections that humans naturally make
        2. Varying sentence rhythm and flow
        3. Including more conversational elements
        4. Adding transitional phrases that sound natural
        5. Incorporating slight stylistic inconsistencies that humans have
        6. Making the tone more engaging and personal
        
        Do not change the core facts or main message, just make it sound more human-written.
        
        Content to humanize:
        {content}
        """
        
        try:
            message = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.anthropic_client.messages.create(
                    model=settings.CLAUDE_MODEL,
                    max_tokens=4000,
                    temperature=0.7,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
            )
            
            output_text = message.content[0].text.strip()
            processing_time = time.time() - start_time
            
            return ProcessingStep(
                step_name="Claude Humanization",
                model_used=settings.CLAUDE_MODEL,
                timestamp=datetime.now(),
                input_text=content,
                output_text=output_text,
                processing_time=processing_time
            )
            
        except Exception as e:
            raise Exception(f"Claude humanization failed: {str(e)}")
    
    async def gemini_revise(self, content: str) -> ProcessingStep:
        """Step 3: Final revision using Gemini"""
        if not self.gemini_model:
            raise Exception("Google API key not configured")
            
        start_time = time.time()
        
        prompt = f"""
        Please perform a final revision of this article to:
        
        1. Ensure smooth flow and readability
        2. Fix any grammatical issues while maintaining natural human writing style
        3. Enhance clarity and engagement
        4. Ensure the content feels authentic and original
        5. Add final polish while keeping it conversational
        6. Maintain all factual information
        
        Article for revision:
        {content}
        """
        
        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.gemini_model.generate_content(prompt)
            )
            
            output_text = response.text.strip()
            processing_time = time.time() - start_time
            
            return ProcessingStep(
                step_name="Gemini Revision",
                model_used=settings.GEMINI_MODEL,
                timestamp=datetime.now(),
                input_text=content,
                output_text=output_text,
                processing_time=processing_time
            )
            
        except Exception as e:
            raise Exception(f"Gemini revision failed: {str(e)}")
    
    async def process_article(self, content: str, title: str = "", style: str = "professional") -> List[ProcessingStep]:
        """Complete processing pipeline"""
        steps = []
        
        # Step 1: ChatGPT rewrite
        step1 = await self.chatgpt_rewrite(content, title, style)
        steps.append(step1)
        
        # Step 2: Claude humanization
        step2 = await self.claude_humanize(step1.output_text)
        steps.append(step2)
        
        # Step 3: Gemini revision
        step3 = await self.gemini_revise(step2.output_text)
        steps.append(step3)
        
        return steps