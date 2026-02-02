'use client'

import { useState, useEffect } from 'react'

export default function MiniMaxSettings({ onApiKeyChange }) {
  const [apiKey, setApiKey] = useState('')
  const [saved, setSaved] = useState(false)
  const [showKey, setShowKey] = useState(false)

  useEffect(() => {
    const savedKey = localStorage.getItem('minimax_api_key')
    if (savedKey) {
      setApiKey(savedKey)
      onApiKeyChange(savedKey)
    }
  }, [onApiKeyChange])

  const handleSave = () => {
    if (apiKey.trim()) {
      localStorage.setItem('minimax_api_key', apiKey.trim())
      onApiKeyChange(apiKey.trim())
      setSaved(true)
      setTimeout(() => setSaved(false), 2000)
    }
  }

  const handleClear = () => {
    setApiKey('')
    localStorage.removeItem('minimax_api_key')
    onApiKeyChange('')
  }

  return (
    <div className="bg-white rounded-2xl p-6 border border-gray-200 shadow-sm">
      <div className="flex items-center gap-3 mb-4">
        <span className="text-2xl">🤖</span>
        <h3 className="text-lg font-bold text-gray-800">MiniMax AI 对话设置</h3>
      </div>
      
      <p className="text-sm text-gray-500 mb-4">
        配置MiniMax API密钥后，可以直接与AI助手对话，咨询学术文献相关问题。
      </p>
      
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            API 密钥
          </label>
          <div className="relative">
            <input
              type={showKey ? 'text' : 'password'}
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder="sk-..."
              className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 pr-12"
            />
            <button
              type="button"
              onClick={() => setShowKey(!showKey)}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
            >
              {showKey ? '🙈' : '👁️'}
            </button>
          </div>
        </div>
        
        <div className="flex gap-3">
          <button
            onClick={handleSave}
            className="flex-1 py-3 px-4 bg-gradient-to-r from-blue-500 to-cyan-500 text-white font-medium rounded-xl hover:from-blue-600 hover:to-cyan-600 transition-all shadow-sm"
          >
            {saved ? '✅ 已保存' : '💾 保存配置'}
          </button>
          
          {apiKey && (
            <button
              onClick={handleClear}
              className="py-3 px-4 bg-gray-100 text-gray-600 font-medium rounded-xl hover:bg-gray-200 transition-all"
            >
              🗑️ 清除
            </button>
          )}
        </div>
        
        <a 
          href="https://platform.minimax.io/docs/guides/text-chat"
          target="_blank"
          rel="noopener noreferrer"
          className="block text-center text-sm text-blue-500 hover:text-blue-700 transition-colors"
        >
          📖 查看MiniMax API文档
        </a>
      </div>
    </div>
  )
}
