import { useState } from "react";

export default function NotificationsSettings() {
  const [enabled, setEnabled] = useState(false);
  const [telegramToken, setTelegramToken] = useState("");
  const [telegramChat, setTelegramChat] = useState("");
  const [discordWebhook, setDiscordWebhook] = useState("");
  const [genericWebhook, setGenericWebhook] = useState("");
  const [genericSecret, setGenericSecret] = useState("");

  return (
    <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
      <h3 className="text-lg font-semibold mb-4">Notifications</h3>

      <label className="flex items-center gap-3 mb-4 cursor-pointer">
        <input
          type="checkbox"
          checked={enabled}
          onChange={(e) => setEnabled(e.target.checked)}
          className="w-4 h-4 rounded border-gray-600 bg-gray-800 text-accent-500 focus:ring-accent-500"
        />
        <span className="text-sm text-gray-300">Enable external notifications</span>
      </label>

      {enabled && (
        <div className="space-y-4">
          <details className="bg-gray-800/50 rounded-lg p-4">
            <summary className="text-sm text-gray-300 cursor-pointer">Telegram</summary>
            <div className="mt-3 space-y-2">
              <input type="text" value={telegramToken} onChange={(e) => setTelegramToken(e.target.value)} placeholder="Bot Token" className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-sm text-gray-200" />
              <input type="text" value={telegramChat} onChange={(e) => setTelegramChat(e.target.value)} placeholder="Chat ID" className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-sm text-gray-200" />
              <button className="px-3 py-1 text-xs bg-gray-700 text-gray-400 hover:text-gray-200 rounded">Test</button>
            </div>
          </details>

          <details className="bg-gray-800/50 rounded-lg p-4">
            <summary className="text-sm text-gray-300 cursor-pointer">Discord</summary>
            <div className="mt-3 space-y-2">
              <input type="text" value={discordWebhook} onChange={(e) => setDiscordWebhook(e.target.value)} placeholder="Webhook URL" className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-sm text-gray-200" />
              <button className="px-3 py-1 text-xs bg-gray-700 text-gray-400 hover:text-gray-200 rounded">Test</button>
            </div>
          </details>

          <details className="bg-gray-800/50 rounded-lg p-4">
            <summary className="text-sm text-gray-300 cursor-pointer">Generic Webhook</summary>
            <div className="mt-3 space-y-2">
              <input type="text" value={genericWebhook} onChange={(e) => setGenericWebhook(e.target.value)} placeholder="Webhook URL" className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-sm text-gray-200" />
              <input type="text" value={genericSecret} onChange={(e) => setGenericSecret(e.target.value)} placeholder="HMAC Secret (optional)" className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-sm text-gray-200" />
              <button className="px-3 py-1 text-xs bg-gray-700 text-gray-400 hover:text-gray-200 rounded">Test</button>
            </div>
          </details>
        </div>
      )}
    </div>
  );
}
