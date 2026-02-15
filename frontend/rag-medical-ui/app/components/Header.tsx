export default function Header() {
  return (
    <header className="flex items-center justify-between px-6 py-4 border-b border-slate-700">
      <div>
        <h1 className="text-2xl font-bold text-teal-400">
          RAG Medical Chatbot
        </h1>
        <p className="text-sm text-slate-400">
          Retrieval-Augmented AI Medical Assistant
        </p>
      </div>

      <input
        type="text"
        placeholder="Search chats..."
        className="bg-[#1e293b] text-white px-4 py-2 rounded-lg
                   focus:outline-none focus:ring-2 focus:ring-teal-400"
      />
    </header>
  );
}
