'use client';

import { useState, useEffect, useRef } from 'react';
import { useSession } from "@/lib/auth-client";
import { useRouter } from "next/navigation";
import Link from "next/link";

import { fetchWithAuth } from "@/lib/api-client";

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export default function ChatPage() {
  const { data: session, isPending } = useSession();
  const user = session?.user;
  const router = useRouter();
  
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!isPending && !user) {
      router.push("/login");
    }
  }, [user, isPending, router]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const sendMessage = async () => {
    if (!input.trim() || !user) return;

    const newMsg: Message = { role: 'user', content: input };
    setMessages(prev => [...prev, newMsg]);
    setInput('');
    setIsLoading(true);

    try {
      const res = await fetchWithAuth(`/api/chat`, {
        method: 'POST',
        body: JSON.stringify({
          message: newMsg.content,
          conversation_id: conversationId
        }),
      });
      
      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.detail || "Chat failed");
      }
      
      const data = await res.json();
      setConversationId(data.conversation_id);
      setMessages(prev => [...prev, { role: 'assistant', content: data.response }]);
    } catch (error) {
      console.error('Chat error:', error);
      setMessages(prev => [...prev, { role: 'assistant', content: "I encountered an error connecting to the service. Please check your connection." }]);
    } finally {
      setIsLoading(false);
    }
  };

  if (isPending || !user) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-white dark:bg-black">
        <div className="w-8 h-8 border-4 border-black border-t-transparent rounded-full animate-spin dark:border-white dark:border-t-transparent"></div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-screen bg-white dark:bg-black font-sans text-gray-900 dark:text-gray-100">
      {/* Header */}
      <header className="flex items-center justify-between px-6 py-4 border-b border-gray-100 dark:border-zinc-800 backdrop-blur-md bg-white/70 dark:bg-black/70 sticky top-0 z-10">
        <div className="flex items-center gap-4">
          <Link href="/dashboard" className="p-2 hover:bg-gray-100 dark:hover:bg-zinc-800 rounded-full transition-colors">
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
          </Link>
          <h1 className="text-lg font-bold tracking-tight">AI Assistant</h1>
        </div>
        <div className="flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-green-500 animate-pulse"></span>
            <span className="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-widest">Active</span>
        </div>
      </header>

      {/* Message Area */}
      <div className="flex-1 overflow-y-auto px-4 py-8 sm:px-6">
        <div className="max-w-3xl mx-auto space-y-8">
          {messages.length === 0 && (
            <div className="flex flex-col items-center justify-center py-20 text-center space-y-4">
                <div className="w-16 h-16 bg-gray-50 dark:bg-zinc-900 rounded-2xl flex items-center justify-center mb-2">
                    <svg className="w-8 h-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                    </svg>
                </div>
                <h2 className="text-2xl font-bold tracking-tight">How can I help you today?</h2>
                <p className="text-gray-500 dark:text-gray-400 max-w-sm">
                    I can help you manage tasks, set deadlines, and organize your productivity workflow.
                </p>
            </div>
          )}

          {messages.map((m, i) => (
            <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'} animate-in fade-in slide-in-from-bottom-2 duration-300`}>
              <div className={`max-w-[85%] sm:max-w-[75%] rounded-2xl px-5 py-3.5 ${
                m.role === 'user' 
                  ? 'bg-black text-white dark:bg-white dark:text-black shadow-lg' 
                  : 'bg-gray-50 text-gray-900 dark:bg-zinc-900 dark:text-gray-100 border border-gray-100 dark:border-zinc-800 shadow-sm'
              }`}>
                <div className="text-sm leading-relaxed whitespace-pre-wrap">
                  {m.content}
                </div>
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="flex justify-start animate-in fade-in duration-300">
              <div className="bg-gray-50 dark:bg-zinc-900 rounded-2xl px-5 py-3.5 border border-gray-100 dark:border-zinc-800">
                <div className="flex gap-1.5 items-center h-5">
                  <div className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce [animation-delay:0.2s]"></div>
                  <div className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce [animation-delay:0.4s]"></div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>
      
      {/* Input Area */}
      <div className="p-4 sm:p-6 border-t border-gray-100 dark:border-zinc-800 bg-white dark:bg-black">
        <div className="max-w-3xl mx-auto relative">
          <textarea 
            rows={1}
            className="w-full pl-4 pr-14 py-4 bg-gray-50 dark:bg-zinc-900 border-0 focus:ring-2 focus:ring-black dark:focus:ring-white rounded-2xl resize-none text-sm dark:text-white transition-all duration-200 shadow-inner"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    sendMessage();
                }
            }}
            placeholder="Ask me anything..."
          />
          <button 
            onClick={sendMessage}
            disabled={isLoading || !input.trim()}
            className="absolute right-2 top-1/2 -translate-y-1/2 p-2.5 bg-black dark:bg-white text-white dark:text-black rounded-xl hover:opacity-80 transition-all disabled:opacity-20 disabled:scale-95"
          >
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
            </svg>
          </button>
        </div>
        <p className="mt-3 text-[10px] text-center text-gray-400 dark:text-gray-500 uppercase tracking-widest font-medium">
            AI Assistant may provide inaccurate information. Check important info.
        </p>
      </div>
    </div>
  );
}