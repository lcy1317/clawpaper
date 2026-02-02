const Database = require('better-sqlite3')
const fs = require('fs')
const path = require('path')

const DB_PATH = path.join(process.cwd(), 'data', 'papers.db')

// 确保数据目录存在
const dataDir = path.dirname(DB_PATH)
if (!fs.existsSync(dataDir)) {
  fs.mkdirSync(dataDir, { recursive: true })
}

const db = new Database(DB_PATH)

// 初始化数据库表
db.exec(`
  CREATE TABLE IF NOT EXISTS papers (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    authors TEXT,
    year INTEGER,
    venue TEXT,
    abstract TEXT,
    institution TEXT,
    citations INTEGER DEFAULT 0,
    ranking TEXT,
    impact_factor REAL,
    impact_factor_label TEXT,
    publisher TEXT,
    access_url TEXT,
    doi TEXT,
    bibtex TEXT,
    file_path TEXT,
    key_contributions TEXT,
    evaluation_method TEXT,
    trust_dimensions TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
  )
`)

db.exec(`
  CREATE TABLE IF NOT EXISTS projects (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    color TEXT,
    paper_count INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  )
`)

db.exec(`
  CREATE TABLE IF NOT EXISTS pdf_files (
    id TEXT PRIMARY KEY,
    paper_id TEXT,
    filename TEXT,
    file_path TEXT,
    file_size INTEGER,
    mime_type TEXT,
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (paper_id) REFERENCES papers(id)
  )
`)

// 插入默认项目
const insertProject = db.prepare(`
  INSERT OR IGNORE INTO projects (id, name, description, color, paper_count)
  VALUES (?, ?, ?, ?, ?)
`)

insertProject.run('trust-literature', '信任度文献调研', '深度调研系统信任度评估文献', 'from-blue-500 to-cyan-500', 1000)
insertProject.run('quant-papers', '量化论文分析', '量化交易相关学术论文与策略研究', 'from-purple-500 to-pink-500', 500)
insertProject.run('ai-safety', 'AI安全研究', '人工智能安全、对齐与伦理研究', 'from-red-500 to-orange-500', 300)

// 从JSON导入数据
function importFromJSON(jsonPath) {
  try {
    const data = JSON.parse(fs.readFileSync(jsonPath, 'utf-8'))
    const papers = data.papers || []
    
    const insert = db.prepare(`
      INSERT OR REPLACE INTO papers (
        id, title, authors, year, venue, abstract, institution, citations,
        ranking, impact_factor, impact_factor_label, publisher, 
        access_url, doi, bibtex, key_contributions, evaluation_method, trust_dimensions
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `)
    
    const importMany = db.transaction((papers) => {
      for (const paper of papers) {
        insert.run(
          paper.id,
          paper.title,
          JSON.stringify(paper.authors || []),
          paper.year,
          paper.venue,
          paper.abstract,
          paper.institution,
          paper.citations || 0,
          paper.journal_info?.ranking || null,
          paper.journal_info?.impact_factor || null,
          paper.journal_info?.impact_factor_label || null,
          paper.journal_info?.publisher || null,
          paper.journal_info?.access_url || null,
          paper.journal_info?.doi || null,
          paper.bibtex || null,
          JSON.stringify(paper.key_contributions || []),
          JSON.stringify(paper.evaluation_method || {}),
          JSON.stringify(paper.trust_dimensions || {})
        )
      }
    })
    
    importMany(papers)
    console.log(`✅ 成功导入 ${papers.length} 篇文献到 SQLite`)
    return papers.length
  } catch (error) {
    console.error('导入失败:', error)
    return 0
  }
}

// 获取所有文献
function getAllPapers(project = null) {
  let query = 'SELECT * FROM papers'
  const params = []
  
  if (project === 'trust-literature') {
    query += ' WHERE trust_dimensions IS NOT NULL AND trust_dimensions != ?'
    params.push('{}')
  }
  
  query += ' ORDER BY year DESC, impact_factor DESC'
  
  console.log('SQL Query:', query)
  console.log('Params:', params)
  
  const stmt = db.prepare(query)
  const rows = stmt.all(...params)
  
  return rows.map(row => ({
    ...row,
    authors: JSON.parse(row.authors || '[]'),
    key_contributions: JSON.parse(row.key_contributions || '[]'),
    evaluation_method: JSON.parse(row.evaluation_method || '{}'),
    trust_dimensions: JSON.parse(row.trust_dimensions || '{}'),
    journal_info: {
      ranking: row.ranking,
      impact_factor: row.impact_factor,
      impact_factor_label: row.impact_factor_label,
      publisher: row.publisher,
      access_url: row.access_url,
      doi: row.doi
    }
  }))
}

// 获取统计信息
function getStats() {
  const total = db.prepare('SELECT COUNT(*) as count FROM papers').get().count
  const q1 = db.prepare("SELECT COUNT(*) as count FROM papers WHERE ranking LIKE '%Q1%' OR ranking LIKE '%CCF-A%'").get().count
  const q2 = db.prepare("SELECT COUNT(*) as count FROM papers WHERE ranking LIKE '%Q2%' OR ranking LIKE '%CCF-B%'").get().count
  const q3 = db.prepare("SELECT COUNT(*) as count FROM papers WHERE ranking LIKE '%Q3%' OR ranking LIKE '%CCF-C%'").get().count
  const ei = db.prepare("SELECT COUNT(*) as count FROM papers WHERE ranking LIKE '%EI%'").get().count
  
  return { total, q1, q2, q3, ei }
}

module.exports = {
  db,
  importFromJSON,
  getAllPapers,
  getStats
}
