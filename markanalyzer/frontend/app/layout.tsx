import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Marks Analyzer",
  description: "Marks Analyzer — Next.js frontend",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
