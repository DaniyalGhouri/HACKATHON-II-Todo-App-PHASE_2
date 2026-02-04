import { AuthForm } from "@/components/auth-form";

export default function LoginPage() {
  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50 dark:bg-black">
      <AuthForm mode="login" />
    </div>
  );
}
