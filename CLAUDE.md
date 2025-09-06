# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Aclarador is a Spanish text clarity improvement tool built with Streamlit. The application uses the Groq API with the Llama 3.3 70B model to analyze Spanish text and provide corrections based on "lenguaje claro" (plain language) principles.

## Dependencies and Environment

- **Python**: Streamlit-based web application
- **Key Libraries**: streamlit, groq, PIL (Pillow), os
- **API Integration**: Groq API with Llama 3.3 70B model
- **Environment Variable**: `GROQ_API_KEY` must be set

## Common Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py

# Set required environment variable
export GROQ_API_KEY="your_api_key_here"
```

## Architecture

### Core Components

1. **app.py**: Single-file Streamlit application containing:
   - Groq API client initialization with environment-based API key
   - `process_text()` function: Handles text processing with predefined Spanish prompt for plain language evaluation
   - Main Streamlit interface with text input and processing workflow

### Text Processing Flow

1. User inputs Spanish text through Streamlit interface
2. Text is combined with expert prompt defining plain language guidelines:
   - One idea per sentence
   - Max 30 words per sentence
   - Avoid jargon
   - Follow subject-verb-predicate order
   - Use logical structure
3. Combined prompt sent to Groq API (Llama 3.3 70B model)
4. Response formatted with corrected text and explanations using markdown sections

### Session State Management

The app maintains user input in `st.session_state["user_input"]` and clears it after processing to reset the interface.

## Reference Materials

- **Manual de estilo**: PDF guide located in `ref/Manual de estilo de lenguaje claro.pdf`
- **agents.md**: Reference file (currently minimal content)

## API Integration Details

- **Model**: "llama-3.3-70b-versatile" 
- **Response Structure**: Returns corrected text followed by explanations
- **Output Format**: Uses `###TEXTO CORREGIDO###` and `###EXPLICACIÓN###` markdown headers