// Small helper for the reviews table. Reads DATABASE_URL from .env.local.
//   node scripts/db/run.mjs schema          create the table
//   node scripts/db/run.mjs pending         list reviews waiting for approval
//   node scripts/db/run.mjs approve <id>…   show reviews
//   node scripts/db/run.mjs reject <id>…    hide reviews
import { readFileSync, existsSync } from "node:fs";
import { neon } from "@neondatabase/serverless";

if (!process.env.DATABASE_URL && existsSync(".env.local")) {
  for (const line of readFileSync(".env.local", "utf8").split("\n")) {
    const m = line.match(/^([A-Z_]+)=(.*)$/);
    if (m && !(m[1] in process.env)) process.env[m[1]] = m[2].replace(/^["']|["']$/g, "");
  }
}
const sql = neon(process.env.DATABASE_URL);
const [cmd, ...ids] = process.argv.slice(2);

if (cmd === "schema") {
  const text = readFileSync(new URL("./schema.sql", import.meta.url), "utf8");
  for (const stmt of text.split(";").map((s) => s.replace(/--.*$/gm, "").trim()).filter(Boolean)) await sql.query(stmt);
  console.log("schema applied");
} else if (cmd === "pending") {
  const rows = await sql`select id, tool, stars, name, created_at from reviews where status = 'pending' order by id`;
  console.table(rows);
} else if (cmd === "approve" || cmd === "reject") {
  const status = cmd === "approve" ? "approved" : "rejected";
  const rows = await sql`update reviews set status = ${status} where id = any(${ids.map(Number)}) returning id`;
  console.log(`${status}:`, rows.map((r) => r.id).join(", ") || "none");
} else {
  console.log("usage: node scripts/db/run.mjs schema | pending | approve <id>… | reject <id>…");
  process.exit(1);
}
