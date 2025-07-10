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
        Write a blog post about the following topic with personal tone. Take the content provided and transform it into a personal blog post that feels authentic and engaging.
        
        Title: {title}
        Target Style: {style}
        
        Requirements:
        - Use a personal, conversational tone
        - Write as if sharing personal insights or experiences
        - Make it engaging and relatable
        - Maintain all factual accuracy
        - Keep the same general length
        - Ensure it sounds naturally written by a human
        
        Original Content:
        {content}
        
        Personal Blog Post:
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
        Rewrite this content like someone processing their thoughts in real time. Make it sound natural and human by:
        
        1. Adding natural thought processes and transitions
        2. Including slight hesitations and considerations ("I think...", "It seems like...", "Maybe...")
        3. Using more conversational language and flow
        4. Adding personal reflections and observations
        5. Making it feel like someone working through ideas as they write
        6. Including natural human imperfections in reasoning and expression
        
        Transform this content to sound like authentic human thinking:
        
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
        Find any phrasing that sounds robotic or predictable in this content and suggest changes. Focus on:
        
        1. Identifying overly formal or robotic language patterns
        2. Spotting predictable AI-generated phrases and structures
        3. Finding repetitive or mechanical sentence patterns
        4. Detecting unnatural transitions or conclusions
        5. Locating overly perfect grammar or structure
        6. Suggesting more natural, human-like alternatives
        
        Review this content and make it sound more authentic and less AI-generated:
        
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