import { useEffect, useState } from "react";

export function useTheme() {
  const [theme, setTheme] = useState<"light" | "dark">("light");

  useEffect(() => {
    const stored = window.localStorage.getItem("assetflow_theme");
    setTheme(stored === "dark" ? "dark" : "light");
  }, []);

  useEffect(() => {
    document.documentElement.classList.toggle("dark", theme === "dark");
    window.localStorage.setItem("assetflow_theme", theme);
  }, [theme]);

  return { theme, toggleTheme: () => setTheme((prev) => (prev === "dark" ? "light" : "dark")) };
}
