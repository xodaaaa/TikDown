export default function DashboardCards() {
  const cards = [
    { label: "Videos", value: "0", color: "text-accent-400" },
    { label: "Users", value: "0", color: "text-blue-400" },
    { label: "Views", value: "0", color: "text-emerald-400" },
    { label: "Likes", value: "0", color: "text-amber-400" },
    { label: "Saved", value: "0", color: "text-purple-400" },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 mb-6">
      {cards.map((card) => (
        <div key={card.label} className="bg-gray-900 border border-gray-800 rounded-xl p-4">
          <div className="text-gray-500 text-xs uppercase tracking-wider mb-1">{card.label}</div>
          <div className={`text-2xl font-bold ${card.color}`}>{card.value}</div>
        </div>
      ))}
    </div>
  );
}
