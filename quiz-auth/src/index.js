import bcrypt from "bcryptjs";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type"
};

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // Handle CORS preflight
    if (request.method === "OPTIONS") {
      return new Response(null, {
        headers: corsHeaders
      });
    }

    // SIGNUP
    if (url.pathname === "/signup" && request.method === "POST") {
      const { email, password } = await request.json();

      if (!email || !password) {
        return new Response("Missing fields", {
          status: 400,
          headers: corsHeaders
        });
      }

      const hash = await bcrypt.hash(password, 10);

      try {
        await env.DB.prepare(
          "INSERT INTO users (email, password_hash) VALUES (?, ?)"
        ).bind(email, hash).run();

        return new Response("User created", {
          headers: corsHeaders
        });
      } catch (err) {
        return new Response("User already exists", {
          status: 400,
          headers: corsHeaders
        });
      }
    }

    // LOGIN
    if (url.pathname === "/login" && request.method === "POST") {
      const { email, password } = await request.json();

      if (!email || !password) {
        return new Response("Missing fields", {
          status: 400,
          headers: corsHeaders
        });
      }

      const user = await env.DB.prepare(
        "SELECT * FROM users WHERE email = ?"
      ).bind(email).first();

      if (!user) {
        return new Response("Invalid login", {
          status: 401,
          headers: corsHeaders
        });
      }

      const valid = await bcrypt.compare(password, user.password_hash);

      if (!valid) {
        return new Response("Invalid login", {
          status: 401,
          headers: corsHeaders
        });
      }

      return new Response(JSON.stringify({
        success: true,
        userId: user.id
      }), {
        headers: corsHeaders
      });
    }

    return new Response("Not found", {
      status: 404,
      headers: corsHeaders
    });
  }
};