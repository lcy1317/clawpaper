#!/usr/bin/env python3
"""落先生的文献小窝 - 信任度评估专题"""

from flask import Flask, render_template_string, send_from_directory, jsonify
import os
import json
from datetime import datetime

app = Flask(__name__)
LITERATURE_DIR = "/root/.openclaw/workspace/literature"

def load_papers():
    with open(os.path.join(LITERATURE_DIR, "papers.json"), "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("papers", []), data.get("statistics", {})

PAPERS_DATA, STATS = load_papers()

SUMMARY = """
落先生，小女仆的学习总结来啦！

信任度评估的核心方法：

1. 数学框架方法
   - 基于信息论的量化方法
   - 信任传播的数学建模
   - 信任公理化定义

2. 4C概念框架
   - Context (情境): 信任产生的环境
   - Computing (计算): 信任值的计算方法
   - Criteria (标准): 评估信任的标准
   - Confidence (置信度): 信任的可靠性

3. 区块链信任模型
   - 去中心化声誉管理
   - 分布式信任存储
   - 抗恶意攻击机制

小女仆的感悟：
信任评估是一个跨学科的研究领域，需要结合
数学、密码学、博弈论和社会学等多个领域的知识呢～
"""

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>落先生的文献小窝 - 信任度评估专题</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: "Segoe UI", "Microsoft YaHei", sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1500px; margin: 0 auto; }
        .header {
            text-align: center;
            padding: 40px 20px;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            margin-bottom: 30px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
        }
        .header h1 {
            font-size: 2.5em;
            background: linear-gradient(45deg, #667eea, #764ba2, #f093fb);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .mascot { font-size: 4em; margin: 20px 0; animation: bounce 2s infinite; }
        @keyframes bounce { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
        .controls { display: flex; justify-content: center; gap: 15px; margin: 20px 0; flex-wrap: wrap; }
        .sort-btn { padding: 12px 25px; border: none; border-radius: 25px; cursor: pointer; font-weight: bold; color: white; transition: all 0.3s; }
        .sort-btn:hover { transform: scale(1.05); }
        .sort-q1 { background: linear-gradient(135deg, #2ecc71, #27ae60); }
        .sort-q2 { background: linear-gradient(135deg, #f39c12, #e67e22); }
        .sort-if { background: linear-gradient(135deg, #e74c3c, #c0392b); }
        .sort-default { background: linear-gradient(135deg, #667eea, #764ba2); }
        .stats { display: flex; justify-content: center; gap: 15px; margin: 15px 0; flex-wrap: wrap; }
        .stat-item { padding: 10px 18px; border-radius: 12px; font-weight: bold; color: white; }
        .stat-total { background: linear-gradient(135deg, #667eea, #764ba2); }
        .stat-q1 { background: linear-gradient(135deg, #2ecc71, #27ae60); }
        .stat-q2 { background: linear-gradient(135deg, #f39c12, #e67e22); }
        .summary-card {
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
        }
        .summary-card h2 { color: #333; margin-bottom: 20px; }
        .summary-content { background: rgba(255, 255, 255, 0.9); border-radius: 15px; padding: 25px; line-height: 1.8; color: #444; white-space: pre-wrap; }
        .papers-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(420px, 1fr)); gap: 25px; margin-bottom: 30px; }
        .paper-card {
            background: white;
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
            transition: all 0.3s ease;
        }
        .paper-card:hover { transform: translateY(-5px); box-shadow: 0 15px 50px rgba(0, 0, 0, 0.25); }
        .paper-title { color: #667eea; margin-bottom: 10px; font-size: 1.05em; line-height: 1.4; }
        .paper-meta { color: #888; font-size: 0.85em; margin-bottom: 12px; }
        .journal-badges { display: flex; gap: 8px; margin-bottom: 15px; flex-wrap: wrap; }
        .badge { padding: 5px 10px; border-radius: 15px; font-size: 0.75em; font-weight: bold; color: white; }
        .badge-ranking { background: #667eea; }
        .badge-type { background: #764ba2; }
        .badge-if { background: #27ae60; }
        .badge-publisher { background: #3498db; }
        .paper-abstract { background: #f8f9fa; border-radius: 10px; padding: 15px; margin-bottom: 15px; font-size: 0.9em; color: #555; line-height: 1.6; }
        .paper-tags { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 15px; }
        .tag { background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 4px 10px; border-radius: 15px; font-size: 0.75em; }
        .trust-dimensions {
            background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%);
            border-radius: 12px;
            padding: 18px;
            margin-bottom: 18px;
        }
        .trust-dimensions h4 { color: #333; margin-bottom: 12px; font-size: 0.95em; }
        .dimension-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; }
        .dimension-item { background: rgba(255, 255, 255, 0.9); border-radius: 8px; padding: 10px; font-size: 0.8em; }
        .dimension-key { font-weight: bold; color: #667eea; margin-bottom: 4px; }
        .dimension-value { color: #555; font-size: 0.9em; }
        .bibtex-section { background: #282c34; border-radius: 12px; padding: 18px; margin-top: 15px; }
        .bibtex-section h4 { color: #61dafb; margin-bottom: 12px; }
        .bibtex-code {
            background: #1e2127;
            border-radius: 8px;
            padding: 12px;
            color: #abb2bf;
            font-family: "Courier New", monospace;
            font-size: 0.75em;
            overflow-x: auto;
            white-space: pre-wrap;
            word-break: break-all;
        }
        .copy-btn { background: #61dafb; color: #282c34; border: none; padding: 8px 15px; border-radius: 8px; cursor: pointer; font-size: 0.85em; margin-top: 10px; }
        .action-btns { display: flex; gap: 10px; flex-wrap: wrap; }
        .btn { flex: 1; padding: 10px 18px; border-radius: 25px; text-decoration: none; font-weight: bold; text-align: center; border: none; transition: all 0.3s; min-width: 100px; font-size: 0.9em; }
        .btn-download { background: linear-gradient(135deg, #e74c3c, #c0392b); color: white; }
        .btn-access { background: linear-gradient(135deg, #2ecc71, #27ae60); color: white; }
        .btn-bibtex { background: linear-gradient(135deg, #11998e, #38ef7d); color: white; }
        .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); z-index: 1000; justify-content: center; align-items: center; padding: 20px; }
        .modal.active { display: flex; }
        .modal-content { background: white; border-radius: 20px; max-width: 850px; width: 100%; max-height: 90vh; overflow-y: auto; padding: 30px; }
        .modal-close { float: right; font-size: 1.5em; cursor: pointer; color: #999; }
        .footer { text-align: center; padding: 30px; color: white; }
        .footer .heart { color: #ff6b6b; animation: heartbeat 1s infinite; }
        @keyframes heartbeat { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.1); } }
        @media (max-width: 768px) { .papers-grid { grid-template-columns: 1fr; } .header h1 { font-size: 1.8em; } }
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <div class="mascot">🐱✨</div>
            <h1>落先生的文献小窝</h1>
            <p class="subtitle">信任度评估系统专题 - 学术文献资源库</p>
            <div class="controls">
                <button class="sort-btn sort-default" onclick="sortPapers('default')">默认排序</button>
                <button class="sort-btn sort-q1" onclick="sortPapers('q1')">仅SCI Q1</button>
                <button class="sort-btn sort-q2" onclick="sortPapers('q2')">仅SCI Q2</button>
                <button class="sort-btn sort-if" onclick="sortPapers('if_desc')">影响因子↓</button>
                <button class="sort-btn sort-if" onclick="sortPapers('if_asc')">影响因子↑</button>
            </div>
            <div class="stats">
                <div class="stat-item stat-total">共 PAPERS_COUNT 篇文献</div>
                <div class="stat-item stat-q1">SCI Q1: STATS_Q1</div>
                <div class="stat-item stat-q2">SCI Q2: STATS_Q2</div>
            </div>
            <p style="color: #999; margin-top: 10px; font-size: 0.9em;">整理日期：CURRENT_DATE</p>
        </header>
        <section class="summary-card">
            <h2>小女仆的学习总结 💕</h2>
            <div class="summary-content">SUMMARY_CONTENT</div>
        </section>
        <h2 style="color: white; margin-bottom: 20px; text-align: center;">学术文献 (点击查看 BibTeX 和信任维度)</h2>
        <div class="papers-grid" id="papersGrid">PAPERS_HTML</div>
        <footer class="footer"><p>Made with ♥ for 落先生 🐱</p><p style="opacity:0.8;margin-top:10px">信任是任何分布式系统的核心挑战</p></footer>
    </div>
    <div class="modal" id="paperModal">
        <div class="modal-content"><span class="modal-close" onclick="closeModal()">&times;</span><div id="modalBody"></div></div>
    </div>
    <script>
        let allPapers = PAPERS_JSON;
        let currentSort = 'default';
        function showModal(paperId) {
            const paper = allPapers.find(p => p.id === paperId);
            if (!paper) return;
            let journalInfoHtml = '';
            if (paper.journal_info) {
                const journal = paper.journal_info;
                const impactLabel = journal.impact_factor_label || '';
                const accessUrl = journal.access_url || '';
                const notes = journal.notes || '';
                journalInfoHtml = '<div class="journal-badges" style="margin: 15px 0;">' +
                    '<span class="badge badge-ranking">' + (journal.ranking || 'N/A') + '</span>' +
                    '<span class="badge badge-type">' + ((journal.type || 'N/A').split(' ')[0]) + '</span>' +
                    (impactLabel ? '<span class="badge badge-if">' + impactLabel + '</span>' : '') +
                    '<span class="badge badge-publisher">' + (journal.publisher || 'N/A') + '</span></div>' +
                    '<p style="color: #666; margin-bottom: 15px;"><strong>访问链接：</strong>' +
                    (accessUrl ? '<a href="' + accessUrl + '" target="_blank" style="color: #667eea;">点击访问</a>' : '无') + '</p>' +
                    (journal.doi ? '<p style="color: #666; margin-bottom: 15px;"><strong>DOI：</strong>' + journal.doi + '</p>' : '') +
                    (notes ? '<p style="color: #888; font-size: 0.9em; margin-bottom: 15px;"><strong>备注：</strong>' + notes + '</p>' : '');
            }
            let dimensionsHtml = '';
            if (paper.trust_dimensions) {
                const dims = Object.entries(paper.trust_dimensions).map(([k, v]) => 
                    '<div class="dimension-item"><div class="dimension-key">' + k + '</div><div class="dimension-value">' + v + '</div></div>'
                ).join('');
                dimensionsHtml = '<div class="trust-dimensions"><h4>🎯 信任维度分析</h4><div class="dimension-list">' + dims + '</div></div>';
            }
            document.getElementById('modalBody').innerHTML = 
                '<h2 style="color:#667eea;margin-bottom:15px;font-size:1.2em">' + paper.title + '</h2>' +
                '<div style="color:#666;margin-bottom:15px;line-height:1.8">' +
                '<strong>作者：</strong>' + paper.authors + '<br>' +
                '<strong>年份：</strong>' + paper.year + '<br>' +
                '<strong>会议/期刊：</strong>' + paper.venue + '<br>' +
                '<strong>机构：</strong>' + paper.institution + '</div>' +
                journalInfoHtml + dimensionsHtml +
                '<div class="bibtex-section"><h4>📋 IEEE BibTeX 引用格式</h4><div class="bibtex-code" id="bibtexContent">' + paper.bibtex + '</div><button class="copy-btn" onclick="copyBibtex()">复制 BibTeX</button></div>';
            document.getElementById('paperModal').classList.add('active');
        }
        function closeModal() { document.getElementById('paperModal').classList.remove('active'); }
        function copyBibtex() {
            const content = document.getElementById('bibtexContent').innerText;
            navigator.clipboard.writeText(content).then(() => alert('BibTeX 已复制到剪贴板！'));
        }
        function sortPapers(sortType) {
            currentSort = sortType;
            const grid = document.getElementById('papersGrid');
            const cards = Array.from(grid.children);
            cards.sort((a, b) => {
                if (sortType === 'default') return 0;
                if (sortType === 'q1') {
                    return ((b.dataset.ranking === 'SCI Q1') ? 1 : 0) - ((a.dataset.ranking === 'SCI Q1') ? 1 : 0);
                }
                if (sortType === 'q2') {
                    return ((a.dataset.ranking === 'SCI Q2') ? 1 : 0) - ((b.dataset.ranking === 'SCI Q2') ? 1 : 0);
                }
                if (sortType === 'if_desc') {
                    return (parseFloat(b.dataset.if) || 0) - (parseFloat(a.dataset.if) || 0);
                }
                if (sortType === 'if_asc') {
                    return (parseFloat(a.dataset.if) || 0) - (parseFloat(b.dataset.if) || 0);
                }
                return 0;
            });
            cards.forEach(card => grid.appendChild(card));
        }
        document.getElementById('paperModal').addEventListener('click', function(e) { if (e.target === this) closeModal(); });
    </script>
</body>
</html>
"""

def generate_papers_html(papers):
    html_parts = []
    for paper in papers:
        journal_info = paper.get('journal_info', {})
        ranking = journal_info.get('ranking', '') if journal_info else ''
        impact = journal_info.get('impact_factor', 0) if journal_info else 0
        impact_label = journal_info.get('impact_factor_label', '') if journal_info else ''
        paper_type = (journal_info.get('type', '') if journal_info else '').split(' ')[0]
        publisher = journal_info.get('publisher', '') if journal_info else ''
        access_url = journal_info.get('access_url', '') if journal_info else ''
        downloadable = journal_info.get('downloadable', False) if journal_info else False
        
        tags_html = ''.join(['<span class="tag">' + tag + '</span>' for tag in paper.get('tags', [])])
        
        btn_download = ''
        if paper.get('file'):
            btn_download = '<a href="/download/' + paper['file'] + '" class="btn btn-download">📥 PDF</a>'
        elif downloadable and access_url:
            btn_download = '<a href="' + access_url + '" target="_blank" class="btn btn-download">📥 PDF</a>'
        
        btn_access = ''
        if access_url:
            btn_access = '<a href="' + access_url + '" target="_blank" class="btn btn-access">🔗 访问</a>'
        
        card_html = '''
            <article class="paper-card" data-ranking="RANKING" data-if="IMPACT">
                <h3 class="paper-title">TITLE</h3>
                <div class="paper-meta"><strong>AUTHORS</strong><br>📅 YEAR | 🏛️ INSTITUTION</div>
                <div class="journal-badges">
                    <span class="badge badge-ranking">RANKING_DISPLAY</span>
                    <span class="badge badge-type">TYPE</span>
                    IF_LABEL
                    <span class="badge badge-publisher">PUBLISHER</span>
                </div>
                <div class="paper-abstract"><strong>摘要：</strong><br>ABSTRACT</div>
                <div class="paper-tags">TAGS</div>
                <div class="action-btns">
                    BTN_DOWNLOAD
                    BTN_ACCESS
                    <button class="btn btn-bibtex" onclick="showModal(\'ID\')">📋 详情</button>
                </div>
            </article>
        '''.replace('TITLE', paper['title'])\
          .replace('AUTHORS', ', '.join(paper['authors']))\
          .replace('YEAR', str(paper['year']))\
          .replace('INSTITUTION', paper['institution'])\
          .replace('RANKING', ranking)\
          .replace('RANKING_DISPLAY', ranking or 'N/A')\
          .replace('TYPE', paper_type or 'N/A')\
          .replace('IF_LABEL', ('<span class="badge badge-if">' + impact_label + '</span>') if impact_label else '')\
          .replace('PUBLISHER', publisher)\
          .replace('IMPACT', str(impact))\
          .replace('ABSTRACT', paper['abstract'])\
          .replace('TAGS', tags_html)\
          .replace('BTN_DOWNLOAD', btn_download)\
          .replace('BTN_ACCESS', btn_access)\
          .replace('ID', paper['id'])
        
        html_parts.append(card_html)
    return ''.join(html_parts)

@app.route('/')
def index():
    html = HTML_TEMPLATE
    html = html.replace('PAPERS_COUNT', str(len(PAPERS_DATA)))
    html = html.replace('STATS_Q1', str(STATS.get('sci_q1', 0)))
    html = html.replace('STATS_Q2', str(STATS.get('sci_q2', 0)))
    html = html.replace('CURRENT_DATE', datetime.now().strftime("%Y年%m月%d日"))
    html = html.replace('SUMMARY_CONTENT', SUMMARY)
    html = html.replace('PAPERS_JSON', json.dumps(PAPERS_DATA, ensure_ascii=False))
    html = html.replace('PAPERS_HTML', generate_papers_html(PAPERS_DATA))
    return html

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(LITERATURE_DIR, filename, as_attachment=True)

@app.route('/api/papers')
def api_papers():
    return jsonify({"papers": PAPERS_DATA, "stats": STATS, "summary": SUMMARY.strip()})

if __name__ == '__main__':
    print("🐱 落先生的文献小窝启动啦！")
    print("📍 访问地址：http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
