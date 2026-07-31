#!/usr/bin/env python3
import sys
import re
from pathlib import Path
from datetime import datetime

def parse_md(md_content):
    lines = md_content.split('\n')
    
    title = "Untitled"
    date = datetime.now().strftime("%Y-%m-%d")
    content_start = 0
    
    for i, line in enumerate(lines):
        if line.startswith('# '):
            title = line[2:].strip()
            content_start = i + 1
            break
    
    for i, line in enumerate(lines):
        if line.startswith('**Date:**'):
            date = line.replace('**Date:**', '').strip()
            if content_start == 0:
                content_start = i + 1
            break
    
    for i, line in enumerate(lines[content_start:], start=content_start):
        if line.strip() == '---':
            content_start = i + 1
            break
    
    md_body = '\n'.join(lines[content_start:])
    return title, date, md_body

def md_to_html(md_text):
    html = md_text
    
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (?!Date:)(.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    
    html = re.sub(r'```([\s\S]*?)```', r'<pre><code>\1</code></pre>', html)
    html = re.sub(r'`(.+?)`', r'<code>\1</code>', html)
    
    html = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)
    
    html = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', html)
    
    lines = html.split('\n')
    in_list = False
    processed_lines = []
    for line in lines:
        if re.match(r'^- (.+)$', line):
            if not in_list:
                processed_lines.append('<ul>')
                in_list = True
            item = re.sub(r'^- (.+)$', r'<li>\1</li>', line)
            processed_lines.append(item)
        else:
            if in_list:
                processed_lines.append('</ul>')
                in_list = False
            processed_lines.append(line)
    if in_list:
        processed_lines.append('</ul>')
    html = '\n'.join(processed_lines)
    
    paragraphs = html.split('\n\n')
    html = ''
    for p in paragraphs:
        p = p.strip()
        if p and not p.startswith('<'):
            html += f'<p>{p}</p>\n'
        else:
            html += p + '\n'
    
    return html

def main():
    if len(sys.argv) < 2:
        print("Использование: python add_article.py <article.md>")
        print("\nФормат статьи:")
        print("# Заголовок")
        print("**Date:** YYYY-MM-DD")
        print("---")
        print("контент в markdown...")
        sys.exit(1)
    
    md_file = Path(sys.argv[1])
    if not md_file.exists():
        print(f"Файл {md_file} не найден!")
        sys.exit(1)
    
    md_content = md_file.read_text(encoding='utf-8')
    title, date, md_body = parse_md(md_content)
    
    html_content = md_to_html(md_body)
    
    def translit(text):
        mapping = {
            'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
            'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
            'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
            'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '',
            'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
            'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'Yo',
            'Ж': 'Zh', 'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M',
            'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
            'Ф': 'F', 'Х': 'H', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Sch', 'Ъ': '',
            'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya'
        }
        result = ''
        for char in text:
            result += mapping.get(char, char)
        return result
    
    slug = translit(title).lower().replace(' ', '-').replace('.', '').replace(',', '')
    slug = re.sub(r'[^a-z0-9\-]', '', slug)
    if not slug:
        slug = 'article-' + datetime.now().strftime('%Y%m%d')
    output_file = Path('articles') / f"{slug}.html"
    
    template_path = Path('articles') / 'template.html'
    if not template_path.exists():
        print("Шаблон template.html не найден в articles/")
        sys.exit(1)
    
    template = template_path.read_text(encoding='utf-8')
    
    final_html = template.replace('{{TITLE}}', title)
    final_html = final_html.replace('{{DATE}}', date)
    final_html = final_html.replace('{{CONTENT}}', html_content)
    
    output_file.write_text(final_html, encoding='utf-8')
    print(f"✓ Статья создана: {output_file}")
    print(f"  Заголовок: {title}")
    print(f"  Дата: {date}")
    
    print(f"\nДобавьте эту строку в archive.html:")
    print(f'  <div class="ln"><a href="./articles/{output_file.name}">{title}</a> <span class="d">........ {date}</span></div>')

if __name__ == '__main__':
    main()
