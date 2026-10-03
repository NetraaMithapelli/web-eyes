// Tiny build script: bundles the TypeScript entry points with esbuild and copies static files.
import { context, build } from "esbuild";
import { cpSync, mkdirSync, rmSync } from "node:fs";

const watch = process.argv.includes("--watch");

rmSync("dist", { recursive: true, force: true });
mkdirSync("dist", { recursive: true });

const copyStatic = () => {
  cpSync("manifest.json", "dist/manifest.json");
  cpSync("src/sidepanel/sidepanel.html", "dist/sidepanel.html");
};

const options = {
  entryPoints: {
    background: "src/background/service-worker.ts",
    content: "src/content/content-script.ts",
    sidepanel: "src/sidepanel/sidepanel.ts",
  },
  bundle: true,
  outdir: "dist",
  format: "iife",
  target: "chrome114",
  sourcemap: true,
  logLevel: "info",
};

copyStatic();
if (watch) {
  const ctx = await context(options);
  await ctx.watch();
  console.log("Watching for changes... (reload the extension in chrome://extensions after edits)");
} else {
  await build(options);
}
