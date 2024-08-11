import "./globals.css";
import { Inter } from "next/font/google";
import OurConsole from "./components/customConsole";

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "BellmanBot",
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
          <div className="w-1/3 h-full bg-antiwhite text-pakistan overflow-y-auto border-r-[2px] border-sage">
            <OurConsole />
          </div>

          {/* Right: Main Application Content with Background Image */}
          <div className="relative w-2/3 h-full flex items-center justify-center bg-gradient-radial from-antiwhite via-seasalt overflow-hidden">
            {/* SVG Background Image */}
            <img
              src="/bell.svg"
              alt="Background SVG"
              className="absolute max-w-[400px] w-[50%] h-auto object-contain opacity-[2%] blur-sm z-0"
              style={{
                top: "50%",
                left: "50%",
                transform: "translate(-50%, -50%)",
              }}
            />
            {/* Main Content */}
            <div className="relative z-10">{children}</div>
          </div>
        </div>
      </body>
    </html>
  );
}
