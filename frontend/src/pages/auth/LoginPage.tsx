import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Eye, EyeOff, Lock, Mail, ShieldCheck } from "lucide-react";
import { z } from "zod";

const loginSchema = z.object({
  email: z.string().email("Enter a valid email"),
  password: z.string().min(6, "Password must be at least 6 characters"),
  remember: z.boolean().optional(),
});

type LoginForm = z.infer<typeof loginSchema>;

export function LoginPage() {
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginForm>({ resolver: zodResolver(loginSchema) });

  const navigate = useNavigate();

  const onSubmit = (values: LoginForm) => {
    setLoading(true);
    window.setTimeout(() => {
      setLoading(false);
      navigate("/dashboard");
    }, 1000);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <div className="mx-auto flex min-h-screen max-w-6xl items-center justify-center px-4 py-12 sm:px-6 lg:px-8">
        <div className="w-full rounded-[2rem] border border-white/10 bg-slate-900/90 p-10 shadow-soft backdrop-blur-xl sm:p-14">
          <div className="mb-10 text-center">
            <div className="mb-4 inline-flex h-16 w-16 items-center justify-center rounded-3xl bg-blue-500 text-3xl font-bold text-white">A</div>
            <h1 className="text-3xl font-semibold">Welcome back to AssetFlow</h1>
            <p className="mt-2 text-slate-400">Securely access your ERP workspace and manage assets, bookings, and teams.</p>
          </div>

          <form className="space-y-6" onSubmit={handleSubmit(onSubmit)}>
            <div className="rounded-3xl border border-slate-800 bg-slate-950/80 p-4">
              <label className="mb-2 block text-sm font-medium text-slate-300">Email</label>
              <div className="flex items-center gap-3 rounded-3xl bg-slate-900 px-4 py-3">
                <Mail className="h-5 w-5 text-slate-500" />
                <input
                  {...register("email")}
                  type="email"
                  placeholder="name@company.com"
                  className="w-full bg-transparent text-white outline-none placeholder:text-slate-500"
                />
              </div>
              {errors.email && <p className="mt-2 text-sm text-rose-400">{errors.email.message}</p>}
            </div>

            <div className="rounded-3xl border border-slate-800 bg-slate-950/80 p-4">
              <label className="mb-2 block text-sm font-medium text-slate-300">Password</label>
              <div className="flex items-center gap-3 rounded-3xl bg-slate-900 px-4 py-3">
                <Lock className="h-5 w-5 text-slate-500" />
                <input
                  {...register("password")}
                  type={showPassword ? "text" : "password"}
                  placeholder="Enter your password"
                  className="w-full bg-transparent text-white outline-none placeholder:text-slate-500"
                />
                <button type="button" onClick={() => setShowPassword(!showPassword)} className="text-slate-400 transition-default hover:text-white">
                  {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                </button>
              </div>
              {errors.password && <p className="mt-2 text-sm text-rose-400">{errors.password.message}</p>}
            </div>

            <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
              <label className="inline-flex items-center gap-2 text-sm text-slate-300">
                <input type="checkbox" {...register("remember")} className="h-4 w-4 rounded border-slate-600 text-blue-500 focus:ring-blue-400" />
                Remember me
              </label>
              <button type="button" className="text-sm text-blue-400 hover:text-blue-200">Forgot password?</button>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="inline-flex w-full items-center justify-center rounded-3xl bg-blue-600 px-6 py-4 text-base font-semibold text-white transition-default hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-slate-500"
            >
              {loading ? "Signing in..." : "Sign in"}
            </button>
          </form>

          <div className="mt-8 rounded-3xl border border-slate-800 bg-slate-950/80 p-6 text-sm text-slate-400">
            <p className="text-center">Use your ERP credentials to access the AssetFlow dashboard and manage workflows seamlessly.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
