'use client'

import Link from 'next/link'
import MiniMaxSettings from '../components/MiniMaxSettings'
import AIChat from '../components/AIChat'
import { useState } from 'react'

const PROJECTS = [
  {
    id: 'trust-literature',
    name: '信任度文献调研',
    description: '深度调研系统信任度评估文献',
    icon: '📚',
    color: 'from-blue-500 to-cyan-500',
    count: 500
  },
  {
    id: 'quant-papers',
    name: '量化论文分析',
    description: '量化交易相关学术论文与策略研究',
    icon: '📈',
    color: 'from-purple-500 to-pink-500',
    count: 0
  },
  {
    id: 'ai-safety',
    name: 'AI安全研究',
    description: '人工智能安全、对齐与伦理研究',
    icon: '🔒',
    color: 'from-red-500 to-orange-500',
    count: 0
  }
]

export default function Home() {
  const [apiKey, setApiKey] = useState('')
  const [showChat, setShowChat] = useState(false)
  const [showSettings, setShowSettings] = useState(false)

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="p-4 md:p-6">
        <div className="max-w-7xl mx-auto">
          {/* 头部 */}
          <header className="mb-12 text-center">
            <h1 className="text-4xl md:text-5xl font-bold text-gray-800 mb-4">
              ClawPaper 🐱
            </h1>
            <p className="text-xl text-gray-600">学术文献管理平台</p>
            <p className="text-gray-400 mt-2">收录500+篇高质量信任相关学术论文</p>
          </header>

          {/* 项目卡片 */}
          <main className="grid gap-6 md:grid-cols-3">
            {PROJECTS.map((project) => (
              <Link 
                key={project.id}
                href={`/${project.id}`}
                className="group bg-white rounded-2xl p-6 shadow-sm hover:shadow-lg transition-all duration-300 border border-gray-100"
              >
                <div className={`w-16 h-16 rounded-2xl bg-gradient-to-r ${project.color} flex items-center justify-center text-3xl mb-4`}>
                  {project.icon}
                </div>
                <h2 className="text-xl font-bold text-gray-800 mb-2 group-hover:text-blue-600 transition-colors">
                  {project.name}
                </h2>
                <p className="text-gray-600 mb-4">{project.description}</p>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-400">
                    {project.count > 0 ? `${project.count} 篇文献` : '🚧 整理中'}
                  </span>
                  <span className="text-blue-500 group-hover:translate-x-1 transition-transform">→</span>
                </div>
              </Link>
            ))}
          </main>

          {/* AI助手区域 */}
          <div className="mt-12 grid gap-6 md:grid-cols-2">
            {/* AI对话按钮 */}
            <div 
              onClick={() => {
                if (!apiKey) {
                  setShowSettings(true)
                } else {
                  setShowChat(true)
                }
              }}
              className="cursor-pointer bg-gradient-to-r from-purple-500 to-pink-500 rounded-2xl p-6 text-white shadow-lg hover:shadow-xl hover:scale-[1.02] transition-all duration-300"
            >
              <div className="flex items-center gap-4">
                <span className="text-4xl">🤖</span>
                <div>
                  <h3 className="text-xl font-bold mb-1">AI学术助手</h3>
                  <p className="text-white/80 text-sm">基于MiniMax AI，解答学术问题</p>
                </div>
              </div>
            </div>

            {/* API设置按钮 */}
            <div 
              onClick={() => setShowSettings(true)}
              className="cursor-pointer bg-white rounded-2xl p-6 border border-gray-200 shadow-sm hover:shadow-md hover:border-gray-300 transition-all duration-300"
            >
              <div className="flex items-center gap-4">
                <span className="text-4xl">⚙️</span>
                <div>
                  <h3 className="text-xl font-bold text-gray-800 mb-1">API 设置</h3>
                  <p className="text-gray-500 text-sm">配置MiniMax API密钥</p>
                </div>
              </div>
            </div>
          </div>

          {/* 底部 */}
          <footer className="mt-16 text-center text-gray-400 text-sm py-8 border-t border-gray-200">
            <p>© 2026 ClawPaper · 学术文献管理平台 · 由可爱的小女仆精心打造 💕</p>
          </footer>
        </div>
      </div>

      {/* 设置弹窗 */}
      {showSettings && (
        <div 
          className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4"
          onClick={() => setShowSettings(false)}
        >
          <div 
            className="w-full max-w-lg"
            onClick={(e) => e.stopPropagation()}
          >
            <MiniMaxSettings 
              apiKey={apiKey} 
              onApiKeyChange={(key) => {
                setApiKey(key)
                setShowSettings(false)
              }} 
            />
          </div>
        </div>
      )}

      {/* AI对话弹窗 */}
      {showChat && apiKey && (
        <AIChat 
          apiKey={apiKey} 
          onClose={() => setShowChat(false)} 
        />
      )}
    </div>
  )
}
