import "./globals.css";
import { Inter } from "next/font/google";
import OurConsole from "./components/customConsole";

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "Nextjs with Flask",
  description: "Just a playground or more....?",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="h-[100vh] flex">
          {/* Left: Custom Console with Radial Gradient */}
          <div className="w-1/3 h-full bg-antiwhite  text-pakistan overflow-y-auto border-r-[2px] border-sage">
            <OurConsole />
          </div>

          {/* Right: Main Application Content with Conic Gradient */}
          <div className="w-2/3 h-full flex items-center justify-center bg-gradient-radial from-antiwhite via-seasalt">
            {children}
          </div>
        </div>
      </body>
    </html>
  );
}
