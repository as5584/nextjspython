import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Attendance Manager",
  description: "Attendance Manager — Next.js frontend",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
