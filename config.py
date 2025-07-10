import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    # API Configuration
    MAX_CONTENT_LENGTH = 50000  # Maximum character length for input content
    REQUEST_TIMEOUT = 300  # 5 minutes timeout for API requests
    
    # Model Settings
    CHATGPT_MODEL = "gpt-3.5-turbo"
    CLAUDE_MODEL = "claude-3-sonnet-20240229"
    GEMINI_MODEL = "gemini-pro"
    
    # Processing Settings
    MAX_RETRIES = 3
    RETRY_DELAY = 2  # seconds
    
    @classmethod
    def validate_api_keys(cls):
        """Validate that all required API keys are present"""
        missing_keys = []
        if not cls.OPENAI_API_KEY:
            missing_keys.append("OPENAI_API_KEY")
        if not cls.ANTHROPIC_API_KEY:
            missing_keys.append("ANTHROPIC_API_KEY")
        if not cls.GOOGLE_API_KEY:
            missing_keys.append("GOOGLE_API_KEY")
        
        if missing_keys:
            raise ValueError(f"Missing required API keys: {', '.join(missing_keys)}")

settings = Settings()