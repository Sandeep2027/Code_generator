import bleach
from markdown import markdown
import os

def sanitize_input(text):
    return bleach.clean(text)

def generate_documentation(description, code, language):
    doc = f"""
# {language.capitalize()} Code Documentation

## Description
{description}

## Generated Code
``` {language}
{code}