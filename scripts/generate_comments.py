#!/usr/bin/env python3
"""
Generate Comments section for Daily Digest using Claude API.

Usage:
    python scripts/generate_comments.py _posts/ko/2026-02-17-daily-digest.md
"""

import os
import sys
import re
from anthropic import Anthropic

def read_post(file_path):
    """Read the Daily Digest post."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_summary(content):
    """Extract '오늘의 핵심 요약' section."""
    match = re.search(r'## 오늘의 핵심 요약\n\n(.*?)\n\n##', content, re.DOTALL)
    if match:
        return match.group(1).strip()
    # Try English version
    match = re.search(r'## Today\'s Key Summary\n\n(.*?)\n\n##', content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""

def generate_comments(summary, lang='ko'):
    """Generate Comments using Claude API."""
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    if lang == 'ko':
        prompt = f"""다음은 오늘의 테크 뉴스 요약입니다:

{summary}

이 요약을 바탕으로 다음 3가지 관점에서 1-2문장씩 코멘트를 작성해주세요:

1. **산업 연관성**: 이 동향이 산업 전반에 어떤 영향을 미칠지
2. **직무 연관성**: 개발자/엔지니어 관점에서 어떤 역량이 중요해지는지
3. **자소서·면접**: 면접에서 어떤 질문이 나올 수 있고 어떻게 대비할지

형식:
- **산업 연관성**: [1-2문장]
- **직무 연관성**: [1-2문장]
- **자소서·면접**: [1-2문장]"""
    else:  # en
        prompt = f"""Here's today's tech news summary:

{summary}

Based on this summary, write 1-2 sentence comments for each of these 3 perspectives:

1. **Industry Relevance**: How this trend will impact the industry overall
2. **Role Relevance**: What capabilities become important from developer/engineer perspective
3. **Interview Prep**: What interview questions might come up and how to prepare

Format:
- **Industry Relevance**: [1-2 sentences]
- **Role Relevance**: [1-2 sentences]
- **Interview Prep**: [1-2 sentences]"""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return message.content[0].text

def update_post(file_path, comments):
    """Update the post with generated comments."""
    content = read_post(file_path)

    # Replace Comments placeholder
    updated = re.sub(
        r'{{ COMMENTS_PLACEHOLDER }}',
        comments,
        content
    )

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(updated)

def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/generate_comments.py <post_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    # Detect language
    lang = 'ko' if '/ko/' in file_path else 'en'

    print(f"Reading post: {file_path}")
    content = read_post(file_path)

    print("Extracting summary...")
    summary = extract_summary(content)
    if not summary:
        print("Error: Could not extract summary section")
        sys.exit(1)

    print(f"Generating comments ({lang})...")
    comments = generate_comments(summary, lang)

    print("Updating post...")
    update_post(file_path, comments)

    print(f"✓ Comments generated and updated in {file_path}")

if __name__ == "__main__":
    main()
