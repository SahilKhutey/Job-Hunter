import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const PROTECTED_ROUTES = ["/dashboard", "/automation", "/profile"];

export function middleware(req: NextRequest) {
  // Note: Middleware can only access Cookies, not LocalStorage.
  // For now, we'll keep this as a placeholder for when we migrate refresh tokens to HTTP-only cookies.
  const refreshToken = req.cookies.get("refresh_token")?.value;

  const isProtected = PROTECTED_ROUTES.some((route) =>
    req.nextUrl.pathname.startsWith(route)
  );

  // If we move to cookies, this will work. 
  // For now, client-side guards in ClientRoot handle the redirection.
  if (isProtected && !refreshToken) {
    // return NextResponse.redirect(new URL("/login", req.url));
  }

  return NextResponse.next();
}
