import gradio as gr
from app import NewsletterGenerator

def generate_newsletter(persona):
    # Define user personas
    personas = {
        'tech_enthusiast': ['tech', 'science'],
        'finance_guru': ['finance', 'tech'],
        'sports_journalist': ['sports'],
        'entertainment_buff': ['entertainment'],
        'science_nerd': ['science', 'tech']
    }
    
    # Get preferences for selected persona
    preferences = personas[persona]
    
    # Generate newsletter with selected preferences
    newsletter = NewsletterGenerator(user_preferences=preferences)
    content = newsletter.generate_newsletter()
    
    # Format the newsletter content for display
    formatted_content = f"# AI-Powered News Digest for {persona.replace('_', ' ').title()}\n\n"
    
    # Add a concise summary at the top
    if content:
        top_articles = content[:3]  # Get top 3 articles by relevance
        formatted_content += "## Today's Highlights\n\n"
        formatted_content += "*Here are the most important stories selected for you:*\n\n"
        for article in top_articles:
            formatted_content += f"- **{article['title']}** - {article['analysis'][:100]}...\n"
        formatted_content += "\n---\n\n"
    
    # Organize content by categories
    categories = {}
    for article in content:
        category = article['category']
        if category not in categories:
            categories[category] = []
        categories[category].append(article)
    
    # Create sections for each category
    for category, articles in categories.items():
        formatted_content += f"## {category.upper()} NEWS\n\n"
        
        for article in articles:
            formatted_content += f"### {article['title']}\n"
            formatted_content += f"**Source:** {article['source']} | **Relevance:** {article['relevance']}/10\n\n"
            formatted_content += f"{article['analysis']}\n\n"
            formatted_content += f"[Read full article]({article['link']})\n\n"
            formatted_content += "---\n\n"
    
    return formatted_content

# Create the Gradio interface with dropdown
with gr.Blocks(theme=gr.themes.Monochrome()) as interface:
    gr.Markdown("# AI-Powered News Digest")
    gr.Markdown("Select a persona and generate a personalized newsletter with the latest news articles.")
    
    with gr.Row():
        persona_dropdown = gr.Dropdown(
            choices=[
                "tech_enthusiast", 
                "finance_guru", 
                "sports_journalist", 
                "entertainment_buff", 
                "science_nerd"
            ],
            value="tech_enthusiast",
            label="Select Your Persona"
        )
    
    generate_button = gr.Button("Generate Newsletter")
    output = gr.Markdown()
    
    generate_button.click(
        fn=generate_newsletter,
        inputs=persona_dropdown,
        outputs=output
    )

if __name__ == "__main__":
    interface.launch()