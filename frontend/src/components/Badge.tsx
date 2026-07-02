interface BadgeProps {
  children: React.ReactNode;
  variant?: "default" | "success" | "warning" | "danger";
}

const variants: Record<string, string> = {
  default: "bg-gray-700 text-gray-300",
  success: "bg-emerald-900/50 text-emerald-400",
  warning: "bg-amber-900/50 text-amber-400",
  danger: "bg-red-900/50 text-red-400",
};

export default function Badge({ children, variant = "default" }: BadgeProps) {
  return (
    <span className={`inline-flex items-center px-2 py-0.5 text-xs font-medium rounded-full ${variants[variant]}`}>
      {children}
    </span>
  );
}
