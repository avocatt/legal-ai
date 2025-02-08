# Prompt System Documentation

## Overview

The Turkish Legal AI Assistant uses a sophisticated prompt engineering system with multiple template types and comprehensive testing framework. This system ensures high-quality, consistent responses while maintaining legal accuracy.

## Prompt Templates

### 1. Basic Legal Prompt

- Simple, direct question-answering
- Context-aware responses
- Source citations
- Legal terminology integration

### 2. Structured Legal Prompt

- Organized response sections:
  - Question Scope
  - Relevant Laws
  - Legal Analysis
  - Conclusion
- Enhanced context utilization
- Detailed legal references
- Term definitions

### 3. Multi-step Reasoning Prompt

- Step-by-step legal analysis
- Complex question decomposition
- Cross-reference handling
- Comprehensive explanations

## Testing Framework

### Evaluation Metrics

1. **Length Score**

   - Optimal response length
   - Content completeness

2. **Structure Score**

   - Section organization
   - Format adherence
   - Logical flow

3. **Legal Reference Score**

   - Citation accuracy
   - Reference relevance
   - Source integration

4. **Term Usage Score**

   - Legal terminology
   - Term definitions
   - Context appropriateness

5. **Formatting Score**

   - Markdown formatting
   - Visual organization
   - Readability

6. **Section Completeness**
   - Content coverage
   - Detail level
   - Comprehensive answers

### Testing Pipeline

1. **Automated Testing**

   ```python
   python -m src.rag.prompt_testing
   ```

2. **Test Cases**

   - Basic legal questions
   - Complex scenarios
   - Edge cases
   - Multi-part questions

3. **Performance Analysis**
   - Response quality metrics
   - Processing time
   - Memory usage
   - Accuracy scores

## Usage Examples

### Basic Prompt

```python
from src.rag.prompts import BasicLegalPrompt

prompt = BasicLegalPrompt()
formatted = prompt.format(
    context="[Legal Context]",
    question="[Question]"
)
```

### Structured Prompt

```python
from src.rag.prompts import StructuredLegalPrompt

prompt = StructuredLegalPrompt()
formatted = prompt.format(
    context="[Legal Context]",
    question="[Question]"
)
```

### Multi-step Prompt

```python
from src.rag.prompts import MultiStepLegalPrompt

prompt = MultiStepLegalPrompt()
formatted = prompt.format(
    context="[Legal Context]",
    question="[Question]"
)
```

## Evaluation Example

```python
from src.rag.prompts import PromptEvaluator

evaluator = PromptEvaluator()
metrics = evaluator.evaluate_response(
    prompt_name="structured",
    question="Sample question",
    answer="Generated answer",
    expected_structure=["SORU KAPSAMI", "İLGİLİ KANUN MADDELERİ"]
)
```

## Best Practices

1. **Template Selection**

   - Use Basic for simple questions
   - Use Structured for comprehensive answers
   - Use Multi-step for complex analysis

2. **Context Management**

   - Provide relevant context
   - Include necessary references
   - Maintain context window size

3. **Legal Accuracy**

   - Verify citations
   - Check terminology
   - Validate references

4. **Response Quality**
   - Monitor evaluation metrics
   - Review test results
   - Update templates as needed

## Future Improvements

1. **Template Enhancements**

   - Dynamic template selection
   - Context-aware formatting
   - Adaptive structuring

2. **Testing Framework**

   - Additional metrics
   - Real-time evaluation
   - User feedback integration

3. **Performance Optimization**
   - Response time improvement
   - Memory usage reduction
   - Caching implementation
