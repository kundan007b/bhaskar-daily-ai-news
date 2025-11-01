#!/usr/bin/env python3
"""
Automated bilingual news post generator for Bhaskar Daily AI News
Generates AI-curated content with error handling, validation, and retry logic
"""
import os
import re
import json
import time
import hashlib
import datetime
import textwrap
import base64
import tempfile
import shutil
import logging
import sys
from pathlib import Path
from typing import Dict, List, Optional

import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from jsonschema import validate, ValidationError
from PIL import Image
from io import BytesIO

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Setup paths
REPO = Path(__file__).resolve().parents[1]
POSTS = REPO / "_posts"
IMGDIR = REPO / "assets" / "images"
IMGDIR.mkdir(parents=True, exist_ok=True)

# API key validation
API = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not API:
    logger.error("GEMINI_API_KEY environment variable not set")
    sys.exit(1)

# Configuration
TOPICS = [
    "India political news and government updates",
    "India business and economy news",
    "Technology and innovation in India",
    "Personal finance, taxation and savings tips",
    "Startups, entrepreneurs and success stories in India"
]
WORDS = 700
MAX_IMAGE_WIDTH = 1200
IMAGE_QUALITY = 85

# JSON Schema for validation
POST_SCHEMA = {
    "type": "object",
    "required": ["title_en", "body_en", "title_hi", "body_hi", "meta_desc_en", "meta_desc_hi", "keywords_en", "keywords_hi"],
    "properties": {
        "title_en": {"type": "string", "minLength": 10, "maxLength": 200},
        "title_hi": {"type": "string", "minLength": 10, "maxLength": 200},
        "body_en": {"type": "string", "minLength": 100},
        "body_hi": {"type": "string", "minLength": 100},
        "meta_desc_en": {"type": "string", "minLength": 50, "maxLength": 160},
        "meta_desc_hi": {"type": "string", "minLength": 50, "maxLength": 160},
        "keywords_en": {"type": "string", "minLength": 10},
        "keywords_hi": {"type": "string", "minLength": 10}
    }
}


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type((requests.RequestException, json.JSONDecodeError))
)
def g_text(prompt: str) -> Dict:
    """
    Generate text content using Gemini API with retry logic
    
    Args:
        prompt: The prompt to send to the API
        
    Returns:
        Dict containing the generated content
        
    Raises:
        requests.RequestException: If API call fails after retries
        json.JSONDecodeError: If response is not valid JSON
    """
    try:
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={API}"
        response = requests.post(
            url,
            json={"contents": [{"parts": [{"text": prompt}]}]},
            timeout=90
        )
        response.raise_for_status()
        
        json_response = response.json()
        text_content = json_response["candidates"][0]["content"]["parts"][0]["text"]
        
        # Clean markdown code blocks if present
        text_content = re.sub(r'^```json\s*', '', text_content)
        text_content = re.sub(r'\s*```$', '', text_content)
        
        parsed = json.loads(text_content)
        logger.info("✓ Text generated successfully")
        return parsed
        
    except requests.RequestException as e:
        logger.error(f"Gemini API request error: {e}")
        raise
    except (KeyError, IndexError) as e:
        logger.error(f"Unexpected API response structure: {e}")
        raise requests.RequestException(f"Invalid API response: {e}")
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON response: {e}")
        logger.error(f"Response text: {text_content[:500]}")
        raise


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type(requests.RequestException)
)
def g_image(prompt: str, size: str = "1280x720") -> str:
    """
    Generate and optimize image using Gemini API
    
    Args:
        prompt: Topic/description for image generation
        size: Image dimensions
        
    Returns:
        Path to saved image (relative to site root)
        
    Raises:
        requests.RequestException: If API call fails after retries
    """
    try:
        # Use OpenAI DALL-E if API key is available, otherwise create placeholder
        if OPENAI_API_KEY and OPENAI_API_KEY.strip():
            url = "https://api.openai.com/v1/images/generations"
            enhanced_prompt = f"Professional Indian news editorial photograph about: {prompt}. Photorealistic, neutral tone, high quality, 16:9 aspect ratio."
            
            response = requests.post(
                url,
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "dall-e-3",
                    "prompt": enhanced_prompt,
                    "size": "1792x1024",
                    "quality": "standard",
                    "n": 1
                },
                timeout=120
            )
            response.raise_for_status()
            
            # Download the generated image
            image_url = response.json()["data"][0]["url"]
            img_response = requests.get(image_url, timeout=60)
            img_response.raise_for_status()
            img_data = img_response.content
            
            # Optimize image
            img = Image.open(BytesIO(img_data))
            img = optimize_image(img)
            
            # Save with content-based filename
            filename = hashlib.md5(enhanced_prompt.encode()).hexdigest()[:10] + ".jpg"
            filepath = IMGDIR / filename
            
            img.save(filepath, "JPEG", quality=IMAGE_QUALITY, optimize=True)
            logger.info(f"✓ Image generated and saved: {filename}")
            
            return f"/assets/images/{filename}"
        else:
            # Create placeholder image if no OpenAI key
            logger.warning("OPENAI_API_KEY not set, creating placeholder image")
            img = Image.new('RGB', (1792, 1024), color='#1a73e8')
            
            filename = hashlib.md5(topic.encode()).hexdigest()[:10] + ".jpg"
            filepath = IMGDIR / filename
            
            img.save(filepath, "JPEG", quality=IMAGE_QUALITY, optimize=True)
            logger.info(f"✓ Placeholder image created: {filename}")
            
            return f"/assets/images/{filename}"
        
    except requests.RequestException as e:
        logger.error(f"Image generation API error: {e}")
        # Fall back to placeholder on API failure
        logger.warning("Falling back to placeholder image due to API error")
        img = Image.new('RGB', (1792, 1024), color='#1a73e8')
        filename = hashlib.md5(topic.encode()).hexdigest()[:10] + ".jpg"
        filepath = IMGDIR / filename
        img.save(filepath, "JPEG", quality=IMAGE_QUALITY, optimize=True)
        logger.info(f"✓ Placeholder image created: {filename}")
        return f"/assets/images/{filename}"
    except Exception as e:
        logger.error(f"Image processing error: {e}")
        raise requests.RequestException(f"Image processing failed: {e}")


def optimize_image(img: Image.Image, max_width: int = MAX_IMAGE_WIDTH) -> Image.Image:
    """
    Resize and optimize image for web
    
    Args:
        img: PIL Image object
        max_width: Maximum width in pixels
        
    Returns:
        Optimized PIL Image
    """
    # Resize if necessary
    if img.width > max_width:
        ratio = max_width / img.width
        new_height = int(img.height * ratio)
        img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
        logger.info(f"✓ Image resized to {max_width}x{new_height}")
    
    # Convert to RGB if necessary (required for JPEG/WebP)
    if img.mode in ('RGBA', 'P', 'LA', 'L'):
        # Create white background for transparent images
        rgb_img = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'RGBA' or img.mode == 'LA':
            rgb_img.paste(img, mask=img.split()[-1])  # Use alpha channel as mask
        else:
            rgb_img.paste(img)
        img = rgb_img
        logger.info("✓ Image converted to RGB")
    
    return img


def truncate_text(text: Optional[str], max_len: int) -> Optional[str]:
    """
    Truncate text to max_len, preferring a nearby sentence boundary.

    Args:
        text: Input string (or None)
        max_len: Maximum allowed length

    Returns:
        Truncated string (or original if already within bounds)
    """
    if not text:
        return text
    if len(text) <= max_len:
        return text
    # Prefer truncating at a natural boundary close to the limit
    for sep in [". ", "! ", "? ", "\n"]:
        idx = text.rfind(sep, 0, max_len)
        if idx != -1 and idx > max_len - 120:
            return text[: idx + len(sep)].strip()
    return text[:max_len].rstrip() + "..."


def truncate_fields(data: Dict) -> Dict:
    """
    Apply safe truncation to fields that have max length constraints
    before schema validation or writing.

    Note: Limits align with POST_SCHEMA and SEO norms.
    """
    limits = {
        "title_en": 200,
        "title_hi": 200,
        "meta_desc_en": 160,
        "meta_desc_hi": 160,
        # Cap keywords length generously to avoid excessive meta size
        "keywords_en": 300,
        "keywords_hi": 300,
    }
    for key, max_len in limits.items():
        if key in data and isinstance(data[key], str):
            data[key] = truncate_text(data[key], max_len)
    return data


def prompt(topic: str) -> str:
    """
    Generate prompt for content creation
    
    Args:
        topic: News topic category
        
    Returns:
        Formatted prompt string
    """
    return f"""Generate a factual, balanced news article about: {topic}

Return ONLY valid JSON (no markdown formatting) with these exact fields:
{{
  "title_en": "Compelling English headline (50-150 chars)",
  "title_hi": "Engaging Hindi headline in Devanagari script (50-150 chars)",
  "body_en": "Comprehensive English article body ({WORDS} words, use markdown formatting, include facts and context)",
  "body_hi": "Complete Hindi translation in Devanagari script ({WORDS} words, maintain markdown formatting)",
  "meta_desc_en": "SEO-optimized English description (120-160 chars)",
  "meta_desc_hi": "SEO-optimized Hindi description in Devanagari (120-160 chars)",
  "keywords_en": "Relevant English keywords (comma-separated, 5-8 keywords)",
  "keywords_hi": "Relevant Hindi keywords in Devanagari (comma-separated, 5-8 keywords)"
}}

Requirements:
- Use CURRENT news from India (October 2025)
- Be factual, neutral, and professional
- No placeholder text or TODOs
- Hindi must use proper Devanagari script
- Include proper markdown headings (##) and lists where appropriate"""


def validate_content(data: Dict) -> List[str]:
    """
    Validate generated content for quality issues
    
    Args:
        data: Generated content dictionary
        
    Returns:
        List of validation error messages (empty if valid)
    """
    issues = []
    
    # Check for placeholder text
    placeholders = ['lorem ipsum', '[insert', 'TODO', 'XXX', 'placeholder', 'example.com']
    for key, text in data.items():
        if isinstance(text, str):
            for placeholder in placeholders:
                if placeholder.lower() in text.lower():
                    issues.append(f"Contains placeholder '{placeholder}' in {key}")
    
    # Check minimum word count
    en_words = len(data['body_en'].split())
    if en_words < 100:
        issues.append(f"English content too short ({en_words} words, minimum 100)")
    
    hi_words = len(data['body_hi'].split())
    if hi_words < 50:
        issues.append(f"Hindi content too short ({hi_words} words, minimum 50)")
    
    # Check for proper Hindi Devanagari script
    hindi_chars = re.findall(r'[\u0900-\u097F]', data['body_hi'])
    if len(hindi_chars) < 50:
        issues.append("Insufficient Hindi Devanagari characters (may not be properly translated)")
    
    # Check for broken markdown
    if data['body_en'].count('```') % 2 != 0:
        issues.append("Unclosed code blocks in English content")
    if data['body_hi'].count('```') % 2 != 0:
        issues.append("Unclosed code blocks in Hindi content")
    
    # Check meta description length
    if len(data['meta_desc_en']) > 160:
        issues.append(f"English meta description too long ({len(data['meta_desc_en'])} chars, max 160)")
    if len(data['meta_desc_hi']) > 160:
        issues.append(f"Hindi meta description too long ({len(data['meta_desc_hi'])} chars, max 160)")
    
    return issues


def slug(s: str) -> str:
    """
    Create URL-friendly slug from string
    
    Args:
        s: Input string
        
    Returns:
        URL-safe slug
    """
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def cat_from(topic: str) -> str:
    """
    Determine category from topic string
    
    Args:
        topic: Topic description
        
    Returns:
        Category name
    """
    topic_lower = topic.lower()
    if "politic" in topic_lower or "government" in topic_lower:
        return "Politics"
    if "business" in topic_lower or "economy" in topic_lower:
        return "Business"
    if "tech" in topic_lower or "innovation" in topic_lower:
        return "Technology"
    if "finance" in topic_lower or "taxation" in topic_lower or "savings" in topic_lower:
        return "Finance"
    return "Startups"


def write_post(data: Dict, img_path: str, topic: str) -> None:
    """
    Write post to markdown file with atomic write operation
    
    Args:
        data: Content dictionary
        img_path: Path to featured image
        topic: Topic category
        
    Raises:
        IOError: If file write fails
    """
    category = cat_from(topic)
    date = datetime.date.today()
    post_slug = slug(data['title_en'])[:60]
    filename = f"{date}-{post_slug}.md"
    final_path = POSTS / filename
    
    # Check for collision
    if final_path.exists():
        logger.warning(f"Post already exists: {filename}")
        return
    
    # Prepare front matter
    front_matter = f"""---
layout: post
title: "{data['title_en']}"
category: "{category}"
description: "{data['meta_desc_en']}"
keywords: "{data['keywords_en']}, {data['keywords_hi']}"
image: {img_path}
image_alt: "News illustration for {data['title_en']}"
body_hi: |
{textwrap.indent(data['body_hi'], '  ')}
meta_desc_hi: "{data['meta_desc_hi']}"
title_hi: "{data['title_hi']}"
---
"""
    
    content = front_matter + data['body_en'] + "\n"
    
    # Atomic write using temporary file
    try:
        with tempfile.NamedTemporaryFile(
            mode='w',
            encoding='utf-8',
            delete=False,
            dir=POSTS,
            suffix='.md'
        ) as tmp:
            tmp.write(content)
            tmp_path = tmp.name
        
        shutil.move(tmp_path, final_path)
        logger.info(f"✅ Post written successfully: {filename}")
        
    except Exception as e:
        logger.error(f"Failed to write post: {e}")
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise


def main():
    """Main execution function - generates posts for all categories"""
    try:
        total_topics = len(TOPICS)
        successful_posts = 0
        failed_posts = 0
        
        logger.info(f"📰 Starting hourly post generation for all {total_topics} categories")
        logger.info("=" * 60)
        
        # Generate posts for each topic/category
        for idx, topic in enumerate(TOPICS, 1):
            try:
                logger.info(f"\n[{idx}/{total_topics}] Processing: {topic}")
                logger.info("-" * 60)
                
                # Generate content
                logger.info("Generating text content...")
                content_prompt = prompt(topic)
                data = g_text(content_prompt)
                # Ensure fields with max length constraints are truncated
                # before schema validation to avoid length errors
                data = truncate_fields(data)
                
                # Validate JSON schema
                try:
                    validate(instance=data, schema=POST_SCHEMA)
                    logger.info("✓ JSON schema validated")
                except ValidationError as e:
                    logger.error(f"JSON validation failed: {e.message}")
                    failed_posts += 1
                    continue
                
                # Validate content quality
                validation_errors = validate_content(data)
                if validation_errors:
                    logger.error("Content validation failed:")
                    for error in validation_errors:
                        logger.error(f"  - {error}")
                    failed_posts += 1
                    continue
                logger.info("✓ Content quality validated")
                
                # Generate image
                logger.info("Generating image...")
                img_path = g_image(topic)
                
                # Write post (fields already truncated where applicable)
                logger.info("Writing post file...")
                write_post(data, img_path, topic)
                
                logger.info(f"✓ Post [{idx}/{total_topics}] completed successfully!")
                successful_posts += 1
                
                # Add a small delay between posts to avoid rate limiting
                if idx < total_topics:
                    logger.info("Waiting 2 seconds before next post...")
                    time.sleep(2)
                
            except KeyboardInterrupt:
                logger.info("Operation cancelled by user")
                sys.exit(130)
            except Exception as e:
                logger.error(f"Error generating post for '{topic}': {e}", exc_info=True)
                failed_posts += 1
                continue
        
        # Summary
        logger.info("\n" + "=" * 60)
        logger.info("🎉 Hourly post generation completed!")
        logger.info(f"✓ Successful: {successful_posts}/{total_topics}")
        if failed_posts > 0:
            logger.warning(f"✗ Failed: {failed_posts}/{total_topics}")
        logger.info("=" * 60)
        
        # Exit with error if all posts failed
        if successful_posts == 0:
            logger.error("All posts failed to generate")
            sys.exit(1)
        
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    POSTS.mkdir(exist_ok=True)
    main()
