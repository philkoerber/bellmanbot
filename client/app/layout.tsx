import "./globals.css";
import { Inter } from "next/font/google";
import OurConsole from "./components/customConsole";
import Image from "next/image";

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
          <div className="w-1/3 h-full bg-antiwhite text-pakistan overflow-y-auto border-r-[2px] bg-gradient-to-tr from-antiwhite via-seasalt border-pakistan">
            <OurConsole />
          </div>

          {/* Right: Main Application*/}
          <div className="w-2/3 h-full bg-gradient-to-tr from-antiwhite via-seasalt overflow-x-hidden relative">
            <div className="relative z-10">{children}</div>
          </div>
          {/* Background Image*/}
          <div className="fixed flex justify-center items-center">
            <Image
              width={400}
              height={400}
              src="/bell.svg"
              alt="Background SVG"
              className="fixed max-w-[400px] w-[50%] h-auto object-contain opacity-[15%] blur-sm z-0"
              style={{
                top: "50%",
                left: "66%",
                transform: "translate(-50%, -50%)",
              }}
            />
          </div>
        </div>
      </body>
    </html>
  );
}
