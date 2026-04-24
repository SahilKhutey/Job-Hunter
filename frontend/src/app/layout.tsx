import "./globals.css";
import ClientRoot from "@/components/layout/ClientRoot";

export const metadata = {
  title: "AI Job Hunter OS",
  description: "AI-Powered Multi-Agent Job Application Platform",
  keywords: "AI, jobs, automation, resume, career",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <link rel="manifest" href="/manifest.json" />
        <meta name="theme-color" content="#7c3aed" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
      </head>
      <body className="bg-neutral-950 text-white">
        <ClientRoot>{children}</ClientRoot>
      </body>
    </html>

  );
}
