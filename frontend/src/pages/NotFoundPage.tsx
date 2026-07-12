import { Link } from "react-router-dom";

export function NotFoundPage() {
  return (
    <div className="mx-auto flex max-w-3xl flex-col items-center justify-center rounded-[2rem] border border-slate-200 bg-white p-12 text-center shadow-soft">
      <h1 className="mb-4 text-5xl font-bold text-slate-900">404</h1>
      <p className="mb-6 text-lg text-slate-600">Page not found. The requested route does not exist.</p>
      <Link className="rounded-2xl bg-blue-600 px-6 py-3 text-sm font-semibold text-white transition-default hover:bg-blue-700" to="/">
        Return to dashboard
      </Link>
    </div>
  );
}
