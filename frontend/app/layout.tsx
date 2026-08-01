import "./globals.css";
import Sidebar from "@/components/Sidebar";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <div className="flex h-screen">
          <Sidebar />

          <main className="flex-1 p-8 bg-white
rounded-3xl
shadow-[0_20px_50px_rgba(59,130,246,0.15)] overflow-y-auto">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}