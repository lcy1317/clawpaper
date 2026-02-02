import { NextResponse } from 'next/server'
import { getAllPapers, getStats, importFromJSON } from '@/lib/db'
import path from 'path'

export async function GET(request) {
  try {
    const { searchParams } = new URL(request.url)
    const project = searchParams.get('project')
    
    // 只允许 trust-literature 项目访问数据，其他项目暂无数据
    if (project !== 'trust-literature') {
      return NextResponse.json({ 
        papers: [], 
        stats: { total: 0, q1: 0, q2: 0, q3: 0, ei: 0 },
        message: '该项目的文献数据正在整理中'
      })
    }
    
    const papers = getAllPapers(project)
    const stats = getStats()
    
    if (papers.length === 0) {
      try {
        const papersPath = path.join(process.cwd(), 'papers.json')
        const count = importFromJSON(papersPath)
        if (count > 0) {
          return NextResponse.json({
            papers: getAllPapers(project),
            stats: getStats(),
            imported: count
          })
        }
      } catch (e) {
        console.log('JSON导入跳过，继续使用空数据')
      }
    }
    
    return NextResponse.json({ papers, stats })
  } catch (error) {
    console.error('API错误:', error)
    return NextResponse.json({ error: error.message }, { status: 500 })
  }
}
