/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  reactStrictMode: true,
  async rewrites() {
    return [
      {
        source: '/api/clawpaper/:path*',
        destination: 'http://localhost:5001/:path*',
      },
    ]
  },
}

module.exports = nextConfig
