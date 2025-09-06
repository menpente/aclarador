# Agents Framework for Aclarador

## Agent Architecture

### 1. Analyzer Agent
**Purpose**: Initial text assessment and classification
**Responsibilities**:
- Determine text type (web content, formal document, marketing, etc.)
- Identify primary clarity issues
- Route to appropriate specialized agents
- Provide overall readability score

### 2. Grammar Agent  
**Purpose**: Grammar and syntax corrections
**Responsibilities**:
- Detect grammatical errors
- Fix sentence structure issues
- Ensure proper punctuation
- Apply conjugation and agreement rules
**PDF References**: Sections on grammar rules, punctuation guidelines

### 3. Style Agent
**Purpose**: Style improvements and coherence
**Responsibilities**:
- Simplify complex sentences (max 30 words)
- Ensure one idea per sentence
- Improve logical flow and structure
- Eliminate jargon and technical language
**PDF References**: Clear writing patterns, style guidelines

### 4. SEO Agent
**Purpose**: Balance clarity with search optimization
**Responsibilities**:
- Maintain keyword density while improving clarity
- Optimize meta descriptions and titles
- Balance SEO requirements with plain language principles
**PDF References**: Internet writing section, SEO vs clarity guidelines

### 5. Validator Agent
**Purpose**: Final review and quality assurance
**Responsibilities**:
- Ensure all changes maintain original meaning
- Verify compliance with lenguaje claro principles
- Generate final report with improvement metrics
- Cite relevant PDF manual sections

## Agent Coordination

### Sequential Processing
1. **Analyzer** ’ Text classification and issue identification
2. **Specialized Agents** ’ Parallel processing of specific aspects
3. **Validator** ’ Final review and consolidation

### Knowledge Base Integration
- Each agent queries relevant PDF sections via RAG system
- Contextual guidelines retrieved based on text type and issues
- Citations provided for all recommendations

## Communication Protocol

### Input Format
```python
{
    "text": "Original text to analyze",
    "text_type": "web|document|marketing|formal",
    "focus_areas": ["grammar", "style", "seo"],
    "severity_level": "basic|intermediate|advanced"
}
```

### Output Format
```python
{
    "corrected_text": "Improved version",
    "changes": [
        {
            "type": "grammar|style|clarity|seo",
            "original": "original phrase",
            "corrected": "corrected phrase", 
            "reason": "explanation",
            "pdf_reference": "Manual section X.Y"
        }
    ],
    "metrics": {
        "readability_score": 0-100,
        "avg_sentence_length": number,
        "complexity_reduction": percentage
    }
}
```

## Implementation Strategy

### Phase 1: Core Agents
- Implement basic Analyzer and Grammar agents
- Simple rule-based corrections

### Phase 2: PDF Integration  
- Add knowledge base retrieval
- Enhance agents with contextual guidelines

### Phase 3: Advanced Features
- SEO optimization capabilities
- Multi-pass refinement
- User preference learning