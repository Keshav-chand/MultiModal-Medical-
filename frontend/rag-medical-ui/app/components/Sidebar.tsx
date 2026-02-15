"use client";
import { Home, MessageSquare, Clock, Settings } from "lucide-react";

export default function Sidebar() {
  return (
    <aside className="w-16 bg-[#0a0f1e] flex flex-col items-center py-4 gap-6">
      <Home className="text-teal-400" />
      <MessageSquare className="text-gray-400 hover:text-teal-400 cursor-pointer" />
      <Clock className="text-gray-400 hover:text-teal-400 cursor-pointer" />
      <Settings className="text-gray-400 hover:text-teal-400 cursor-pointer mt-auto" />
    </aside>
  );
}
