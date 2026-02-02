import '../styles/globals.css'

export const metadata = {
  title: 'ClawPaper - 学术文献平台',
  description: '学术文献管理平台',
}

export default function RootLayout({ children }) {
  return (
    <html lang="zh-CN">
      <body className="antialiased">{children}</body>
    </html>
  )
}
