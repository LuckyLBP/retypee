// Reviews for the tool pages. GET lists approved ratings, POST adds one (a star rating and an optional name).
// A 3+ star rating is auto-approved; 1-2 stars go to the moderation queue first.
// Nothing about the visitor is stored: no IP, no cookie, no user agent.
import { readFileSync } from "node:fs";
import { neon } from "@neondatabase/serverless";

const TOOLS = new Set(JSON.parse(readFileSync(new URL("./_tools.json", import.meta.url), "utf8")));
const sql = neon(process.env.DATABASE_URL);

const MAX_PENDING_PER_HOUR = 40;   // overall, so a flood cannot fill the moderation queue
const MIN_FILL_MS = 2500;          // a real person takes longer than this to fill in the form
const clean = (s, max) => String(s ?? "").replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f]/g, "").replace(/\s+/g, " ").trim().slice(0, max);

function send(res, status, body, cache) {
  res.setHeader("Cache-Control", cache || "no-store");
  res.status(status).json(body);
}

export default async function handler(req, res) {
  try {
    if (req.method === "GET") {
      const tool = String(req.query.tool || "");
      if (!TOOLS.has(tool)) return send(res, 400, { error: "unknown tool" });
      const [stats] = await sql`select count(*)::int as count, round(avg(stars)::numeric, 1)::float as average from reviews where tool = ${tool} and status = 'approved'`;
      const breakdown = await sql`select stars, count(*)::int as n from reviews where tool = ${tool} and status = 'approved' group by stars`;
      const counts = { 5: 0, 4: 0, 3: 0, 2: 0, 1: 0 };
      for (const b of breakdown) counts[b.stars] = b.n;
      return send(res, 200, { count: stats.count, average: stats.average, counts },
        "public, s-maxage=300, stale-while-revalidate=3600");
    }

    if (req.method === "POST") {
      const b = typeof req.body === "string" ? JSON.parse(req.body || "{}") : req.body || {};
      if (b.website) return send(res, 200, { ok: true });                       // honeypot: pretend it worked
      const tool = String(b.tool || "");
      const stars = Number(b.stars);
      const name = clean(b.name, 40) || null;
      const lang = b.lang === "en" ? "en" : "sv";
      if (!TOOLS.has(tool)) return send(res, 400, { error: "unknown tool" });
      if (!Number.isInteger(stars) || stars < 1 || stars > 5) return send(res, 400, { error: "stars" });
      if (!(Number(b.fillMs) >= MIN_FILL_MS)) return send(res, 429, { error: "too fast" });
      const [recent] = await sql`select count(*)::int as n from reviews where created_at > now() - interval '1 hour'`;
      if (recent.n >= MAX_PENDING_PER_HOUR) return send(res, 429, { error: "busy" });
      const status = stars >= 3 ? "approved" : "pending";
      await sql`insert into reviews (tool, stars, name, lang, status) values (${tool}, ${stars}, ${name}, ${lang}, ${status})`;
      return send(res, 201, { ok: true });
    }

    res.setHeader("Allow", "GET, POST");
    return send(res, 405, { error: "method" });
  } catch (err) {
    console.error("reviews:", err);
    return send(res, 500, { error: "server" });
  }
}
