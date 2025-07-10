# AI Article Rewriter API

A FastAPI-based REST API that rewrites articles using multiple AI models to create human-like content that bypasses AI detection. The system uses a three-stage pipeline with different AI models to ensure natural, engaging content.

## Features

- **Multi-AI Pipeline**: Uses ChatGPT, Claude, and Gemini in sequence
- **AI Detection Bypass**: Employs techniques to make content appear more human-written
- **Reference Tracking**: Maintains links to source materials
- **Async Processing**: Supports both synchronous and asynchronous processing
- **Style Customization**: Allows different writing styles (professional, casual, academic)

## Pipeline Process

1. **ChatGPT Rewrite**: Initial content rewriting with structure variation
2. **Claude Humanization**: Adds human-like imperfections and natural flow
3. **Gemini Revision**: Final polish and readability enhancement

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd content
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. Run the server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### `GET /`
Health check endpoint

### `GET /health`
Detailed health check with API key status

### `POST /rewrite`
Rewrite an article through the full AI pipeline

**Request Body:**
```json
{
  "content": "Your article content here...",
  "source_urls": ["https://example.com/source"],
  "title": "Article Title",
  "target_style": "professional"
}
```

**Response:**
```json
{
  "original_content": "...",
  "rewritten_content": "...",
  "title": "...",
  "processing_steps": [...],
  "reference_urls": [...],
  "total_processing_time": 45.67
}
```

### `POST /rewrite-async`
Start asynchronous article rewriting

## Configuration

Set the following environment variables in your `.env` file:

- `OPENAI_API_KEY`: Your OpenAI API key
- `ANTHROPIC_API_KEY`: Your Anthropic API key  
- `GOOGLE_API_KEY`: Your Google AI API key

## Testing

Run the test script:
```bash
python test_api.py
```

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Requirements

- Python 3.8+
- Valid API keys for OpenAI, Anthropic, and Google AI
- Internet connection for API calls

## License

See LICENSE file for details.