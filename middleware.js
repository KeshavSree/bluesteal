// middleware.js
export const config = {
  matcher: '/', // Only run on root path
};

export default function middleware(request) {
  const url = new URL(request.url);

  // Check for maintenance mode
  if (process.env.MAINTENANCE_MODE === '1') {
    // Only show maintenance for HTML requests
    const accept = request.headers.get('accept');
    if (accept && accept.includes('text/html')) {
      // Serve root-level maintenance.html
      url.pathname = '/maintenance.html';
      return Response.rewrite(url);
    }
  }

  // Otherwise continue as normal
  return new Response();
}