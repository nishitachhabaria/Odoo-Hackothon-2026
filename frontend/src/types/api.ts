export interface ApiResponse<T> {
  message: string;
  data: T;
}

export interface UserSession {
  id: string;
  email: string;
  name: string;
  department_id?: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}
