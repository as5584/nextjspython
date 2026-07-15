import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Resume Keyword Checker",
  description: "Resume Keyword Checker — Next.js frontend",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
