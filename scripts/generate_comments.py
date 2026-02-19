#!/usr/bin/env python3
"""
Generate Comments section for Daily Tech Review using Claude API.

Usage:
    python scripts/generate_comments.py _posts/ko/2026-02-19-daily.md
"""

import os
import sys
import re
from anthropic import Anthropic


def read_post(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def extract_body(content):
    """Extract post body (before ## Comments section)."""
    # Remove front matter
    body = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
    # Remove everything from ## Comments onwards
    body = re.split(r'\n## Comments\n', body)[0]
    return body.strip()


def generate_comments(body, lang='ko'):
    """Generate Comments using Claude API."""
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    if lang == 'ko':
        prompt = f"""아래는 오늘의 Daily Tech Review 포스트 본문입니다.
3개 토픽을 종합하여 취업 준비생 관점에서 간결한 코멘트 3개를 작성하세요.

[포스트 본문]
{body[:3000]}

출력 형식 (이 줄들만 출력):
- **산업 연관성**: (이 소식들이 산업에 미치는 통합 인사이트, 2문장)
- **직무 연관성**: (개발자/PM/데이터 직무 지원자에게 실질적 의미, 2문장)
- **자소서/면접**: (면접에서 활용할 수 있는 포인트 1~2개, 구체적으로)"""
    else:
        prompt = f"""Below is today's Daily Tech Review post content.
Synthesize the topics and write 3 concise comments from a job seeker's perspective.

[Post Content]
{body[:3000]}

Output format (these lines only):
- **Industry Insight**: (Integrated insight on how these news items affect the industry, 2 sentences)
- **Career Relevance**: (Practical meaning for developer/PM/data job applicants, 2 sentences)
- **Interview Prep**: (1-2 specific points to use in interviews or cover letters)"""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text.strip()


def update_post(file_path, comments):
    """Replace empty Comments section with generated comments."""
    content = read_post(file_path)

    if '## Comments\n' not in content:
        print(f"Warning: ## Comments section not found in {file_path}")
        return

    parts = content.split('## Comments\n', 1)
    new_content = parts[0] + '## Comments\n' + comments + '\n'

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/generate_comments.py <post_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    lang = 'ko' if '/ko/' in file_path else 'en'

    print(f"Reading post: {file_path}")
    content = read_post(file_path)

    print("Extracting body...")
    body = extract_body(content)
    if not body:
        print("Error: Could not extract post body")
        sys.exit(1)

    print(f"Generating comments ({lang})...")
    comments = generate_comments(body, lang)

    print("Updating post...")
    update_post(file_path, comments)
    print(f"✓ Comments updated: {file_path}")


if __name__ == "__main__":
    main()
