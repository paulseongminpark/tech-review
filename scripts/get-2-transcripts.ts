import { Innertube } from "npm:youtubei.js";
import { readdir, readTextFile, writeTextFile } from "node:fs/promises";

const BLOG_DIR = new URL("../", import.meta.url).pathname.replace(/^\/([A-Z]:)/, "$1");
const DATA_DIR = `${BLOG_DIR}_data/sources/`;

const MISSING = ["kvZKl7eLSX8", "A8PMyC7W_vg"];

const yt = await Innertube.create();
console.log("[YouTube.js] 준비 완료\n");

for (const vid of MISSING) {
  console.log(`[${vid}]`);
  try {
    const info = await yt.getInfo(vid);
    const transcriptInfo = await info.getTranscript();
    const segments = (transcriptInfo as any)?.transcript?.content?.body?.initial_segments;
    if (segments && segments.length > 0) {
      const lines: string[] = [];
      for (const seg of segments) {
        const text = (seg as any)?.snippet?.text?.toString()?.trim();
        if (text) lines.push(text);
      }
      const result = lines.join(" ").trim();
      if (result.length > 100) {
        console.log(`  YouTube.js OK (${result.length}자)`);

        // JSON 파일 찾아서 업데이트
        const entries = [...Deno.readDirSync(DATA_DIR)].filter(e => e.name.startsWith("youtube-") && e.name.endsWith(".json"));
        for (const entry of entries) {
          const filepath = `${DATA_DIR}${entry.name}`;
          const raw = Deno.readTextFileSync(filepath);
          let data = JSON.parse(raw);
          if (!Array.isArray(data)) data = [data];
          let changed = false;
          for (const v of data) {
            if (v.video_id === vid) {
              v.transcript = result.slice(0, 100000);
              changed = true;
            }
          }
          if (changed) {
            Deno.writeTextFileSync(filepath, JSON.stringify(data, null, 2));
            console.log(`  → ${entry.name} 업데이트`);
          }
        }
        continue;
      }
    }
    console.log("  자막 없음 → Gemini 필요");
  } catch (e) {
    console.log(`  실패: ${(e as Error).message?.slice(0, 100)}`);
  }
}
