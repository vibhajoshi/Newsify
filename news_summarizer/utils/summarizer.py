import requests

def clean_summary(summary):
    """Format the summary with proper bullet points and spacing"""
    lines = []
    for line in summary.split('\n'):
        line = line.strip()
        if not line:
            continue
        
        # Remove existing bullets/numbers
        if line.startswith(('•', '*', '-', '1.', '2.', '3.')):
            line = line[1:].strip()
        
        # Format section headers
        if ':' in line and line.endswith(':'):
            lines.append(f"\n<b>{line}</b>")
        else:
            lines.append(f"• {line}")
    
    return '\n'.join(lines)

def summarize_with_ollama(text):
    try:
        # Local Ollama API call
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2",
                "prompt": f"Summarize this news in clean bullet points:\n\n{text}",
                "stream": False
            }
        )
        
        if response.status_code == 200:
            raw_summary = response.json().get("response", "")
            return clean_summary(raw_summary)
        return "• Could not generate summary (API error)"
    except Exception as e:
        print(f"Summarization error: {str(e)}")
        return "• Could not generate summary (server error)"