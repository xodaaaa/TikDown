import { useEffect, useRef, useState } from "react";
import { useEventSource } from "../../hooks/useEventSource";
import type { ActivityEvent } from "../../types";

export default function ActivityFeed() {
  const [events, setEvents] = useState<ActivityEvent[]>([]);
  const [autoScroll, setAutoScroll] = useState(true);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEventSource((event) => {
    setEvents((prev) => [...prev.slice(-200), event]);
  });

  useEffect(() => {
    if (autoScroll && bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [events, autoScroll]);

  return (
    <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold">Activity Feed</h2>
        <label className="flex items-center gap-2 text-sm text-gray-400 cursor-pointer">
          <input type="checkbox" checked={autoScroll} onChange={(e) => setAutoScroll(e.target.checked)} />
          Auto-scroll
        </label>
      </div>
      <div className="bg-gray-950 rounded-lg p-4 h-64 overflow-y-auto font-mono text-xs">
        {events.length === 0 && (
          <p className="text-gray-600 text-center mt-20">Waiting for events...</p>
        )}
        {events.map((evt, i) => (
          <div key={i} className="py-1 border-b border-gray-900 last:border-0">
            <span className="text-accent-400">{evt.type}</span>
            <span className="text-gray-600 ml-2">
              {JSON.stringify(evt.payload)}
            </span>
          </div>
        ))}
        <div ref={bottomRef} />
      </div>
    </div>
  );
}
