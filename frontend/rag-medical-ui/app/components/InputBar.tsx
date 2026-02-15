"use client";
import { useState } from "react";

type Props = {
  onSend: (msg: string) => void;
};

export default function InputBar({ onSend }: Props) {
  const [value, setValue] = useState("");

  return (
    <div className="flex items-center gap-3 bg-[#0a0f1e] px-6 py-4">
      <textarea
        className="flex-1 resize-none bg-[#1e293b] text-white
                   px-4 py-3 rounded-xl focus:outline-none"
        placeholder="Type a medical question..."
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            onSend(value);
            setValue("");
          }
        }}
      />

      <button
        onClick={() => {
          onSend(value);
          setValue("");
        }}
        className="bg-emerald-500 text-black px-6 py-3 rounded-xl font-medium"
      >
        Send
      </button>
    </div>
  );
}
