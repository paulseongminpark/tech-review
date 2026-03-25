/**
 * fix-transcripts.ts — Deno + YouTube.js로 FAIL 영상 transcript 재수집
 *
 * 1차: YouTube.js (InnerTube) 자막 추출
 * 2차: Gemini API (영상 URL 직접 전달 → 텍스트 추출)
 *
 * Usage: deno run --allow-net --allow-read --allow-write scripts/fix-transcripts.ts
 */

import { Innertube } from "npm:youtubei.js";

const BLOG_DIR = new URL("../", import.meta.url).pathname.replace(/^\/([A-Z]:)/, "$1");
const DATA_DIR = `${BLOG_DIR}_data/sources/`;
const ENV_PATH = `${BLOG_DIR}.env`;

// FAIL 영상 목록
const FAIL_IDS = [
  // 자막 불일치 (03-20 집중)
  "_TZhiX4qajk", "vfn_Ezu1qfk", "L40tTQ8TpaM", "mpALXah_PBg",
  "i1GPX8CEwP4", "J1F8zH_QCt8", "2qap-FCk9zU", "X3Srdwkuor4",
  "s4_UKVvTkIA", "Y5pzLHmMobc", "0xF13rNDD0A",
  "eMngNllXbYE", "jxzpitU9YBg",
  // 미수집 (03-24)
  "IRBb6A-sIPE", "kwSVtQ7dziU", "ySPyLO4xrk8",
];

// .env에서 GEMINI_API_KEY 읽기
function loadEnv(): Record<string, string> {
  try {
    const text = Deno.readTextFileSync(ENV_PATH);
    const env: Record<string, string> = {};
    for (const line of text.split("\n")) {
      const m = line.match(/^([A-Z_]+)=(.+)$/);
      if (m) env[m[1]] = m[2].trim().replace(/^["']|["']$/g, "");
    }
    return env;
  } catch { return {}; }
}

// YouTube.js로 자막 추출
async function getTranscriptYouTubeJS(yt: Innertube, videoId: string): Promise<string | null> {
  try {
    const info = await yt.getInfo(videoId);
    const transcriptInfo = await info.getTranscript();

    if (!transcriptInfo?.transcript?.content?.body?.initial_segments) {
      return null;
    }

    const segments = transcriptInfo.transcript.content.body.initial_segments;
    const lines: string[] = [];
    for (const seg of segments) {
      const text = seg?.snippet?.text?.toString()?.trim();
      if (text) lines.push(text);
    }

    const result = lines.join(" ").trim();
    return result.length > 100 ? result.slice(0, 100000) : null;
  } catch (e) {
    console.log(`  [YouTube.js] 실패: ${(e as Error).message?.slice(0, 80)}`);
    return null;
  }
}

// Gemini API로 영상 텍스트 추출
async function getTranscriptGemini(videoId: string, apiKey: string): Promise<string | null> {
  const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${apiKey}`;

  try {
    const resp = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        contents: [{
          parts: [
            { file_data: { mime_type: "video/youtube", file_uri: `https://www.youtube.com/watch?v=${videoId}` }},
            { text: "이 YouTube 영상의 전체 발언을 빠짐없이 텍스트로 추출해라. 발화자의 모든 말을 순서대로 기록. 요약하지 말고 그대로 텍스트만 출력." }
          ]
        }]
      })
    });

    if (!resp.ok) {
      const err = await resp.text();
      console.log(`  [Gemini] HTTP ${resp.status}: ${err.slice(0, 100)}`);
      return null;
    }

    const data = await resp.json();
    const text = data?.candidates?.[0]?.content?.parts?.[0]?.text?.trim();
    return text && text.length > 100 ? text.slice(0, 100000) : null;
  } catch (e) {
    console.log(`  [Gemini] 실패: ${(e as Error).message?.slice(0, 80)}`);
    return null;
  }
}

// 데이터 파일에서 영상 찾아서 업데이트
function updateVideoInData(videoId: string, transcript: string): number {
  let updated = 0;

  for (const entry of Deno.readDirSync(DATA_DIR)) {
    if (!entry.name.startsWith("youtube-") || !entry.name.endsWith(".json")) continue;

    const filepath = `${DATA_DIR}${entry.name}`;
    const raw = Deno.readTextFileSync(filepath);
    let data = JSON.parse(raw);
    if (!Array.isArray(data)) data = [data];

    let changed = false;
    for (const v of data) {
      if (v.video_id === videoId) {
        v.transcript = transcript;
        // 잘못된 summary 제거 (Sonnet이 재생성)
        if (v.summary) delete v.summary;
        changed = true;
      }
    }

    if (changed) {
      Deno.writeTextFileSync(filepath, JSON.stringify(data, null, 2));
      updated++;
    }
  }

  return updated;
}

async function main() {
  console.log(`=== Phase 1: transcript 수집 (${FAIL_IDS.length}건) ===\n`);

  const env = loadEnv();
  const geminiKey = env.GEMINI_API_KEY || Deno.env.get("GEMINI_API_KEY") || "";

  console.log("[YouTube.js] InnerTube 초기화...");
  const yt = await Innertube.create();
  console.log("[YouTube.js] 준비 완료\n");

  let success = 0;
  let fail = 0;

  for (const vid of FAIL_IDS) {
    process.stdout?.write?.(`[${vid}] `) ?? Deno.stdout.writeSync(new TextEncoder().encode(`[${vid}] `));

    // 1차: YouTube.js
    let transcript = await getTranscriptYouTubeJS(yt, vid);
    if (transcript) {
      console.log(`YouTube.js OK (${transcript.length}자)`);
    } else {
      // 2차: Gemini API
      if (geminiKey) {
        console.log("YouTube.js 자막 없음 → Gemini...");
        transcript = await getTranscriptGemini(vid, geminiKey);
        if (transcript) {
          console.log(`  [Gemini] OK (${transcript.length}자)`);
        } else {
          console.log(`  실패 (자막 없음 + Gemini 실패)`);
          fail++;
          continue;
        }
      } else {
        console.log("자막 없음 (GEMINI_API_KEY 없어서 fallback 불가)");
        fail++;
        continue;
      }
    }

    // 데이터 파일 업데이트
    const updated = updateVideoInData(vid, transcript);
    if (updated > 0) {
      console.log(`  → ${updated}개 파일 업데이트`);
      success++;
    } else {
      console.log(`  WARNING: 데이터 파일에 ${vid} 없음`);
      fail++;
    }
  }

  console.log(`\n=== 완료: 성공 ${success}, 실패 ${fail} ===`);
}

await main();
