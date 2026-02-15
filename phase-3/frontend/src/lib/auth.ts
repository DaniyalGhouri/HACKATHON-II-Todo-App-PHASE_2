import { betterAuth } from "better-auth";
import { Pool } from "pg";
import { jwt } from "better-auth/plugins/jwt"; // Corrected import path

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: process.env.DATABASE_URL?.includes("localhost") ? false : { rejectUnauthorized: false }, 
});

export const auth = betterAuth({
  database: pool,
  secret: process.env.BETTER_AUTH_SECRET,
  baseURL: process.env.BETTER_AUTH_URL || process.env.NEXT_PUBLIC_BETTER_AUTH_URL,
  emailAndPassword: {
    enabled: true,
  },
  plugins: [
    jwt() 
  ],
  cookies: {
    sessionToken: {
      name: "better-auth.session_token",
      options: {
        sameSite: "none",
        secure: true,
        httpOnly: true,
      },
    },
  }
});
