export default function Sidebar() {
  const sections = [
    {
      heading: "Command",
      items: [
        "Dashboard",
      ],
    },
    {
      heading: "Growth",
      items: [
        "Ventures",
        "Opportunities",
        "Projects",
      ],
    },
    {
      heading: "Wealth",
      items: [
        "Assets",
        "Capital",
      ],
    },
    {
      heading: "Execution",
      items: [
        "Tasks",
        "Knowledge",
      ],
    },
    {
      heading: "Impact",
      items: [
        "Community",
      ],
    },
    {
      heading: "System",
      items: [
        "Settings",
      ],
    },
  ];

  return (
    <aside className="w-72 bg-gradient-to-b from-[#132238] to-[#1D4E89] text-white shadow-2xl overflow-y-auto">
      <div className="p-6 border-b border-white/10">
        <h1 className="text-3xl font-bold">
          Cerebro
        </h1>

        <p className="text-sm text-blue-200 mt-1">
          Personal Intelligence System
        </p>
      </div>

      <nav className="p-4">
        {sections.map((section) => (
          <div
            key={section.heading}
            className="mb-8"
          >
            <h2 className="text-xs uppercase tracking-widest text-blue-300 mb-3 px-3">
              {section.heading}
            </h2>

            {section.items.map((item) => (
              <button
                key={item}
                className="
                  w-full
                  text-left
                  px-4
                  py-3
                  rounded-2xl
                  mb-2
                  transition-all
                  hover:bg-white/10
                  hover:translate-x-1
                "
              >
                {item}
              </button>
            ))}
          </div>
        ))}
      </nav>
    </aside>
  );
}