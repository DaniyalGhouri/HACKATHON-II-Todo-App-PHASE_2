/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/auth/use-user',
        destination: '/api/auth/get-session',
      },
    ];
  },
};

export default nextConfig;