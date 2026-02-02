'use client'

import { useState, useRef, useEffect } from 'react'

export default function AIChat({ apiKey, onClose }) {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: '你好！我是学术文献助手 🤖\n\n我可以帮助你：\n- 解答关于AI可信度的问题\n- 推荐相关学术论文\n- 解释信任评估方法\n- 分析研究趋势\n\n有什么可以帮你的吗？'
    }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSend = async () => {
    if (!input.trim() || loading) return
    
    const userMessage = { role: 'user', content: input.trim() }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)
    
    try {
      const history = messages.map(m => ({ role: m.role, content: m.content }))
      
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: userMessage.content,
          apiKey,
          history
        })
      })
      
      const data = await res.json()
      
      if (data.error) {
        setMessages(prev => [...prev, {
          role: 'assistant',
          content: `❌ 错误：${data.error}`
        }])
      } else {
        setMessages(prev => [...prev, {
          role: 'assistant',
          content: data.message
        }])
      }
    } catch (error) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: '抱歉，网络错误，请稍后重试。'
      }])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="fixed bottom-0 right-4 w-96 h-[32rem] bg-white rounded-t-2xl shadow-2xl border border-gray-200 flex flex-col z-50">
      {/* 头部 */}
      <div className="flex items-center justify-between p-4 border-b border-gray-100 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-t-2xl">
        <div className="flex items-center gap-3">
          <span className="text-2xl">🤖</span>
          <div>
            <h3 className="text-white font-bold">学术文献助手</h3>
            <p className="text-xs text-white/80">MiniMax AI</p>
          </div>
        </div>
        <button
          onClick={onClose}
          className="text-white/80 hover:text-white text-2xl transition-colors"
        >
          ×
        </button>
      </div>
      
      {/* 消息列表 */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[85%] rounded-2xl px-4 py-3 ${
                msg.role === 'user'
                  ? 'bg-gradient-to-r from-blue-500 to-cyan-500 text-white rounded-br-md'
                  : 'bg-white border border-gray-200 text-gray-800 rounded-bl-md shadow-sm'
              }`}
            >
              <div className="whitespace-pre-wrap text-sm leading-relaxed">
                {msg.content}
              </div>
            </div>
          </div>
        ))}
        
        {loading && (
          <div className="flex justify-start">
            <div className="bg-white border border-gray-200 rounded-2xl rounded-bl-md px-4 py-3 shadow-sm">
              <div className="flex gap-1">
                <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></span>
                <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></span>
                <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></span>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>
      
      {/* 输入框 */}
      <div className="p-4 border-t border-gray-100 bg-white rounded-b-2xl">
        <div className="flex gap-3">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="输入问题..."
            rows={1}
            className="flex-1 px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || loading}
            className={`px-6 py-3 rounded-xl font-medium transition-all ${
              input.trim() && !loading
                ? 'bg-gradient-to-r from-blue-500 to-cyan-500 text-white hover:from-blue-600 hover:to-cyan-600 shadow-lg shadow-blue-500/25'
                : 'bg-gray-100 text-gray-400 cursor-not-allowed'
            }`}
          >
            {loading ? '...' : '发送'}
          </button>
        </div>
      </div>
    </div>
  )
}
