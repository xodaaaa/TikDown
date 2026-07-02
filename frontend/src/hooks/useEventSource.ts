import { useEffect, useRef, useState } from "react";
import type { ActivityEvent } from "../types";

export function useEventSource(onEvent?: (event: ActivityEvent) => void) {
  const [connected, setConnected] = useState(false);
  const retryRef = useRef(0);

  useEffect(() => {
    let es: EventSource | null = null;
    let timeout: ReturnType<typeof setTimeout>;

    function connect() {
      es = new EventSource("/api/events", { withCredentials: true });

      es.onopen = () => {
        setConnected(true);
        retryRef.current = 0;
      };

      es.onmessage = (evt) => {
        try {
          const data = JSON.parse(evt.data) as ActivityEvent;
          onEvent?.(data);
        } catch {
          // ignore parse errors (e.g., ping events)
        }
      };

      es.onerror = () => {
        setConnected(false);
        es?.close();
        const delay = Math.min(1000 * 2 ** retryRef.current, 30_000);
        retryRef.current++;
        timeout = setTimeout(connect, delay);
      };
    }

    connect();

    return () => {
      es?.close();
      clearTimeout(timeout);
    };
  }, [onEvent]);

  return { connected };
}
