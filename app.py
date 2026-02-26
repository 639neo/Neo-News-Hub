#!/usr/bin/env python3
"""Neo News Hub - Blog/Magazine Application"""

import os
import json
import glob
from datetime import datetime
from flask import Flask, render_template, request, jsonify, abort
from markupsafe import Markup
import markdown

app = Flask(__name__)

POSTS_DIR = os.path.join(os.path.dirname(__file__), 'posts')

def get_all_posts(sort_by='date', reverse=True):
    posts = []
    for filepath in glob.glob(os.path.join(POSTS_DIR, '*.json')):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                post = json.load(f)
                post['slug'] = os.path.splitext(os.path.basename(filepath))[0]
                posts.append(post)
        except Exception:
            pass
    posts.sort(key=lambda x: x.get('date', ''), reverse=reverse)
    return posts

def get_post(slug):
    filepath = os.path.join(POSTS_DIR, f'{slug}.json')
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        post = json.load(f)
        post['slug'] = slug
        return post

def render_content(content):
    return Markup(markdown.markdown(content, extensions=['extra', 'nl2br']))

@app.route('/')
def index():
    posts = get_all_posts()
    return render_template('index.html', posts=posts)

@app.route('/posts')
def all_posts():
    query = request.args.get('q', '').lower()
    tag = request.args.get('tag', '')
    posts = get_all_posts()
    
    all_tags = set()
    for p in posts:
        for t in p.get('tags', []):
            all_tags.add(t)
    
    if query:
        posts = [p for p in posts if 
                 query in p.get('title', '').lower() or 
                 query in p.get('excerpt', '').lower() or
                 query in p.get('content', '').lower()]
    if tag:
        posts = [p for p in posts if tag in p.get('tags', [])]
    
    return render_template('posts.html', posts=posts, query=query, tag=tag, all_tags=sorted(all_tags))

@app.route('/post/<slug>')
def post_detail(slug):
    post = get_post(slug)
    if not post:
        abort(404)
    post['rendered_content'] = render_content(post.get('content', ''))
    all_posts = get_all_posts()
    recent = [p for p in all_posts if p['slug'] != slug][:3]
    return render_template('post.html', post=post, recent=recent)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/api/posts', methods=['GET'])
def api_posts():
    posts = get_all_posts()
    return jsonify(posts)

@app.route('/api/post', methods=['POST'])
def api_create_post():
    """API endpoint to create a new post"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data'}), 400
    
    required = ['title', 'content']
    for r in required:
        if r not in data:
            return jsonify({'error': f'Missing field: {r}'}), 400
    
    # Generate slug from title
    slug = data['title'].lower()
    slug = ''.join(c if c.isalnum() or c == '-' else '-' for c in slug)
    slug = '-'.join(filter(None, slug.split('-')))
    
    # Add timestamp to ensure uniqueness
    ts = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    slug = f"{slug}-{ts}"
    
    post = {
        'title': data['title'],
        'content': data['content'],
        'excerpt': data.get('excerpt', data['content'][:200] + '...'),
        'author': data.get('author', 'Neo'),
        'date': data.get('date', datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')),
        'tags': data.get('tags', []),
        'thumbnail': data.get('thumbnail', ''),
        'thumbnail_alt': data.get('thumbnail_alt', data['title'])
    }
    
    filepath = os.path.join(POSTS_DIR, f'{slug}.json')
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(post, f, indent=2, ensure_ascii=False)
    
    return jsonify({'success': True, 'slug': slug}), 201

if __name__ == '__main__':
    os.makedirs(POSTS_DIR, exist_ok=True)
    app.run(host='0.0.0.0', port=8080, debug=False)
