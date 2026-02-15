"use client";
import { useState } from "react";
import Sidebar from "@/app/components/Sidebar";
import Header from "@/app/components/Header";
import ChatCard from "@/app/components/ChatCard";
import InputBar from "@/app/components/InputBar";

type Message = {
  role: "user" | "assistant";
  content: string;
};

export default function Page() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "user",
      content: "What can I do to improve my cholesterol levels naturally?",
    },
    {
      role: "assistant",
      content:
        "Focus on a heart-healthy diet, regular exercise, quitting smoking, and limiting saturated fats.",
    },
  ]);

  const sendMessage = async (text: string) => {
    if (!text.trim()) return;

    setMessages((prev) => [...prev, { role: "user", content: text }]);

    const res = await fetch("http://localhost:5000/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: text }),
    });

    const data = await res.json();

    setMessages((prev) => [
      ...prev,
      { role: "assistant", content: data.answer || "No response" },
    ]);
  };

  return (
    <div className="h-screen flex bg-gradient-to-br from-[#0a0f1e] to-[#1e293b]">
      <Sidebar />

      <main className="flex flex-col flex-1">
        <Header />

        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.map((msg, i) => (
            <ChatCard key={i} role={msg.role} content={msg.content} />
          ))}
        </div>

        <InputBar onSend={sendMessage} />
      </main>
    </div>
  );
}
