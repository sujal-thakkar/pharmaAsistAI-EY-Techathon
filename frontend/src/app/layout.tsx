import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "PharmaAssist AI - Multi-Agent Pharmaceutical Intelligence Platform",
  description: "AI-powered pharmaceutical research platform with multi-agent intelligence for drug discovery, clinical trials, market analysis, and regulatory insights.",
  keywords: ["pharmaceutical", "AI", "drug discovery", "clinical trials", "market analysis", "multi-agent"],
  authors: [{ name: "PharmaAssist AI Team" }],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${inter.variable} font-sans antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
