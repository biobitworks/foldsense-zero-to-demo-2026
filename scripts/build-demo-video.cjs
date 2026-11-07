#!/usr/bin/env node
// FoldSense public-safe audiovisual walkthrough from the actual offline review prototype.
// No external APIs, model inference, user media, or physical Samsung/Watch capture.
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const puppeteer=require(process.env.PUPPETEER_MODULE || 'puppeteer');
const root=path.resolve(__dirname,'..'), out=path.join(root,'video'),frameDir=path.join(out,'frames');
fs.mkdirSync(frameDir,{recursive:true});
const notes=[["INTRO",[261.626]],["0D",[261.626]],["1D",[261.626]],["2D",[261.626,391.995]],["3D",[261.626,329.628,391.995]],["4D_PRE",[261.626,329.628,391.995,523.251]],["4D_CROSS",[261.626,277.183,369.994,466.164]],["M",[261.626,293.665,329.628,391.995,493.883]],["OUTRO",[261.626,329.628,391.995]]];
function digest(b){return crypto.createHash('sha256').update(b).digest('hex')}
function wav(){
const sr=44100,dur=notes.length*4,samples=sr*dur,buf=Buffer.alloc(44+samples*2);
buf.write("RIFF",0);buf.writeUInt32LE(36+samples*2,4);buf.write("WAVEfmt ",8);
buf.writeUInt32LE(16,16);buf.writeUInt16LE(1,20);buf.writeUInt16LE(1,22);
buf.writeUInt32LE(sr,24);buf.writeUInt32LE(sr*2,28);buf.writeUInt16LE(2,32);
buf.writeUInt16LE(16,34);buf.write("data",36);buf.writeUInt32LE(samples*2,40);
for(let i=0;i<samples;i++){const segment=Math.min(notes.length-1,Math.floor(i/(4*sr)));
let t=i/sr,local=t-segment*4, freq=notes[segment][1],signal=0;
if(segment===2){ // one-note sequence, eight notes
 const seq=[0,2,4,7,5,9,7,4];const j=Math.min(7,Math.floor(local*2));
 const hz=261.626*Math.pow(2,seq[j]/12);
 const envelope=Math.min(1,((local*2)%1)*8)*Math.min(1,(1-((local*2)%1))*5);
 signal=Math.sin(2*Math.PI*hz*t)*envelope;
}else{
 for(const hz of freq){const h=Math.sin(2*Math.PI*hz*t)+0.12*Math.sin(2*Math.PI*hz*2*t);
 signal+=h/freq.length}
}
const fade=Math.min(1,local/0.16,(4-local)/0.21);
const amp=0.19*Math.max(0,fade);buf.writeInt16LE(Math.max(-32767,Math.min(32767,Math.round(signal*amp*32767))),44+2*i)}
return buf}
function escapeHTML(s){return String(s).replace(/[&<>"']/g,ch=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[ch]))}
(async()=>{
 const browser=await puppeteer.launch({headless:true,executablePath:process.env.CHROME_BIN || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',args:['--no-sandbox','--disable-web-security']});
 const page=await browser.newPage();await page.setViewport({width:1280,height:720,deviceScaleFactor:1});
 await page.goto('file://'+path.join(root,'storybook.html'),{waitUntil:'load'});
 const records=[];
 async function frame(name,heading,subtext,kind='chapter'){
   const state=await page.evaluate(()=>({
      level:document.getElementById('music-title').textContent,
      title:document.getElementById('reader-title').textContent,
      story:document.getElementById('story').textContent,
      description:document.getElementById('music-description').textContent,
      score:document.getElementById('music-score').innerHTML,
      artwork:document.querySelector('.art').outerHTML,
      tension:document.getElementById('music-tension-value').textContent,
      note:document.getElementById('music-note-caption').textContent,
      distance:document.getElementById('distance-area').classList.contains('hidden')?null:document.getElementById('distance').textContent,
      currentChapter:document.getElementById('page-label').textContent
   }));
   await page.evaluate(({state,heading,subtext,kind})=>{
      const old=document.getElementById('video-stage');if(old)old.remove();
      const d=document.createElement('section');d.id='video-stage';
      d.style.cssText='position:fixed;inset:0;z-index:999999;background:linear-gradient(145deg,#062734,#123b50 53%,#153242);color:#f7f4ed;padding:38px 50px;box-sizing:border-box;font:16px system-ui, sans-serif;overflow:hidden';
      const title=document.createElement('div');title.textContent='FoldSense  ·  The Living Protein Storybook';
      title.style.cssText='color:#f5cb83;font:700 20px system-ui;letter-spacing:.04em;margin-bottom:18px';
      d.appendChild(title);
      const h=document.createElement('h1');h.textContent=heading;h.style.cssText='font:700 46px Georgia,serif;line-height:1.07;margin:0 0 10px';d.appendChild(h);
      const s=document.createElement('p');s.textContent=subtext;s.style.cssText='font:19px system-ui;color:#d8e9ea;max-width:1130px;margin:0 0 22px';d.appendChild(s);
      if(kind==='chapter'){
        const cols=document.createElement('div');cols.style.cssText='display:grid;grid-template-columns:1fr 1fr;gap:25px;height:446px';
        const left=document.createElement('div');left.style.cssText='border:1px solid #628b94;background:#e5f3f5;border-radius:17px;padding:14px;overflow:hidden;color:#163341';
        const ah=document.createElement('h2');ah.textContent=state.title;ah.style.cssText='font:700 25px Georgia,serif;margin:0 0 7px';left.appendChild(ah);
        const pic=document.createElement('div');pic.innerHTML=state.artwork;pic.style.cssText='height:305px;overflow:hidden';left.appendChild(pic);pic.querySelector('.art').style.cssText='height:294px;min-height:0;margin:0';
        const story=document.createElement('div');story.textContent=state.story;story.style.cssText='font:13px system-ui;max-height:55px;overflow:hidden;margin-top:5px';left.appendChild(story);
        const right=document.createElement('div');right.style.cssText='background:#fff8ed;border-radius:17px;padding:16px 21px;color:#203a48;overflow:hidden';
        const mh=document.createElement('h2');mh.textContent=state.level;mh.style.cssText='font:700 25px Georgia,serif;margin:0 0 12px';right.appendChild(mh);
        const cap=document.createElement('p');cap.textContent=state.description;cap.style.cssText='font:15px system-ui;margin:0 0 12px';right.appendChild(cap);
        const score=document.createElement('div');score.className='music-surface';score.innerHTML=state.score;score.style.cssText='min-height:100px;border-radius:10px;max-height:150px;overflow:hidden';right.appendChild(score);
        const tension=document.createElement('div');tension.textContent='Illustrative harmonic tension: '+state.tension;tension.style.cssText='font:700 18px system-ui;margin:18px 0 7px';right.appendChild(tension);
        const note=document.createElement('p');note.textContent=state.note;note.style.cssText='font:13px system-ui;color:#40515a';right.appendChild(note);
        if(state.distance!==null){const dist=document.createElement('p');dist.textContent='Toy distance: '+state.distance+' demo units · threshold 5.0';dist.style.cssText='font:700 18px system-ui;color:#a85a10';right.appendChild(dist)}
        cols.append(left,right);d.appendChild(cols);
      }else{
        const extra=document.createElement('div');extra.style.cssText='padding:28px;border-radius:18px;background:#ffffff16;border:1px solid #89b0ae;margin-top:55px;font:600 26px system-ui;line-height:1.7';
        extra.textContent=kind==='intro'?'Choose your learning path → turn six pages → see, hear, and explore conformational relationships':'Try the storybook on the web. Review the open source and evidence before making claims.';
        d.appendChild(extra)
      }
      const bottom=document.createElement('footer');bottom.textContent='SCREEN-CAPTURE-DERIVED LOCAL DEMO   ·   SYNTHETIC EDUCATIONAL FIXTURE   ·   NOT REAL MOLECULAR DYNAMICS   ·   NOT SAMSUNG/WATCH VIDEO';
      bottom.style.cssText='position:absolute;left:50px;right:50px;bottom:25px;color:#b7d1cf;font:700 11px system-ui;letter-spacing:.055em';d.appendChild(bottom);
      document.body.appendChild(d);
   },{state,heading,subtext,kind});
   const file=path.join(frameDir,name+'.png');await page.screenshot({path:file});
   records.push({name,sha256:digest(fs.readFileSync(file)),chapter:state.currentChapter,uiTitle:state.title,score:state.level,tension:state.tension,distance:state.distance,clip_type:kind});
   await page.evaluate(()=>document.getElementById('video-stage')?.remove());
 }
 await page.click('#path-options button:nth-child(3)');
 await page.click('#start');
 await frame('00-intro','See · Hear · Feel · Learn','A protein story for different sensory preferences.','intro');
 const headings=[
 ['01-0d','0D · One amino acid, one note','Begin with one chemical building block — and one sustained musical voice.'],
 ['02-1d','1D · Sequence becomes melody','The order of amino acids introduces a recognizable musical phrase.'],
 ['03-2d','2D · Local patterns become counterpoint','Helices and sheets are introduced schematically as interacting voices.'],
 ['04-3d','3D · Structure becomes harmony','Tertiary context introduces harmonic relationships among three voices.'],
 ['05-4d-open','4D · Motion before the crossing','Four voices encode the open state of a synthetic contact threshold.'],
 ['06-4d-cross','4D · The chord changes','A toy A–B distance crosses 5.0 demo units; consonance shifts to artistic dissonance.'],
 ['07-m','M · Multiscale musical ensemble','Five voices combine sequence, shape, movement and optional sensory channels.']
 ];
 for(let i=0;i<5;i++){await frame(...headings[i]);if(i<4)await page.click('#next')}
 for(let n=0;n<5;n++)await page.click('#step');
 await frame(...headings[5]);
 await page.click('#next');
 await frame(...headings[6]);
 await frame('08-outro','Explore the story yourself','Published FoldSense Touch Lab · Public GitHub source · inspectable synthetic-science limitations.','outro');
 await browser.close();
 fs.writeFileSync(path.join(out,'demo-score.wav'),wav());
 const concat=records.map(x=>"file 'frames/"+x.name+".png'\nduration 4\n").join('')+"file 'frames/"+records.at(-1).name+".png'\n";
 fs.writeFileSync(path.join(out,'concat.txt'),concat);
 fs.writeFileSync(path.join(out,'capture-manifest.json'),JSON.stringify({schema:'foldsense.demo.video.capture.v1',source_file_sha256:digest(fs.readFileSync(path.join(root,'storybook.html'))),method:'actual browser DOM rendered via Puppeteer and edited into frame compositions; generated original score',device:'macOS Chrome headless, not Samsung',screens:records,audio_sha256:digest(fs.readFileSync(path.join(out,'demo-score.wav'))),physical_user_test:'NOT_TESTED',signature:'NOT_SIGNED',merkle_mmr:'NOT_COMMITTED'},null,2)+'\n');
 console.log(JSON.stringify({frames:records.map(x=>x.name),audio_sha256:digest(fs.readFileSync(path.join(out,'demo-score.wav'))),manifest:path.join(out,'capture-manifest.json')}));
})().catch(err=>{console.error("VIDEO_CAPTURE_FAILED",err?.stack||err);process.exit(1)});
