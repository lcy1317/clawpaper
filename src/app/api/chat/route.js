import { NextResponse } from 'next/server'

export async function POST(request) {
  try {
    const { message, apiKey, history } = await request.json()
    
    if (!apiKey) {
      return NextResponse.json({ 
        error: '请先配置MiniMax API密钥' 
      }, { status: 400 })
    }
    
    if (!message) {
      return NextResponse.json({ 
        error: '请输入问题' 
      }, { status: 400 })
    }
    
    // 构建消息历史 + 当前问题
    const messages = [
      {
        role: 'system',
        content: '你是一个学术文献助手，专注于帮助用户解答关于AI可信度、软件供应链安全、零信任架构等学术问题。请用中文回答，保持专业且友好的语气。'
      },
      ...(history || []).slice(-10), // 只保留最近10轮对话
      {
        role: 'user',
        content: message
      }
    ]
    
    // 调用MiniMax API
    const response = await fetch('https://api.minimax.chat/v1/text/chatcompletion_v2', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`
      },
      body: JSON.stringify({
        model: 'abab6.5s-chat', // 使用MiniMax的聊天模型
        messages: messages,
        temperature: 0.7,
        max_tokens: 2000
      })
    })
    
    const data = await response.json()
    
    if (data.error) {
      return NextResponse.json({ 
        error: data.error.message || 'MiniMax API错误' 
      }, { status: 500 })
    }
    
    const assistantMessage = data.choices?.[0]?.message?.content || '抱歉，我暂时无法回答这个问题。'
    
    return NextResponse.json({ 
      message: assistantMessage,
      role: 'assistant'
    })
    
  } catch (error) {
    console.error('Chat API error:', error)
    return NextResponse.json({ 
      error: '服务器错误，请稍后重试' 
    }, { status: 500 })
  }
}
