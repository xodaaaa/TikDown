interface ProgressBarProps {
  value: number;
  max: number;
  label?: string;
}

export default function ProgressBar({ value, max, label }: ProgressBarProps) {
  const pct = max > 0 ? Math.min((value / max) * 100, 100) : 0;

  return (
    <div className="w-full">
      {label && <div className="text-xs text-gray-400 mb-1">{label}</div>}
      <div className="w-full bg-gray-800 rounded-full h-2">
        <div
          className="bg-accent-500 h-2 rounded-full transition-all duration-300"
          style={{ width: `${pct}%` }}
        />
      </div>
      <div className="text-xs text-gray-500 mt-0.5 text-right">
        {value}/{max}
      </div>
    </div>
  );
}
