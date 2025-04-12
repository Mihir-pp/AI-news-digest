# AI-Powered News Digest Generator

## Overview
AI-Powered News Digest is a personalized newsletter generator that curates and analyzes news articles from various sources based on user preferences. The application uses OpenAI's GPT models to analyze article content, determine relevance, and provide concise summaries tailored to different user personas.

## Features
- **Personalized Content**: Delivers news based on user preferences and personas
- **AI-Powered Analysis**: Uses OpenAI's GPT models to analyze and summarize articles
- **Relevance Scoring**: Ranks articles by relevance and quality
- **Multiple Categories**: Supports tech, finance, sports, entertainment, and science news
- **Web Interface**: Easy-to-use Gradio web interface for generating newsletters

## User Personas
The application supports five predefined user personas:
- **Tech Enthusiast**: Focus on technology and science news
- **Finance Guru**: Focus on finance and technology news
- **Sports Journalist**: Focus on sports news
- **Entertainment Buff**: Focus on entertainment news
- **Science Nerd**: Focus on science and technology news

## Installation

### Prerequisites
- Python 3.8 or higher
- OpenAI API key

### Setup
1. Clone the repository

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

### Command Line Interface
Run the application in command line mode to generate newsletters for all personas:

```
python app.py
```

This will generate and display newsletters for all predefined personas.

### Web Interface
Launch the web interface to interactively generate newsletters:

```
python web_app.py
```

Once launched:
1. Select your preferred persona from the dropdown menu
2. Click "Generate Newsletter"
3. View your personalized newsletter with the latest relevant articles

## Technical Details

### Components
- **app.py**: Core newsletter generation logic and OpenAI integration
- **web_app.py**: Gradio web interface for interactive use
- **requirements.txt**: Project dependencies

### Dependencies
- feedparser: RSS feed parsing
- requests: HTTP requests
- gradio: Web interface
- openai: OpenAI API integration
- python-dotenv: Environment variable management

### How It Works
1. The application fetches articles from RSS feeds based on user preferences
2. Each article is analyzed using OpenAI's GPT model to:
   - Generate a concise summary
   - Determine the article category
   - Assign a relevance score
3. Articles are filtered based on relevance and user preferences
4. The final newsletter is formatted and presented to the user

## License
This project is open source and available under the MIT License.

## Acknowledgements
- OpenAI for providing the GPT models
- Various news sources for their RSS feeds