import { useState } from "react";
import { navigation, type NavigationItem } from "./navigation/navigation";
import { DashboardPage } from "./pages/DashboardPage";
import { PlaceholderPage } from "./pages/PlaceholderPage";

export default function App() {
  const [activePage, setActivePage] = useState<NavigationItem>(navigation[0]);

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">ClipStudio AI</div>
        <nav aria-label="Main navigation">
          {navigation.map((item) => (
            <button
              className={item.id === activePage.id ? "nav-item active" : "nav-item"}
              key={item.id}
              onClick={() => setActivePage(item)}
            >
              {item.label}
            </button>
          ))}
        </nav>
      </aside>
      <main className="content">
        {activePage.id === "dashboard" ? (
          <DashboardPage />
        ) : (
          <PlaceholderPage title={activePage.label} />
        )}
      </main>
    </div>
  );
}
