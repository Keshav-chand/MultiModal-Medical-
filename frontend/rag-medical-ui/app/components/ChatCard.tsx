import ReactMarkdown from "react-markdown";

type Props = {
  role: "user" | "assistant";
  content: string;
};

export default function ChatCard({ role, content }: Props) {
  return (
    <div
      className={`max-w-[80%] p-4 rounded-xl shadow-lg text-sm leading-relaxed
        ${
          role === "user"
            ? "ml-auto bg-teal-600 text-white"
            : "mr-auto bg-white text-slate-800"
        }`}
    >
      <ReactMarkdown
        components={{
          strong: ({ children }) => (
            <strong className="block mt-3 font-semibold text-slate-900">
              {children}
            </strong>
          ),
          li: ({ children }) => (
            <li className="ml-4 list-disc">{children}</li>
          ),
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}
