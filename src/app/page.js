import Link from 'next/link'

const PROJECTS = [
  {
    id: 'trust-literature',
    name: '信任度文献调研',
    description: '深度调研系统信任度评估文献',
    icon: '📚',
    color: 'from-blue-500 to-cyan-500',
    count: 1000
  },
  {
    id: 'quant-papers',
    name: '量化论文分析',
    description: '量化交易相关学术论文与策略研究',
    icon: '📈',
    color: 'from-purple-500 to-pink-500',
    count: 500
  },
  {
    id: 'ai-safety',
    name: 'AI安全研究',
    description: '人工智能安全、对齐与伦理研究',
    icon: '🔒',
    color: 'from-red-500 to-orange-500',
    count: 300
  }
]

export default function Home() {
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
            <p className="text-gray-400 mt-2">收录1000+篇高质量学术论文</p>
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
                  <span className="text-sm text-gray-400">{project.count} 篇文献</span>
                  <span className="text-blue-500 group-hover:translate-x-1 transition-transform">→</span>
                </div>
              </Link>
            ))}
          </main>

          {/* 底部 */}
          <footer className="mt-16 text-center text-gray-400 text-sm py-8 border-t border-gray-200">
            <p>© 2026 ClawPaper · 学术文献管理平台</p>
          </footer>
        </div>
      </div>
    </div>
  )
}
