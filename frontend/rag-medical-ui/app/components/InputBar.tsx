"use client";
import { useState, useRef } from "react";

export default function InputBar({
  onSend,
  onImageUpload,
}: {
  onSend: (text: string) => void;
  onImageUpload: (file: File) => void;
}) {
  const [text, setText] = useState("");
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSend = () => {
    if (!text.trim()) return;
    onSend(text);
    setText("");
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      handleSend();
    }
  };

  const handleFileChange = (e: any) => {
    const file = e.target.files[0];
    if (file) {
      onImageUpload(file);
    }
  };

  return (
    <div className="flex items-center gap-3 p-4 bg-[#1e293b]">
      <input
        className="flex-1 p-3 rounded-lg bg-[#0f172a] text-white outline-none"
        placeholder="Type a medical question..."
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={handleKeyDown}
      />

      <button
        onClick={() => fileInputRef.current?.click()}
        className="bg-[#334155] text-white px-4 py-2 rounded-lg"
      >
        📎
      </button>

      <input
        type="file"
        accept="image/*"
        hidden
        ref={fileInputRef}
        onChange={handleFileChange}
      />

      <button
        onClick={handleSend}
        className="bg-green-500 px-5 py-2 rounded-lg text-black font-semibold"
      >
        Send
      </button>
    </div>
  );
}