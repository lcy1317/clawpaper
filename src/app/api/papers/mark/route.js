import { NextResponse } from 'next/server'
const db = require('../../lib/db')

// 获取单篇论文的标记信息
export async function GET(request) {
  try {
    const { searchParams } = new URL(request.url)
    const paperId = searchParams.get('id')
    
    if (!paperId) {
      return NextResponse.json({ error: '缺少论文ID' }, { status: 400 })
    }
    
    const stmt = db.db.prepare('SELECT id, star_rating, notes, updated_at FROM papers WHERE id = ?')
    const paper = stmt.get(paperId)
    
    if (!paper) {
      return NextResponse.json({ error: '论文不存在' }, { status: 404 })
    }
    
    return NextResponse.json({
      id: paper.id,
      star_rating: paper.star_rating || 0,
      notes: paper.notes || '',
      updated_at: paper.updated_at
    })
  } catch (error) {
    console.error('获取论文标记失败:', error)
    return NextResponse.json({ error: '服务器错误' }, { status: 500 })
  }
}

// 更新论文的星级评分或备注
export async function POST(request) {
  try {
    const { id, star_rating, notes } = await request.json()
    
    if (!id) {
      return NextResponse.json({ error: '缺少论文ID' }, { status: 400 })
    }
    
    // 验证star_rating范围
    if (star_rating !== undefined && (star_rating < 0 || star_rating > 5)) {
      return NextResponse.json({ error: '星级评分必须在0-5之间' }, { status: 400 })
    }
    
    // 构建更新语句
    const updates = []
    const params = []
    
    if (star_rating !== undefined) {
      updates.push('star_rating = ?')
      params.push(star_rating)
    }
    
    if (notes !== undefined) {
      updates.push('notes = ?')
      params.push(notes)
    }
    
    if (updates.length === 0) {
      return NextResponse.json({ error: '没有可更新的字段' }, { status: 400 })
    }
    
    updates.push('updated_at = CURRENT_TIMESTAMP')
    params.push(id)
    
    const query = `UPDATE papers SET ${updates.join(', ')} WHERE id = ?`
    db.db.prepare(query).run(...params)
    
    // 获取更新后的数据
    const stmt = db.db.prepare('SELECT id, star_rating, notes, updated_at FROM papers WHERE id = ?')
    const paper = stmt.get(id)
    
    return NextResponse.json({
      success: true,
      data: {
        id: paper.id,
        star_rating: paper.star_rating || 0,
        notes: paper.notes || '',
        updated_at: paper.updated_at
      }
    })
  } catch (error) {
    console.error('更新论文标记失败:', error)
    return NextResponse.json({ error: '服务器错误' }, { status: 500 })
  }
}
