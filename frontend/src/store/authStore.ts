import { createContext, useContext, useEffect, useState } from "react";
import type { UserSession } from "../types/api";

interface AuthContextValue {
  user: UserSession | null;
  setUser: (user: UserSession | null) => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<UserSession | null>(null);

  useEffect(() => {
    const stored = window.localStorage.getItem("assetflow_user");
    if (stored) {
      setUser(JSON.parse(stored));
    }
  }, []);

  useEffect(() => {
    if (user) {
      window.localStorage.setItem("assetflow_user", JSON.stringify(user));
    } else {
      window.localStorage.removeItem("assetflow_user");
    }
  }, [user]);

  return <AuthContext.Provider value={{ user, setUser }}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
}
