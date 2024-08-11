/** @type {import('next').NextConfig} */
const nextConfig = {
  rewrites: async () => {
    return [
      {
        source: "/api/:path*",
        destination: "http://server:5000/api/:path*",
      },
    ];
  },
};

module.exports = nextConfig;
