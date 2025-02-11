"""Prompt templates and evaluation module for the Turkish Legal RAG system. This module contains different prompt templates and utilities for evaluating their effectiveness."""

from .base import BasePromptTemplate
from .templates import BasicLegalPrompt, MultiStepLegalPrompt, StructuredLegalPrompt

__all__ = [
    "BasePromptTemplate",
    "BasicLegalPrompt",
    "StructuredLegalPrompt",
    "MultiStepLegalPrompt",
]
