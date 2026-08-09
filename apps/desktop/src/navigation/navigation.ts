export type NavigationItem = {
  id: string;
  label: string;
};

export const navigation: NavigationItem[] = [
  { id: "dashboard", label: "Dashboard" },
  { id: "agents", label: "Agents" },
  { id: "workflows", label: "Workflows" },
  { id: "review", label: "Review" },
  { id: "settings", label: "Settings" },
];
