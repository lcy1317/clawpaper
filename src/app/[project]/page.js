"use client"

import { useState, useEffect } from 'react'
import Link from 'next/link'

const PROJECT_INFO = {
  'trust-literature': {
    name: '信任度文献调研',
    color: 'from-blue-500 to-cyan-500',
    description: '深度调研系统信任度评估文献，聚焦AI系统可信度、云服务可信度、软件供应链安全、零信任架构。本项目收录了1000+篇顶会顶刊论文，涵盖CVPR、NeurIPS、ICML、ICLR、AAAI等顶级会议，以及Nature、Science、IEEE TPAMI等权威期刊。所有文献均经过人工筛选和分类，包含完整的论文元数据、影响因子、期刊分区、信任维度标注和核心贡献点分析。',
    stats: { total: 1000, q1: 450, q2: 280, q3: 150, ei: 120 }
  },
  'quant-papers': {
    name: '量化论文分析',
    color: 'from-purple-500 to-pink-500',
    description: '量化交易相关学术论文与策略研究。涵盖因子模型、机器学习预测、组合优化、风险管理、高频交易等核心领域。收录JPM、QuantLib、AQR等顶级期刊和会议论文，提供策略回测框架、因子分析工具和实盘指导。',
    stats: { total: 500, q1: 200, q2: 150, q3: 100, ei: 50 }
  },
  'ai-safety': {
    name: 'AI安全研究',
    color: 'from-red-500 to-orange-500',
    description: '人工智能安全、对齐与伦理研究。聚焦大模型安全、RLHF对齐、价值观约束、对抗鲁棒性、隐私保护、公平性等前沿课题。收录ICML、NeurIPS、ICLR、AAAI等安全专题论文，提供安全评估框架和最佳实践指南。',
    stats: { total: 300, q1: 120, q2: 80, q3: 60, ei: 40 }
  }
}

const RANKING_BADGES = {
  'sci q1': { label: 'SCI Q1', color: 'bg-green-100 text-green-800 border-green-200' },
  'sci q2': { label: 'SCI Q2', color: 'bg-yellow-100 text-yellow-800 border-yellow-200' },
  'sci q3': { label: 'SCI Q3', color: 'bg-orange-100 text-orange-800 border-orange-200' },
  'ccf-a': { label: 'CCF-A', color: 'bg-red-100 text-red-800 border-red-200' },
  'ccf-b': { label: 'CCF-B', color: 'bg-orange-100 text-orange-800 border-orange-200' },
  'ccf-c': { label: 'CCF-C', color: 'bg-blue-100 text-blue-800 border-blue-200' },
  'ei': { label: 'EI', color: 'bg-purple-100 text-purple-800 border-purple-200' },
}

function getRankingInfo(ranking) {
  if (!ranking) return { label: '其他', color: 'bg-gray-100 text-gray-800 border-gray-200' }
  const key = ranking.toLowerCase().replace(/\s+/g, ' ')
  const badge = RANKING_BADGES[key]
  return badge || { label: ranking, color: 'bg-gray-100 text-gray-800 border-gray-200' }
}

export default function ProjectPage({ params }) {
  const [papers, setPapers] = useState([])
  const [stats, setStats] = useState({ total: 0, q1: 0, q2: 0, q3: 0, ei: 0 })
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')
  const [sortType, setSortType] = useState('default')
  const [selectedPaper, setSelectedPaper] = useState(null)
  
  useEffect(() => {
    async function loadPapers() {
      try {
        const res = await fetch('/api/papers')
        const data = await res.json()
        setPapers(data.papers || [])
        setStats(data.stats || { total: 0, q1: 0, q2: 0, q3: 0, ei: 0 })
      } catch (error) {
        console.error('加载文献失败:', error)
      } finally {
        setLoading(false)
      }
    }
    loadPapers()
  }, [])
  
  const projectInfo = PROJECT_INFO[params.project] || { 
    name: '未知项目', 
    color: 'from-gray-400 to-gray-500', 
    description: '该项目正在整理中...',
    stats: { total: 0, q1: 0, q2: 0, q3: 0, ei: 0 }
  }
  
  const filteredPapers = papers.filter(p => {
    if (!searchQuery) return true
    const q = searchQuery.toLowerCase()
    return p.title?.toLowerCase().includes(q) ||
           p.authors?.some(a => a.toLowerCase().includes(q)) ||
           p.abstract?.toLowerCase().includes(q)
  }).sort((a, b) => {
    if (sortType === 'if_desc') return (b.journal_info?.impact_factor || 0) - (a.journal_info?.impact_factor || 0)
    if (sortType === 'if_asc') return (a.journal_info?.impact_factor || 0) - (b.journal_info?.impact_factor || 0)
    if (sortType === 'year_desc') return (b.year || 0) - (a.year || 0)
    if (sortType === 'year_asc') return (a.year || 0) - (b.year || 0)
    return 0
  })
  
  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-600">加载文献中...</p>
        </div>
      </div>
    )
  }
  
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="p-4 md:p-6">
        <div className="max-w-7xl mx-auto">
          <header className="mb-8">
            <Link href="/" className="inline-flex items-center gap-2 text-gray-500 hover:text-gray-800 mb-6 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
                <path d="m12 19-7-7 7-7"></path>
                <path d="M19 12H5"></path>
              </svg>
              返回首页
            </Link>

            <div className={`bg-gradient-to-r ${projectInfo.color} rounded-2xl p-6 md:p-8 mb-6 text-white shadow-lg`}>
              <h1 className="text-2xl md:text-3xl font-bold mb-3">{projectInfo.name}</h1>
              <p className="text-white/90 mb-6 leading-relaxed">{projectInfo.description}</p>
              
              <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                <div className="bg-white/20 backdrop-blur-sm rounded-xl p-3 text-center">
                  <div className="text-2xl font-bold">{stats.total}</div>
                  <div className="text-xs text-white/80">📚 总文献</div>
                </div>
                <div className="bg-white/20 backdrop-blur-sm rounded-xl p-3 text-center">
                  <div className="text-2xl font-bold">{stats.q1}</div>
                  <div className="text-xs text-white/80">🟢 Q1/CCF-A</div>
                </div>
                <div className="bg-white/20 backdrop-blur-sm rounded-xl p-3 text-center">
                  <div className="text-2xl font-bold">{stats.q2}</div>
                  <div className="text-xs text-white/80">🟠 Q2/CCF-B</div>
                </div>
                <div className="bg-white/20 backdrop-blur-sm rounded-xl p-3 text-center">
                  <div className="text-2xl font-bold">{stats.q3}</div>
                  <div className="text-xs text-white/80">🟡 Q3/CCF-C</div>
                </div>
                <div className="bg-white/20 backdrop-blur-sm rounded-xl p-3 text-center">
                  <div className="text-2xl font-bold">{stats.ei}</div>
                  <div className="text-xs text-white/80">⚪ EI</div>
                </div>
              </div>
            </div>

            <div className="flex flex-col md:flex-row gap-4 mb-6">
              <div className="relative flex-1">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400">
                  <circle cx="11" cy="11" r="8"></circle>
                  <path d="m21 21-4.3-4.3"></path>
                </svg>
                <input 
                  type="text" 
                  placeholder="搜索标题、作者、摘要..." 
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-12 pr-4 py-3 bg-white border border-gray-200 rounded-xl text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-sm"
                />
              </div>
              <select 
                value={sortType}
                onChange={(e) => setSortType(e.target.value)}
                className="px-4 py-3 bg-white border border-gray-200 rounded-xl text-gray-800 cursor-pointer shadow-sm"
              >
                <option value="default">📅 默认排序</option>
                <option value="if_desc">📈 影响因子↓</option>
                <option value="if_asc">📉 影响因子↑</option>
                <option value="year_desc">🆕 最新发布</option>
                <option value="year_asc">📜 最早发布</option>
              </select>
            </div>
          </header>

          <main>
            {papers.length === 0 ? (
              <div className="text-center py-16 bg-white rounded-2xl shadow-sm">
                <h3 className="text-xl font-semibold text-gray-600 mb-2">暂无文献数据</h3>
                <p className="text-gray-400">该项目的文献数据正在整理中</p>
              </div>
            ) : filteredPapers.length === 0 ? (
              <div className="text-center py-16 bg-white rounded-2xl shadow-sm">
                <h3 className="text-xl font-semibold text-gray-600 mb-2">未找到匹配文献</h3>
                <p className="text-gray-400">请尝试调整搜索条件</p>
              </div>
            ) : (
              <div className="grid gap-4 md:grid-cols-2">
                {filteredPapers.map((paper) => {
                  const journal = paper.journal_info || {}
                  const ranking = getRankingInfo(journal.ranking || '')
                  const impact = journal.impact_factor || 0
                  const publisher = journal.publisher || paper.institution || ''
                  const dimensions = Object.keys(paper.trust_dimensions || {}).slice(0, 5)
                  
                  return (
                    <article 
                      key={paper.id} 
                      onClick={() => setSelectedPaper(paper)}
                      className="group cursor-pointer bg-white rounded-2xl p-6 border border-gray-100 shadow-sm hover:shadow-lg hover:border-gray-200 transition-all duration-300"
                    >
                      <div className="flex justify-between items-start mb-3">
                        <h3 className="text-lg font-semibold text-gray-800 pr-16 leading-relaxed group-hover:text-blue-600 transition-colors">
                          {paper.title}
                        </h3>
                        <span className="bg-blue-500 text-white text-xs font-bold px-3 py-1 rounded-full flex-shrink-0">
                          {paper.year}
                        </span>
                      </div>
                      
                      <div className="flex items-center gap-2 text-sm text-gray-500 mb-3">
                        <span className="truncate">
                          {(paper.authors || []).slice(0, 3).join(', ')}{(paper.authors?.length > 3) && ` 等${paper.authors.length}人`}
                        </span>
                      </div>
                      
                      <div className="flex flex-wrap items-center gap-3 text-sm text-gray-500 mb-4">
                        <span>{paper.venue || '未知期刊'}</span>
                        {impact > 0 && <span className="text-emerald-600 font-medium">IF: {impact.toFixed(1)}</span>}
                        {paper.citations > 0 && <span className="text-amber-600">引用: {paper.citations}</span>}
                      </div>
                      
                      <div className="flex flex-wrap gap-2 mb-4">
                        <span className={`px-2 py-1 rounded-lg text-xs font-medium border ${ranking.color}`}>
                          {ranking.label}
                        </span>
                        {publisher && (
                          <span className="px-2 py-1 rounded-lg text-xs font-medium bg-gray-100 text-gray-600">
                            {publisher.substring(0, 15)}
                          </span>
                        )}
                      </div>
                      
                      <p className="text-gray-600 text-sm line-clamp-3 mb-4 leading-relaxed">
                        {paper.abstract || '暂无摘要'}
                      </p>
                      
                      {dimensions.length > 0 && (
                        <div className="flex flex-wrap gap-2 mb-4">
                          {dimensions.map(d => (
                            <span key={d} className="px-2 py-1 rounded-lg text-xs font-medium bg-blue-50 text-blue-600 border border-blue-100">
                              {d}
                            </span>
                          ))}
                        </div>
                      )}
                      
                      <div className="flex gap-2 pt-3 border-t border-gray-100">
                        {journal.access_url && (
                          <a 
                            href={journal.access_url} 
                            target="_blank" 
                            onClick={(e) => e.stopPropagation()}
                            className="flex-1 py-2 px-4 rounded-xl text-center text-sm font-medium bg-emerald-500 text-white hover:bg-emerald-600 transition-colors"
                          >
                            访问
                          </a>
                        )}
                        <button className="flex-1 py-2 px-4 rounded-xl text-center text-sm font-medium bg-blue-500 text-white hover:bg-blue-600 transition-colors">
                          详情
                        </button>
                      </div>
                    </article>
                  )
                })}
              </div>
            )}
          </main>

          <footer className="mt-16 text-center text-gray-400 text-sm py-8 border-t border-gray-200">
            <p>© 2026 ClawPaper · 学术文献管理平台</p>
          </footer>
        </div>
      </div>

      {selectedPaper && (
        <div 
          className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4"
          onClick={() => setSelectedPaper(null)}
        >
          <div 
            className="bg-white rounded-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="p-6 md:p-8 relative">
              <button 
                onClick={() => setSelectedPaper(null)}
                className="absolute top-4 right-4 text-gray-400 hover:text-gray-600 text-2xl"
              >
                &times;
              </button>
              
              <h2 className="text-2xl font-bold text-gray-800 mb-6 pr-8 leading-relaxed">
                {selectedPaper.title}
              </h2>
              
              <div className="text-gray-600 mb-6 space-y-2">
                <p><span className="font-medium text-gray-800">作者：</span>{selectedPaper.authors?.join(', ')}</p>
                <p><span className="font-medium text-gray-800">年份：</span>{selectedPaper.year}</p>
                <p><span className="font-medium text-gray-800">期刊/会议：</span>{selectedPaper.venue || 'N/A'}</p>
                <p><span className="font-medium text-gray-800">机构：</span>{selectedPaper.institution || 'N/A'}</p>
              </div>
              
              <div className="flex flex-wrap gap-2 mb-4">
                <span className={`px-3 py-1 rounded-lg text-sm font-medium border ${getRankingInfo(selectedPaper.journal_info?.ranking || '').color}`}>
                  {getRankingInfo(selectedPaper.journal_info?.ranking || '').label}
                </span>
                {(selectedPaper.journal_info?.impact_factor || 0) > 0 && (
                  <span className="px-3 py-1 rounded-lg text-sm font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">
                    IF: {selectedPaper.journal_info.impact_factor.toFixed(1)}
                  </span>
                )}
              </div>
              
              {selectedPaper.journal_info?.access_url && (
                <p className="mb-4">
                  <a 
                    href={selectedPaper.journal_info.access_url} 
                    target="_blank" 
                    className="text-blue-600 hover:text-blue-800"
                  >
                    访问原文 →
                  </a>
                </p>
              )}
              
              <h4 className="text-xl font-bold text-gray-800 mb-4">摘要</h4>
              <div className="bg-gray-50 rounded-xl p-4 mb-6 text-gray-600 leading-relaxed">
                {selectedPaper.abstract || '暂无摘要'}
              </div>
              
              {selectedPaper.bibtex && (
                <div className="bg-gray-900 rounded-xl p-4 border border-gray-700">
                  <h4 className="text-blue-400 font-bold mb-3">IEEE BibTeX 引用格式</h4>
                  <pre className="text-gray-300 text-sm overflow-x-auto whitespace-pre-wrap break-all font-mono bg-black/50 p-4 rounded-lg">
                    {selectedPaper.bibtex}
                  </pre>
                  <button 
                    onClick={() => {
                      navigator.clipboard.writeText(selectedPaper.bibtex || '')
                      alert('BibTeX 已复制到剪贴板！')
                    }}
                    className="mt-3 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
                  >
                    复制 BibTeX
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
