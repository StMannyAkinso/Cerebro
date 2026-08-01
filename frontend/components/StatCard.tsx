interface StatCardProps {
  title: string;
  value: string | number;
}

export default function StatCard({
  title,
  value,
}: StatCardProps) {
  return (
    <div className="rounded-3xl bg-white p-6 shadow-lg">
      <h2 className="text-sm text-gray-600">
        {title}
      </h2>

      <p className="mt-2 text-3xl text-gray-800 font-bold">
        {value}
      </p>
    </div>
  );
}