/** @type {import('next').NextConfig} */
const API_TARGET = process.env.API_PROXY_TARGET || "http://127.0.0.1:8006";

const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    // Browser calls same-origin /backend/* -> Next proxies to FastAPI (no CORS)
    return [
      {
        source: "/backend/:path*",
        destination: `${API_TARGET}/:path*`,
      },
    ];
  },
};

export default nextConfig;
