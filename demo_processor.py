import asyncio
import time
import random
from typing import List
from datetime import datetime
from models import ProcessingStep

class DemoAIProcessor:
    """Demo AI processor that simulates the pipeline without actual API calls"""
    
    def __init__(self):
        self.demo_mode = True
    
    async def chatgpt_rewrite(self, content: str, title: str = "", style: str = "professional") -> ProcessingStep:
        """Demo Step 1: Simulated ChatGPT rewrite"""
        start_time = time.time()
        
        # Simulate processing time
        await asyncio.sleep(1.5)
        
        # Create a demo rewritten version
        demo_content = self._demo_rewrite(content, "chatgpt")
        processing_time = time.time() - start_time
        
        return ProcessingStep(
            step_name="ChatGPT Rewrite (Demo)",
            model_used="gpt-3.5-turbo (simulated)",
            timestamp=datetime.now(),
            input_text=content,
            output_text=demo_content,
            processing_time=processing_time
        )
    
    async def claude_humanize(self, content: str) -> ProcessingStep:
        """Demo Step 2: Simulated Claude humanization"""
        start_time = time.time()
        
        # Simulate processing time
        await asyncio.sleep(1.2)
        
        # Create a demo humanized version
        demo_content = self._demo_rewrite(content, "claude")
        processing_time = time.time() - start_time
        
        return ProcessingStep(
            step_name="Claude Humanization (Demo)",
            model_used="claude-3-sonnet (simulated)",
            timestamp=datetime.now(),
            input_text=content,
            output_text=demo_content,
            processing_time=processing_time
        )
    
    async def gemini_revise(self, content: str) -> ProcessingStep:
        """Demo Step 3: Simulated Gemini revision"""
        start_time = time.time()
        
        # Simulate processing time
        await asyncio.sleep(1.0)
        
        # Create a demo revised version
        demo_content = self._demo_rewrite(content, "gemini")
        processing_time = time.time() - start_time
        
        return ProcessingStep(
            step_name="Gemini Revision (Demo)",
            model_used="gemini-pro (simulated)",
            timestamp=datetime.now(),
            input_text=content,
            output_text=demo_content,
            processing_time=processing_time
        )
    
    def _demo_rewrite(self, content: str, model: str) -> str:
        """Create a demo rewritten version of the content"""
        sentences = content.split('. ')
        
        # Different rewriting strategies for each model
        if model == "chatgpt":
            # ChatGPT simulation: restructure and rephrase
            rewrites = []
            for sentence in sentences:
                if sentence.strip():
                    rewritten = self._rephrase_sentence(sentence.strip())
                    rewrites.append(rewritten)
            return '. '.join(rewrites) + '.'
            
        elif model == "claude":
            # Claude simulation: add human touches and vary flow
            rewrites = []
            for i, sentence in enumerate(sentences):
                if sentence.strip():
                    rewritten = self._humanize_sentence(sentence.strip())
                    if i > 0 and random.random() < 0.3:
                        # Occasionally add transitional phrases
                        transitions = ["Moreover, ", "Additionally, ", "Furthermore, ", "In fact, "]
                        rewritten = random.choice(transitions) + rewritten.lower()
                    rewrites.append(rewritten)
            return '. '.join(rewrites) + '.'
            
        elif model == "gemini":
            # Gemini simulation: polish and refine
            rewrites = []
            for sentence in sentences:
                if sentence.strip():
                    rewritten = self._polish_sentence(sentence.strip())
                    rewrites.append(rewritten)
            return '. '.join(rewrites) + '.'
        
        return content
    
    def _rephrase_sentence(self, sentence: str) -> str:
        """Simulate sentence rephrasing"""
        # Simple word substitutions for demo
        replacements = {
            'artificial intelligence': 'AI technology',
            'technology': 'technological innovation',
            'systems': 'frameworks',
            'create': 'develop',
            'important': 'crucial',
            'modern': 'contemporary',
            'advanced': 'sophisticated',
            'effective': 'efficient'
        }
        
        result = sentence
        for old, new in replacements.items():
            result = result.replace(old, new)
        
        return result
    
    def _humanize_sentence(self, sentence: str) -> str:
        """Simulate humanizing text"""
        # Add some human-like variations
        if sentence.startswith('This'):
            sentence = sentence.replace('This', 'This particular', 1)
        
        if 'very' not in sentence and random.random() < 0.3:
            words = sentence.split()
            if len(words) > 3:
                # Insert 'quite' or 'rather' before adjectives
                for i, word in enumerate(words):
                    if word.endswith('ing') or word.endswith('ed'):
                        words.insert(i, 'quite')
                        break
                sentence = ' '.join(words)
        
        return sentence
    
    def _polish_sentence(self, sentence: str) -> str:
        """Simulate polishing text"""
        # Make minor improvements
        sentence = sentence.replace(' that ', ' which ')
        sentence = sentence.replace(' also ', ' likewise ')
        
        return sentence
    
    async def process_article(self, content: str, title: str = "", style: str = "professional") -> List[ProcessingStep]:
        """Complete demo processing pipeline"""
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