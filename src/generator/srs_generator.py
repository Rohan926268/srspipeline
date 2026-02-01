"""SRS Generator - Generates SRS documents using Gemini AI."""

import os
from typing import Optional
from google import genai
from dotenv import load_dotenv

from src.templates import TemplateRegistry, get_template

load_dotenv()


class SRSGenerator:
    """SRS Document Generator using Google Gemini AI."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the SRS Generator.
        
        Args:
            api_key: Optional Gemini API key. If not provided, uses GOOGLE_GEMINI_API_KEY env var.
        """
        self.api_key = api_key or os.getenv("GOOGLE_GEMINI_API_KEY")
        self.gemini_model = os.getenv("GEMINI_MODEL")
        if not self.api_key:
            raise ValueError("Gemini API key is required. Set GOOGLE_GEMINI_API_KEY environment variable or pass api_key parameter.")
        
        self.client = genai.Client(api_key=self.api_key)
        self.model = self.gemini_model
    
    def generate(
        self, 
        user_requirement: str, 
        template_name: Optional[str] = None,
        custom_instructions: Optional[str] = None
    ) -> dict:
        """Generate an SRS document based on user requirements.
        
        Args:
            user_requirement: The user's project/product requirements
            template_name: Optional template name (agile, ieee, minimal, startup)
                          If not provided, auto-detects based on requirement content
            custom_instructions: Optional additional instructions for generation
        
        Returns:
            dict containing:
                - srs_document: The generated SRS in Markdown format
                - template_used: The template that was used
                - metadata: Additional metadata about the generation
        """
        # Auto-detect or use provided template
        if template_name:
            selected_template = template_name.lower()
        else:
            selected_template = TemplateRegistry.get_template_for_requirement(user_requirement)
        
        # Get the template
        template = get_template(selected_template)
        if not template:
            # Fallback to agile if template not found
            template = get_template("agile")
            selected_template = "agile"
        
        # Build the prompt
        prompt = template.get_prompt_template().format(user_requirement=user_requirement)
        
        # Add custom instructions if provided
        if custom_instructions:
            prompt += f"\n\n**Additional Instructions:**\n{custom_instructions}"
        
        # Generate using Gemini
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            srs_document = response.text
            
            return {
                "success": True,
                "srs_document": srs_document,
                "template_used": selected_template,
                "template_description": template.description,
                "sections": template.sections,
                "validation_criteria": template.get_validation_criteria(),
                "metadata": {
                    "model": self.model,
                    "user_requirement_length": len(user_requirement),
                    "output_length": len(srs_document)
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "template_used": selected_template,
                "srs_document": None
            }
    
    def list_available_templates(self) -> list:
        """List all available SRS templates."""
        return TemplateRegistry.list_templates()
    
    def get_template_info(self, template_name: str) -> Optional[dict]:
        """Get information about a specific template."""
        template = get_template(template_name)
        if template:
            return {
                "name": template.name,
                "description": template.description,
                "sections": template.get_sections(),
                "validation_criteria": template.get_validation_criteria()
            }
        return None