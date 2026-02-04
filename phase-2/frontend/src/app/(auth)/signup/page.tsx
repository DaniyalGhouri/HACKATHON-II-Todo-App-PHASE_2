import { AuthForm } from "@/components/auth-form";

export default function SignupPage() {
  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50 dark:bg-black">
      <AuthForm mode="signup" />
    </div>
  );
}
