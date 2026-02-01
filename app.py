#!/usr/bin/env python3
"""落先生的文献小窝 - 信任度评估专题 V2.0"""

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

# 提取所有唯一维度
ALL_DIMENSIONS = set()
for paper in PAPERS_DATA:
    if paper.get("trust_dimensions"):
        ALL_DIMENSIONS.update(paper["trust_dimensions"].keys())

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
    <title>落先生的文献小窝 V2.0 - 信任度评估专题</title>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Noto Sans SC', 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            min-height: 100vh;
            color: #e0e0e0;
        }
        .container { max-width: 1600px; margin: 0 auto; padding: 20px; }
        
        .header {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 24px;
            padding: 40px;
            margin-bottom: 30px;
            text-align: center;
        }
        .header h1 {
            font-size: 2.8em;
            background: linear-gradient(90deg, #667eea, #764ba2, #f093fb, #667eea);
            background-size: 300% 300%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: gradientShift 5s ease infinite;
            margin-bottom: 10px;
        }
        @keyframes gradientShift {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        .subtitle { color: #a0a0a0; font-size: 1.1em; margin-bottom: 20px; }
        .mascot { font-size: 3.5em; margin: 15px 0; animation: bounce 2s infinite; }
        @keyframes bounce { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
        
        .stats-bar { display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin: 25px 0; }
        .stat-card {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 20px 30px;
            text-align: center;
            transition: all 0.3s ease;
        }
        .stat-card:hover { transform: translateY(-5px); border-color: rgba(102, 126, 234, 0.5); }
        .stat-number { font-size: 2em; font-weight: 700; color: #667eea; }
        .stat-label { color: #888; font-size: 0.9em; margin-top: 5px; }
        
        .filter-section {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 25px;
            margin-bottom: 30px;
        }
        .filter-title { color: #667eea; font-size: 1.2em; margin-bottom: 15px; display: flex; align-items: center; gap: 10px; }
        .filter-controls { display: flex; gap: 15px; flex-wrap: wrap; align-items: center; }
        .sort-btn {
            padding: 10px 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 25px;
            cursor: pointer;
            font-weight: 500;
            color: #e0e0e0;
            background: rgba(255, 255, 255, 0.05);
            transition: all 0.3s ease;
        }
        .sort-btn:hover, .sort-btn.active {
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-color: transparent;
        }
        .dimension-select {
            padding: 10px 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 25px;
            background: rgba(255, 255, 255, 0.05);
            color: #e0e0e0;
            cursor: pointer;
            font-size: 0.95em;
        }
        .dimension-select option { background: #1a1a2e; color: #e0e0e0; }
        
        .papers-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(450px, 1fr)); gap: 25px; margin-bottom: 30px; }
        .paper-card {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 25px;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        .paper-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        }
        .paper-card:hover {
            transform: translateY(-8px);
            border-color: rgba(102, 126, 234, 0.5);
            box-shadow: 0 20px 40px rgba(102, 126, 234, 0.2);
        }
        .paper-year-badge {
            position: absolute;
            top: 20px;
            right: 20px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
        }
        .paper-title { color: #fff; font-size: 1.15em; line-height: 1.5; margin-bottom: 12px; padding-right: 70px; }
        .paper-meta { color: #888; font-size: 0.9em; margin-bottom: 15px; }
        .paper-meta i { margin-right: 5px; color: #667eea; }
        
        .badges { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 15px; }
        .badge { padding: 5px 12px; border-radius: 15px; font-size: 0.75em; font-weight: 500; }
        .badge-q1 { background: linear-gradient(135deg, #00b894, #00cec9); color: #000; }
        .badge-q2 { background: linear-gradient(135deg, #fdcb6e, #f39c12); color: #000; }
        .badge-ei { background: linear-gradient(135deg, #e17055, #d63031); color: #fff; }
        .badge-ssci { background: linear-gradient(135deg, #6c5ce7, #a29bfe); color: #fff; }
        .badge-if { background: linear-gradient(135deg, #00b894, #55efc4); color: #000; }
        .badge-publisher { background: rgba(255, 255, 255, 0.1); color: #a0a0a0; }
        
        .paper-abstract { background: rgba(0, 0, 0, 0.2); border-radius: 12px; padding: 15px; margin-bottom: 15px; font-size: 0.9em; line-height: 1.7; color: #b0b0b0; }
        
        .dimensions-preview { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 15px; }
        .dimension-tag { background: rgba(102, 126, 234, 0.2); border: 1px solid rgba(102, 126, 234, 0.3); padding: 4px 10px; border-radius: 12px; font-size: 0.75em; color: #667eea; }
        
        .action-btns { display: flex; gap: 10px; flex-wrap: wrap; }
        .btn { flex: 1; padding: 10px 15px; border-radius: 25px; text-decoration: none; font-weight: 500; text-align: center; border: none; transition: all 0.3s ease; min-width: 100px; font-size: 0.9em; cursor: pointer; }
        .btn-download { background: linear-gradient(135deg, #e74c3c, #c0392b); color: white; }
        .btn-access { background: linear-gradient(135deg, #00b894, #00cec9); color: #000; }
        .btn-detail { background: linear-gradient(135deg, #667eea, #764ba2); color: white; }
        .btn:hover { transform: scale(1.05); filter: brightness(1.1); }
        
        .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.8); z-index: 1000; justify-content: center; align-items: center; padding: 20px; backdrop-filter: blur(5px); }
        .modal.active { display: flex; }
        .modal-content {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 24px;
            max-width: 900px;
            width: 100%;
            max-height: 90vh;
            overflow-y: auto;
            padding: 35px;
        }
        .modal-close { float: right; font-size: 1.8em; cursor: pointer; color: #666; transition: color 0.3s; }
        .modal-close:hover { color: #fff; }
        
        .modal-title { color: #fff; font-size: 1.4em; margin-bottom: 20px; line-height: 1.4; }
        .modal-meta { color: #888; margin-bottom: 20px; line-height: 1.8; }
        .modal-meta i { color: #667eea; margin-right: 8px; }
        
        .dimensions-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 12px; margin: 20px 0; }
        .dimension-card { background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%); border: 1px solid rgba(102, 126, 234, 0.2); border-radius: 12px; padding: 15px; }
        .dimension-key { color: #667eea; font-weight: 600; font-size: 0.9em; margin-bottom: 5px; }
        .dimension-value { color: #b0b0b0; font-size: 0.85em; }
        
        .bibtex-section { background: #1e1e1e; border-radius: 16px; padding: 20px; margin-top: 20px; }
        .bibtex-section h4 { color: #61dafb; margin-bottom: 15px; display: flex; align-items: center; gap: 10px; }
        .bibtex-code { background: #121212; border-radius: 10px; padding: 15px; color: #abb2bf; font-family: 'Fira Code', 'Consolas', monospace; font-size: 0.8em; overflow-x: auto; white-space: pre-wrap; word-break: break-all; line-height: 1.6; }
        .copy-btn { background: #61dafb; color: #1e1e1e; border: none; padding: 10px 20px; border-radius: 10px; cursor: pointer; font-weight: 600; margin-top: 15px; transition: all 0.3s; }
        .copy-btn:hover { background: #4fa8d1; }
        
        .summary-card { background: linear-gradient(135deg, rgba(255, 202, 58, 0.1) 0%, rgba(255, 112, 67, 0.1) 100%); border: 1px solid rgba(255, 202, 58, 0.2); border-radius: 20px; padding: 30px; margin-bottom: 30px; }
        .summary-card h2 { color: #ffca28; margin-bottom: 20px; display: flex; align-items: center; gap: 10px; }
        .summary-content { background: rgba(0, 0, 0, 0.2); border-radius: 15px; padding: 25px; line-height: 1.9; color: #d0d0d0; white-space: pre-wrap; }
        
        
        /* Sidebar Styles */
        .main-layout { display: flex; gap: 30px; align-items: flex-start; }
        .main-content { flex: 1; min-width: 0; }
        .sidebar {
            width: 320px;
            position: sticky;
            top: 20px;
            flex-shrink: 0;
        }
        .sidebar-section {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .sidebar-section h3 {
            color: #667eea;
            font-size: 1.1em;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .top-dimensions { display: flex; flex-direction: column; gap: 10px; }
        .dim-item { margin-bottom: 8px; }
        .dim-header { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; }
        .dim-rank { 
            background: linear-gradient(135deg, #667eea, #764ba2); 
            color: white; 
            padding: 2px 6px; 
            border-radius: 8px; 
            font-size: 0.7em; 
            font-weight: bold;
            min-width: 28px;
            text-align: center;
        }
        .dim-name { flex: 1; font-size: 0.85em; color: #e0e0e0; }
        .dim-count { font-size: 0.75em; color: #888; }
        .dim-bar-bg { background: rgba(255,255,255,0.1); height: 6px; border-radius: 3px; overflow: hidden; }
        .dim-bar { height: 100%; border-radius: 3px; transition: width 0.3s; }
        .stats-summary .stat-row {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        .stats-summary .stat-row:last-child { border-bottom: none; }
        .stats-summary span { color: #888; font-size: 0.9em; }
        .stats-summary strong { color: #667eea; font-size: 1.1em; }
        
        @media (max-width: 1200px) {
            .main-layout { flex-direction: column; }
            .sidebar { width: 100%; position: static; }
            .sidebar-section { display: inline-block; width: calc(50% - 10px); vertical-align: top; }
            .stats-summary { width: calc(50% - 10px); display: inline-block; }
        }
        @media (max-width: 768px) {
            .sidebar-section, .stats-summary { width: 100%; }
        }


.footer { text-align: center; padding: 40px; color: #666; }
        .footer .heart { color: #ff6b6b; animation: heartbeat 1s infinite; display: inline-block; }
        @keyframes heartbeat { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.15); } }
        
        .no-results { text-align: center; padding: 60px 20px; color: #666; }
        .no-results i { font-size: 4em; margin-bottom: 20px; color: #444; }
        
        @media (max-width: 768px) {
            .papers-grid { grid-template-columns: 1fr; }
            .header h1 { font-size: 2em; }
            .stats-bar { gap: 10px; }
            .stat-card { padding: 15px 20px; }
        }
    </style>
</head>
<body>
    <div class="container">        <div class="main-layout">
            <div class="main-content">
                <section class="summary-card">
                    <h2>📚 小女仆的学习总结 💕</h2>
                    <div class="summary-content">SUMMARY_CONTENT</div>
                </section>
                
                <section class="filter-section">
                    <h3 class="filter-title"><i class="fas fa-filter"></i> 文献筛选与排序</h3>
                    <div class="filter-controls">
                        <button class="sort-btn active" data-sort="default">📅 默认排序</button>
                        <button class="sort-btn" data-sort="if_desc">📈 影响因子↓</button>
                        <button class="sort-btn" data-sort="if_asc">📉 影响因子↑</button>
                        <button class="sort-btn" data-sort="year_desc">🆕 最新发布</button>
                        <button class="sort-btn" data-sort="year_asc">📜 最早发布</button>
                        <select class="dimension-select" id="dimensionFilter">
                            <option value信任维度筛选="">🎯 按</option>
                            DIM_OPTIONS
                        </select>
                    </div>
                </section>
                
                <h2 style="color: #fff; margin-bottom: 25px; text-align: center;"><i class="fas fa-book-open" style="color: #667eea;"></i> 学术文献</h2>
                
                <div class="papers-grid" id="papersGrid">PAPERS_HTML</div>
                
                <div class="no-results" id="noResults" style="display: none;">
                    <i class="fas fa-search"></i>
                    <h3>没有找到匹配的文献</h3>
                    <p>请尝试调整筛选条件</p>
                </div>
            </div>
            
            <div class="sidebar" id="sidebarSection">
                <!-- Sidebar populated by JavaScript -->
            </div>
        </div>
        
        <footer class="footer">
            <p>Made with <span class="heart">♥</span> for 落先生 🐱</p>
            <p style="margin-top: 10px; opacity: 0.7;">信任是任何分布式系统的核心挑战 💡</p>
            <p style="margin-top: 5px; opacity: 0.5; font-size: 0.85em;">更新日期：CURRENT_DATE</p>
        </footer>
    </div>
<div class="modal" id="paperModal">
        <div class="modal-content"><span class="modal-close" onclick="closeModal()">&times;</span><div id="modalBody"></div></div>
    </div>
    
    <script>
        let allPapers = PAPERS_JSON;
        let currentSort = 'default';
        let currentDimension = '';
        
        function showModal(paperId) {
            const paper = allPapers.find(p => p.id === paperId);
            if (!paper) return;
            
            let journalInfoHtml = '';
            if (paper.journal_info) {
                const journal = paper.journal_info;
                journalInfoHtml = '<div class="badges" style="margin: 15px 0;">' +
                    '<span class="badge badge-' + (journal.ranking || 'na').toLowerCase().replace(/\\s+/g, '-') + '">' + (journal.ranking || 'N/A') + '</span>' +
                    '<span class="badge badge-publisher">' + (journal.publisher || 'N/A') + '</span>' +
                    (journal.impact_factor_label ? '<span class="badge badge-if">' + journal.impact_factor_label + '</span>' : '') +
                    '</div>' +
                    (journal.access_url ? '<p><i class="fas fa-link"></i> <a href="' + journal.access_url + '" target="_blank" style="color: #667eea;">访问原文</a></p>' : '') +
                    (journal.doi ? '<p><i class="fas fa-fingerprint"></i> DOI: ' + journal.doi + '</p>' : '') +
                    (journal.notes ? '<p style="color: #888; font-size: 0.9em;"><i class="fas fa-info-circle"></i> ' + journal.notes + '</p>' : '');
            }
            
            let dimensionsHtml = '';
            if (paper.trust_dimensions) {
                let dimsHtml = '';
                for (const [key, value] of Object.entries(paper.trust_dimensions)) {
                    dimsHtml += '<div class="dimension-card"><div class="dimension-key">' + key + '</div><div class="dimension-value">' + value + '</div></div>';
                }
                dimensionsHtml = '<h4 style="color: #667eea; margin: 20px 0 15px;"><i class="fas fa-cube"></i> 信任维度分析</h4><div class="dimensions-grid">' + dimsHtml + '</div>';
            }
            
            let coverImageHtml = '';
            if (paper.cover_image) {
                coverImageHtml = '<img src="' + paper.cover_image + '" alt="封面" style="width:100%;max-height:200px;object-fit:cover;border-radius:16px;margin-bottom:20px;">';
            }
            
            document.getElementById('modalBody').innerHTML = 
                coverImageHtml +
                '<h2 class="modal-title">' + paper.title + '</h2>' +
                '<div class="modal-meta">' +
                '<p><i class="fas fa-user"></i> <strong>作者：</strong>' + paper.authors.join(', ') + '</p>' +
                '<p><i class="fas fa-calendar"></i> <strong>年份：</strong>' + paper.year + '</p>' +
                '<p><i class="fas fa-university"></i> <strong>机构：</strong>' + paper.institution + '</p>' +
                '<p><i class="fas fa-book"></i> <strong>期刊/会议：</strong>' + paper.venue + '</p>' +
                '</div>' +
                journalInfoHtml +
                '<h4 style="color: #ffca28; margin: 20px 0 15px;"><i class="fas fa-align-left"></i> 摘要</h4>' +
                '<div class="paper-abstract">' + paper.abstract + '</div>' +
                dimensionsHtml +
                '<div class="bibtex-section"><h4><i class="fas fa-quote-right"></i> IEEE BibTeX 引用格式</h4><div class="bibtex-code" id="bibtexContent">' + paper.bibtex + '</div><button class="copy-btn" onclick="copyBibtex()"><i class="fas fa-copy"></i> 复制 BibTeX</button></div>';
            document.getElementById('paperModal').classList.add('active');
        }
        
        function closeModal() { document.getElementById('paperModal').classList.remove('active'); }
        
        function copyBibtex() {
            const content = document.getElementById('bibtexContent').innerText;
            navigator.clipboard.writeText(content).then(() => alert('BibTeX 已复制到剪贴板！'));
        }
        
        function sortAndFilterPapers() {
            let filtered = allPapers;
            if (currentDimension) {
                filtered = allPapers.filter(p => p.trust_dimensions && Object.keys(p.trust_dimensions).some(k => k.toLowerCase().includes(currentDimension.toLowerCase())));
            }
            
            filtered.sort((a, b) => {
                if (currentSort === 'default') return 0;
                if (currentSort === 'if_desc') {
                    const aIf = (a.journal_info && a.journal_info.impact_factor) || 0;
                    const bIf = (b.journal_info && b.journal_info.impact_factor) || 0;
                    return bIf - aIf;
                }
                if (currentSort === 'if_asc') {
                    const aIf = (a.journal_info && a.journal_info.impact_factor) || 0;
                    const bIf = (b.journal_info && b.journal_info.impact_factor) || 0;
                    return aIf - bIf;
                }
                if (currentSort === 'year_desc') return b.year - a.year;
                if (currentSort === 'year_asc') return a.year - b.year;
                return 0;
            });
            
            renderPapers(filtered);
        }
        
        function renderPapers(papers) {
            const grid = document.getElementById('papersGrid');
            const noResults = document.getElementById('noResults');
            
            if (papers.length === 0) {
                grid.innerHTML = '';
                noResults.style.display = 'block';
                return;
            }
            noResults.style.display = 'none';
            
            grid.innerHTML = papers.map(paper => {
                const journal = paper.journal_info || {};
                const ranking = journal.ranking || '';
                const impact = journal.impact_factor || 0;
                const rankingClass = ranking.toLowerCase().replace(/\\s+/g, '-');
                
                let btnDownload = '';
                if (paper.file) {
                    btnDownload = '<a href="/download/' + paper.file + '" class="btn btn-download"><i class="fas fa-download"></i> PDF</a>';
                }
                
                let btnAccess = '';
                if (journal.access_url) {
                    btnAccess = '<a href="' + journal.access_url + '" target="_blank" class="btn btn-access"><i class="fas fa-external-link-alt"></i> 访问</a>';
                }
                
                let dimensionsPreview = '';
                if (paper.trust_dimensions) {
                    const dims = Object.keys(paper.trust_dimensions);
                    const dimTags = dims.slice(0, 4).map(k => '<span class="dimension-tag">' + k + '</span>').join('');
                    const more = dims.length > 4 ? '<span class="dimension-tag">+更多</span>' : '';
                    dimensionsPreview = '<div class="dimensions-preview">' + dimTags + more + '</div>';
                }
                
                let badges = '<span class="badge badge-' + rankingClass + '">' + ranking + '</span>';
                if (journal.impact_factor_label) {
                    badges += '<span class="badge badge-if">' + journal.impact_factor_label + '</span>';
                }
                badges += '<span class="badge badge-publisher">' + (journal.publisher || paper.institution) + '</span>';
                
                return '<article class="paper-card" data-ranking="' + ranking + '" data-if="' + impact + '" data-year="' + paper.year + '">' +
                    '<span class="paper-year-badge">' + paper.year + '</span>' +
                    '<h3 class="paper-title">' + paper.title + '</h3>' +
                    '<div class="paper-meta"><i class="fas fa-user"></i> ' + paper.authors.join(', ') + '<br><i class="fas fa-university"></i> ' + paper.institution + '</div>' +
                    '<div class="badges">' + badges + '</div>' +
                    '<div class="paper-abstract">' + paper.abstract.substring(0, 150) + '...</div>' +
                    dimensionsPreview +
                    '<div class="action-btns">' + btnDownload + btnAccess + '<button class="btn btn-detail" onclick="showModal(\\'' + paper.id + '\\')"><i class="fas fa-info-circle"></i> 详情</button></div></article>';
            }).join('');
        }
        
        document.querySelectorAll('.sort-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                document.querySelectorAll('.sort-btn').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                currentSort = this.dataset.sort;
                sortAndFilterPapers();
            });
        });
        
        document.getElementById('dimensionFilter').addEventListener('change', function() {
            currentDimension = this.value;
            sortAndFilterPapers();
        });
        
        // 生成侧边栏统计
        generateSidebar();
        
        document.getElementById('paperModal').addEventListener('click', function(e) { if (e.target === this) closeModal(); });
    </script>
    <script>
    // 维度统计数据
    const dimensionStats = DIM_STATS_JSON;
    
    function generateSidebar() {
        const sidebar = document.getElementById('sidebarSection');
        if (!sidebar) return;
        
        const topDims = dimensionStats.top_dimensions.slice(0, 10);
        
        let html = `
            <div class="sidebar-section">
                <h3><i class="fas fa-chart-pie"></i> 维度统计</h3>
                <canvas id="dimensionChart" width="280" height="200"></canvas>
            </div>
            
            <div class="sidebar-section">
                <h3><i class="fas fa-trophy"></i> Top 10 维度</h3>
                <div class="top-dimensions">
        `;
        
        topDims.forEach((item, index) => {
            const barWidth = (item.count / topDims[0].count) * 100;
            html += `
                <div class="dim-item">
                    <div class="dim-header">
                        <span class="dim-rank">#${index + 1}</span>
                        <span class="dim-name">${item.dimension}</span>
                        <span class="dim-count">${item.count} (${item.percentage}%)</span>
                    </div>
                    <div class="dim-bar-bg">
                        <div class="dim-bar" style="width:${barWidth}%;"></div>
                    </div>
                </div>
            `;
        });
        
        html += `
                </div>
            </div>
            
            <div class="sidebar-section stats-summary">
                <h3><i class="fas fa-chart-bar"></i> 统计概览</h3>
                <div class="stat-row">
                    <span>📚 文献总数</span>
                    <strong>${dimensionStats.total_papers}</strong>
                </div>
                <div class="stat-row">
                    <span>🎯 唯一维度</span>
                    <strong>${dimensionStats.unique_dimensions}</strong>
                </div>
                <div class="stat-row">
                    <span>📊 维度总数</span>
                    <strong>${dimensionStats.total_dimensions}</strong>
                </div>
            </div>
        `;
        
        sidebar.innerHTML = html;
        
        // 初始化图表
        setTimeout(() => initChart(), 100);
    }
    
    function initChart() {
        const canvas = document.getElementById('dimensionChart');
        if (!canvas) return;
        
        const ctx = canvas.getContext('2d');
        const data = dimensionStats.top_dimensions.slice(0, 8);
        
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.map(d => d.dimension),
                datasets: [{
                    data: data.map(d => d.count),
                    backgroundColor: [
                        '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7',
                        '#DDA0DD', '#98D8C8', '#F7DC6F'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: '#a0a0a0',
                            font: { size: 9 },
                            padding: 5
                        }
                    }
                }
            }
        });
    }
    </script>
<!-- Sidebar and Charts -->
    <div class="sidebar">
        <div class="sidebar-section">
            <h3><i class="fas fa-chart-pie"></i> 维度统计</h3>
            <canvas id="dimensionChart" width="280" height="280"></canvas>
        </div>
        
        <div class="sidebar-section">
            <h3><i class="fas fa-trophy"></i> Top 10 维度</h3>
            <div class="top-dimensions">
                
        <div class="dim-item">
            <div class="dim-header">
                <span class="dim-rank">#1</span>
                <span class="dim-name">reputation</span>
                <span class="dim-count">3 (11.1%)</span>
            </div>
            <div class="dim-bar-bg">
                <div class="dim-bar" style="width:100%;background:linear-gradient(90deg,#667eea,#764ba2);"></div>
            </div>
        </div>
    
        <div class="dim-item">
            <div class="dim-header">
                <span class="dim-rank">#2</span>
                <span class="dim-name">security</span>
                <span class="dim-count">3 (11.1%)</span>
            </div>
            <div class="dim-bar-bg">
                <div class="dim-bar" style="width:100%;background:linear-gradient(90deg,#667eea,#764ba2);"></div>
            </div>
        </div>
    
        <div class="dim-item">
            <div class="dim-header">
                <span class="dim-rank">#3</span>
                <span class="dim-name">trust</span>
                <span class="dim-count">2 (7.4%)</span>
            </div>
            <div class="dim-bar-bg">
                <div class="dim-bar" style="width:66%;background:linear-gradient(90deg,#667eea,#764ba2);"></div>
            </div>
        </div>
    
        <div class="dim-item">
            <div class="dim-header">
                <span class="dim-rank">#4</span>
                <span class="dim-name">self_assessment</span>
                <span class="dim-count">2 (7.4%)</span>
            </div>
            <div class="dim-bar-bg">
                <div class="dim-bar" style="width:66%;background:linear-gradient(90deg,#667eea,#764ba2);"></div>
            </div>
        </div>
    
        <div class="dim-item">
            <div class="dim-header">
                <span class="dim-rank">#5</span>
                <span class="dim-name">cloud_audit</span>
                <span class="dim-count">2 (7.4%)</span>
            </div>
            <div class="dim-bar-bg">
                <div class="dim-bar" style="width:66%;background:linear-gradient(90deg,#667eea,#764ba2);"></div>
            </div>
        </div>
    
        <div class="dim-item">
            <div class="dim-header">
                <span class="dim-rank">#6</span>
                <span class="dim-name">usability</span>
                <span class="dim-count">2 (7.4%)</span>
            </div>
            <div class="dim-bar-bg">
                <div class="dim-bar" style="width:66%;background:linear-gradient(90deg,#667eea,#764ba2);"></div>
            </div>
        </div>
    
        <div class="dim-item">
            <div class="dim-header">
                <span class="dim-rank">#7</span>
                <span class="dim-name">continuous_verification</span>
                <span class="dim-count">2 (7.4%)</span>
            </div>
            <div class="dim-bar-bg">
                <div class="dim-bar" style="width:66%;background:linear-gradient(90deg,#667eea,#764ba2);"></div>
            </div>
        </div>
    
        <div class="dim-item">
            <div class="dim-header">
                <span class="dim-rank">#8</span>
                <span class="dim-name">least_privilege</span>
                <span class="dim-count">2 (7.4%)</span>
            </div>
            <div class="dim-bar-bg">
                <div class="dim-bar" style="width:66%;background:linear-gradient(90deg,#667eea,#764ba2);"></div>
            </div>
        </div>
    
        <div class="dim-item">
            <div class="dim-header">
                <span class="dim-rank">#9</span>
                <span class="dim-name">micro_segmentation</span>
                <span class="dim-count">2 (7.4%)</span>
            </div>
            <div class="dim-bar-bg">
                <div class="dim-bar" style="width:66%;background:linear-gradient(90deg,#667eea,#764ba2);"></div>
            </div>
        </div>
    
        <div class="dim-item">
            <div class="dim-header">
                <span class="dim-rank">#10</span>
                <span class="dim-name">transparency</span>
                <span class="dim-count">2 (7.4%)</span>
            </div>
            <div class="dim-bar-bg">
                <div class="dim-bar" style="width:66%;background:linear-gradient(90deg,#667eea,#764ba2);"></div>
            </div>
        </div>
    
            </div>
        </div>
        
        <div class="sidebar-section stats-summary">
            <h3><i class="fas fa-chart-bar"></i> 统计概览</h3>
            <div class="stat-row">
                <span>📚 文献总数</span>
                <strong>27</strong>
            </div>
            <div class="stat-row">
                <span>🎯 唯一维度</span>
                <strong>93</strong>
            </div>
            <div class="stat-row">
                <span>📊 维度总数</span>
                <strong>106</strong>
            </div>
        </div>
    </div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('dimensionChart').getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['reputation', 'security', 'trust', 'self_assessment', 'cloud_audit', 'usability', 'continuous_verification', 'least_privilege', 'micro_segmentation', 'transparency', 'compliance', 'human_agency_oversight', 'fairness_nondiscrimination', 'transparency_explainability', 'robustness_accuracy'],
            datasets: [{
                data: [3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1],
                backgroundColor: ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9', '#F8B500', '#00CED1', '#FF69B4', '#7DCEA0', '#E74C3C'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#a0a0a0',
                        font: { size: 10 },
                        padding: 8
                    }
                }
            }
        }
    });
});
</script>
</body>
</html>
"""

def generate_papers_html(papers):
    return "PLACEHOLDER"

@app.route('/')
def index():
    html = HTML_TEMPLATE
    html = html.replace('PAPERS_COUNT', str(len(PAPERS_DATA)))
    html = html.replace('STATS_Q1', str(STATS.get('sci_q1', 0)))
    html = html.replace('STATS_Q2', str(STATS.get('sci_q2', 0)))
    html = html.replace('STATS_EI', str(STATS.get('ei', 0)))
    html = html.replace('DIM_COUNT', str(len(ALL_DIMENSIONS)))
    html = html.replace('CURRENT_DATE', datetime.now().strftime("%Y年%m月%d日"))
    html = html.replace('SUMMARY_CONTENT', SUMMARY)
    html = html.replace('PAPERS_JSON', json.dumps(PAPERS_DATA, ensure_ascii=False))
    
    # 维度选项
    dim_options = '<option value="">🎯 按信任维度筛选</option>'
    for dim in sorted(ALL_DIMENSIONS):
        dim_options += '<option value="' + dim + '">' + dim + '</option>'
    html = html.replace('DIM_OPTIONS', dim_options)
    
    # 加载维度统计数据
    with open(os.path.join(LITERATURE_DIR, 'dimension_stats.json'), 'r', encoding='utf-8') as f:
        dim_stats = json.load(f)
    html = html.replace('DIM_STATS_JSON', json.dumps(dim_stats))
    
    # 生成论文卡片
    papers_html = []
    for paper in PAPERS_DATA:
        journal_info = paper.get('journal_info', {})
        ranking = journal_info.get('ranking', '') if journal_info else ''
        impact = journal_info.get('impact_factor', 0) if journal_info else 0
        access_url = journal_info.get('access_url', '') if journal_info else ''
        publisher = journal_info.get('publisher', '') if journal_info else paper.get('institution', '')
        
        btn_download = ''
        if paper.get('file'):
            btn_download = '<a href="/download/' + paper['file'] + '" class="btn btn-download"><i class="fas fa-download"></i> PDF</a>'
        
        btn_access = ''
        if access_url:
            btn_access = '<a href="' + access_url + '" target="_blank" class="btn btn-access"><i class="fas fa-external-link-alt"></i> 访问</a>'
        
        dimensions_preview = ''
        if paper.get('trust_dimensions'):
            dims = list(paper['trust_dimensions'].keys())
            dim_tags = ''.join(['<span class="dimension-tag">' + k + '</span>' for k in dims[:4]])
            more = '<span class="dimension-tag">+更多</span>' if len(dims) > 4 else ''
            dimensions_preview = '<div class="dimensions-preview">' + dim_tags + more + '</div>'
        
        ranking_class = ranking.lower().replace(' ', '-') if ranking else 'na'
        badges = '<span class="badge badge-' + ranking_class + '">' + ranking + '</span>'
        if journal_info.get('impact_factor_label'):
            badges += '<span class="badge badge-if">' + journal_info['impact_factor_label'] + '</span>'
        badges += '<span class="badge badge-publisher">' + publisher + '</span>'
        
        # 封面图片
        cover_image = paper.get('cover_image', '')
        cover_html = ''
        if cover_image:
            cover_html = '<img src="' + cover_image + '" alt="封面" style="width:100%;height:120px;object-fit:cover;border-radius:12px;margin-bottom:15px;">'
        
        card = '''<article class="paper-card" data-ranking="RANKING" data-if="IMPACT" data-year="YEAR">
            COVER_IMAGE
            <span class="paper-year-badge">YEAR</span>
            <h3 class="paper-title">TITLE</h3>
            <div class="paper-meta"><i class="fas fa-user"></i> AUTHORS<br><i class="fas fa-university"></i> INSTITUTION</div>
            <div class="badges">BADGES</div>
            <div class="paper-abstract">ABSTRACT...</div>
            DIMENSIONS_PREVIEW
            <div class="action-btns">BTN_DOWNLOAD BTN_ACCESS <button class="btn btn-detail" onclick="showModal('ID')"><i class="fas fa-info-circle"></i> 详情</button></div>
        </article>'''
        
        card = card.replace('COVER_IMAGE', cover_html)\
                   .replace('TITLE', paper['title'])\
                   .replace('AUTHORS', ', '.join(paper['authors']))\
                   .replace('INSTITUTION', paper['institution'])\
                   .replace('YEAR', str(paper['year']))\
                   .replace('RANKING', ranking)\
                   .replace('IMPACT', str(impact))\
                   .replace('BADGES', badges)\
                   .replace('ABSTRACT', paper['abstract'][:150])\
                   .replace('DIMENSIONS_PREVIEW', dimensions_preview)\
                   .replace('BTN_DOWNLOAD', btn_download)\
                   .replace('BTN_ACCESS', btn_access)\
                   .replace('ID', paper['id'])
        papers_html.append(card)
    
    html = html.replace('PAPERS_HTML', ''.join(papers_html))
    return html

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(LITERATURE_DIR, filename, as_attachment=True)

@app.route('/api/papers')
def api_papers():
    return jsonify({
        "papers": PAPERS_DATA, 
        "stats": STATS, 
        "summary": SUMMARY.strip(),
        "dimensions": list(ALL_DIMENSIONS)
    })

if __name__ == '__main__':
    print("🐱 落先生的文献小窝 V2.0 启动啦！")
    print("📍 访问地址：http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
