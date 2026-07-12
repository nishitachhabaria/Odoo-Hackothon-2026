import { api } from "./api";
import type { ApiResponse, LoginRequest, UserSession } from "../types/api";

export const authApi = {
  login: async (payload: LoginRequest) => {
    const response = await api.post<ApiResponse<{ token: string; user: UserSession }>>("/api/v1/auth/login", payload);
    return response.data;
  },
  me: async () => {
    const response = await api.get<ApiResponse<UserSession>>("/api/v1/auth/me");
    return response.data;
  },
};
