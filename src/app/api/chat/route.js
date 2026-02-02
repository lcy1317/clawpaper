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
    
    // 构建消息 - text-generation不需要role，用直接的prompt
    const prompt = `你是一个学术文献助手，专注于帮助用户解答关于AI可信度、软件供应链安全、零信任架构等学术问题。请用中文回答，保持专业且友好的语气。

用户问题：${message}

请回答：`
    
    // 调用MiniMax text-generation API
    const response = await fetch('https://api.minimax.chat/v1/text_generation/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`
      },
      body: JSON.stringify({
        model: 'MiniMax-M2.1', // 使用MiniMax-M2.1模型
        prompt: prompt,
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
    
    // text-generation返回格式不同
    const assistantMessage = data.choices?.[0]?.text || 
                             data.choices?.[0]?.message?.content || 
                             data.output?.[0]?.text ||
                             '抱歉，我暂时无法回答这个问题。'
    
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
