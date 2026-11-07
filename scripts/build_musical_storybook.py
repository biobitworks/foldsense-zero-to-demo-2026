from pathlib import Path
root=Path('/mnt/data/foldsense_review')
s=(root/'FoldSense_Living_Storybook_REVIEW.html').read_text()
css='''
.music-panel{border:2px solid #345e7e;border-radius:16px;padding:15px;background:#edf5fa;margin:12px 0 17px}
.music-panel h3{font-size:1.16rem;margin:4px 0 5px}
.music-panel .musical-caption{font-size:.9rem;color:#294d63;margin:7px 0 10px}
.music-surface{display:flex;gap:8px;align-items:end;min-height:67px;margin:9px 0 12px;border-radius:11px;padding:7px;background:#fff}
.music-voice{flex:1;min-width:9px;background:#2584a0;border:2px solid #155574;border-radius:7px 7px 3px 3px;min-height:8px;transition:height .16s ease}
.music-voice.tension{background:#c16c21;border-color:#8d3912}
.music-voice[aria-label]{position:relative}
.music-meter{height:14px;border:1px solid #7d9eac;border-radius:20px;background:#dae6ee;overflow:hidden;margin:6px 0}
.music-meter>div{height:100%;background:linear-gradient(90deg,#2d8b98,#c37a1f);transition:width .16s ease}
.music-control{display:flex;flex-wrap:wrap;align-items:center;gap:8px}
.music-control>.btn{flex:1;min-width:110px}
.music-panel label{font-weight:650;font-size:.87rem}
.music-panel select{display:block;max-width:100%;min-height:46px;background:white;border:2px solid #7c9daf;border-radius:8px;padding:5px 10px;color:#17364b}
@media(prefers-reduced-motion:reduce){.music-voice,.music-meter>div{transition:none}}
'''
s=s.replace('</style>',css+'</style>',1)
markup='''
    <section class="music-panel" aria-label="Molecular music learning layer">
      <div class="page-label">Listen to the levels · original generative teaching music</div>
      <h3 id="music-title">0D: a single note</h3>
      <p id="music-description" class="musical-caption">One residue, one note. Added structure will introduce independent musical voices.</p>
      <div class="music-surface" id="music-score" role="img" aria-label="One musical voice; melodic complexity rises with chapter level"></div>
      <div class="barline"><span class="small" id="music-tension-label">Harmonic tension · no switching event</span><b id="music-tension-value">0 / 100</b></div>
      <div class="music-meter" role="meter" aria-label="Educational harmonic tension, not measured protein stability" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0" id="music-tension-meter"><div id="music-tension-fill" style="width:0%"></div></div>
      <p class="small muted" id="music-note-caption">Score: C4 · 261.63 Hz. Musical tension is an illustrative encoding, not a protein stability or folding score.</p>
      <div class="music-control"><button class="btn accent" id="play-music">▶ Play this level</button><button class="btn alt" id="stop-music">■ Stop sound</button></div>
      <details><summary>Choose musical instrument and playback</summary>
        <div class="two" style="margin:8px 0"><label for="instrument">Instrument / timbre<select id="instrument"><option value="bell">Soft bell</option><option value="strings">Warm strings</option><option value="pulse">Soft electronic pulse</option></select></label><label for="music-tempo">Pace<select id="music-tempo"><option value="slow">Slow and clear</option><option value="medium">Moderate</option></select></label></div>
        <label class="toggle-row"><input type="checkbox" id="music-follow"> Follow page turns and frame steps after I enable sound</label>
        <p class="small muted">Manual playback is always available. No audio starts on page load; musical output is optional and never replaces text or haptic information. Music is synthesized locally in the browser.</p>
      </details>
      <p class="status" role="status" id="music-play-status" aria-live="polite">Sound not requested. Physical hearing NOT_TESTED.</p>
    </section>
'''
s=s.replace('    <div id="distance-area"',markup+'    <div id="distance-area"',1)
# New deterministic engine, independent of existing cue one-shot (which remains for alerts).
engine=r'''
// FoldSense music v2: ORIGINAL, deterministic pedagogical motifs; never claims physical protein stability.
// 0D = one residue and pitch, 1D = sequence melody, 2D = layered motifs,
// 3D = spatial harmony, 4D = time-varying intervals driven by toy distance,
// M = multiscale/polyphonic context. These are learning lenses, not physical dimensions.
const MUSIC_BASE=261.625565; // C4 reference; user can choose synthesized timbre.
const MUSIC_CHAPTERS=[
 {name:'One note',voices:1,intervals:[0],steps:1,caption:'A single amino-acid teaching focus gets a single sustained note.'},
 {name:'Sequence becomes melody',voices:1,intervals:[0,2,4,7,5,9,7,4],steps:8,caption:'A toy sequence of eight abstract residue identities becomes eight successive notes; not actual ubiquitin BILN.'},
 {name:'Local patterns become two voices',voices:2,intervals:[0,4,7,2,5,9],steps:6,caption:'A helix or sheet adds a counter-melody. These are conceptual motifs, not experimentally inferred interactions.'},
 {name:'Tertiary interactions become harmony',voices:3,intervals:[0,4,7,12,9,5],steps:6,caption:'Spatial context adds a third harmonic voice; consonance is a musical metaphor, not a stability measurement.'},
 {name:'Conformational switching changes the harmony',voices:4,intervals:[0,4,7,11,12,7],steps:6,caption:'Toy frame distance and threshold crossing modulate chord tension in real time.'},
 {name:'Multiscale ensemble',voices:5,intervals:[0,4,7,12,16,9,5],steps:7,caption:'Multiple independent musical lines describe a conceptual multi-chain ensemble. Not observed ubiquitin quaternary structure.'}
];
const MUSIC_INSTRUMENT={bell:'sine',strings:'triangle',pulse:'square'};
function clampMusic(n,min,max){return Math.min(max,Math.max(min,n))}
function midiFrequency(semitones){return Number((MUSIC_BASE*Math.pow(2,semitones/12)).toFixed(3))}
function musicPlan(chapter,frame=0){
 const level=clampMusic(Math.trunc(chapter),0,5),meta=MUSIC_CHAPTERS[level];
 const current=distance(frame),prev=distance(Math.max(0,frame-1));
 const is4d=level===4,below=current<5,switched=is4d&&frame>0&&((prev<5)!==(current<5));
 const velocity=frame>0?Math.abs(current-prev):0;
 // A visible, reversible ARTISTIC mapping of numerical inputs, not energy/thermodynamics:
 const tension=is4d?clampMusic(Math.round((below?52:12)+Math.min(20,velocity*20)+(switched?25:0)),0,100):[0,8,14,18,0,23][level];
 const chord=level===0?[0]:level===1?[0]:level===2?[0,7]:level===3?[0,4,7]:level===4?(below?[0,1,6,10]:[0,4,7,12]):[0,4,7,12,16];
 const ordered=meta.intervals.map((interval,i)=>level===1?interval:level===4?chord[i%chord.length]+(i>=chord.length?12:0):interval);
 return {level,frame,voices:meta.voices,steps:meta.steps,intervals:ordered,chord,
    frequencies:ordered.map(midiFrequency),tension,switched,distance:Number(current.toFixed(3)),
    musicalClassification:level===4?(below?'Dissonant tension motif':'Consonant/open motif'):'Illustrative increasing polyphony',
    source:'SYNTHETIC_DEMO_FIXTURE',isScientificStabilityScore:false};
}
let MUSIC_CTX=null;let MUSIC_VOICES=[];let MUSIC_GENERATION=0;
function stopMusic(){MUSIC_GENERATION++;for(const item of MUSIC_VOICES){try{item.stop()}catch{}}MUSIC_VOICES=[];
 if($('music-play-status'))$('music-play-status').textContent='Sound stopped or not playing. Human hearing NOT_TESTED.'}
function noteOn(context,frequency,start,duration,level,amp,timbre){
 const osc=context.createOscillator(),gain=context.createGain();
 osc.type=MUSIC_INSTRUMENT[timbre]||'sine';osc.frequency.setValueAtTime(frequency,start);
 gain.gain.setValueAtTime(0,start);gain.gain.linearRampToValueAtTime(amp,start+.016);
 gain.gain.setValueAtTime(amp*.76,Math.max(start+.02,start+duration*.57));
 gain.gain.linearRampToValueAtTime(.00001,start+duration);
 osc.connect(gain).connect(context.destination);osc.start(start);osc.stop(start+duration+.015);
 MUSIC_VOICES.push(osc);osc.addEventListener('ended',()=>{const i=MUSIC_VOICES.indexOf(osc);if(i>=0)MUSIC_VOICES.splice(i,1)});
}
async function playMusic(reason='USER_PREVIEW'){
 // Audio is OPTIONAL for every profile: sensory presets must not prohibit an explicitly requested channel.
 if(!($('sound').checked)){
  $('music-play-status').textContent='Turn on Request musical sound cues in Customize sound before playback.';return false;
 }
 try{
  const Audio=window.AudioContext||window.webkitAudioContext;if(!Audio)throw Error('WEB_AUDIO_NOT_SUPPORTED');
  if(!MUSIC_CTX)MUSIC_CTX=new Audio();await MUSIC_CTX.resume();stopMusic();
  const plan=musicPlan(state.ch,state.fi),now=MUSIC_CTX.currentTime+.04,
       pace=$('music-tempo').value==='medium'?.145:.245,instrument=$('instrument').value,
       amplitude=.075/Math.max(1,Math.sqrt(plan.voices));
  // Single notes gradually layer into a polyphonic chord. Hard upper bound on oscillator count.
  if(plan.level===0){noteOn(MUSIC_CTX,plan.frequencies[0],now,.49,plan.level,amplitude,instrument)}
  else if(plan.level===1){plan.frequencies.slice(0,8).forEach((f,i)=>noteOn(MUSIC_CTX,f,now+i*pace,pace*.78,plan.level,amplitude,instrument))}
  else{
   const notes=plan.chord.slice(0,Math.min(5,plan.voices));
   for(const [i,semitone] of notes.entries())noteOn(MUSIC_CTX,midiFrequency(semitone),now+(i*.055),pace*3.3,plan.level,amplitude,instrument);
   if(plan.level>=4)noteOn(MUSIC_CTX,midiFrequency(plan.intervals[plan.intervals.length-1]),now+pace*.72,pace*.67,plan.level,amplitude*.55,instrument);
  }
  $('music-play-status').textContent=`${plan.voices} voice(s) ${instrument} synthesis requested · ${plan.musicalClassification}. Physical hearing NOT_TESTED.`;
  eventRecord('MUSICAL_PREVIEW',{reason,level:plan.level,frame:plan.frame,voices:plan.voices,intervals:plan.intervals,tension:plan.tension,
    source:'SYNTHETIC_NOT_MD',actual_sound_heard:'NOT_TESTED',instrument,pace});return true;
 }catch(e){$('music-play-status').textContent='Playback unavailable: '+(e?.message||'AUDIO_FAILED');eventRecord('MUSIC_FAILED',{reason:String(e?.message||'ERROR')});return false}
}
function renderMusic(){
 const plan=musicPlan(state.ch,state.fi),meta=MUSIC_CHAPTERS[state.ch];
 $('music-title').textContent=`${chapters[state.ch].level}: ${meta.name} · ${plan.voices} ${plan.voices===1?'voice':'voices'}`;
 $('music-description').textContent=meta.caption;
 $('music-tension-label').textContent=state.ch===4?'Illustrative harmonic tension · switching-sensitive':'Illustrative harmonic tension · conceptual mapping';
 $('music-tension-value').textContent=plan.tension+' / 100';
 $('music-tension-meter').setAttribute('aria-valuenow',String(plan.tension));$('music-tension-fill').style.width=plan.tension+'%';
 $('music-score').innerHTML=Array.from({length:plan.voices},(_,i)=>`<div class="music-voice ${plan.tension>=50?'tension':''}" style="height:${(19+(i*13)+(plan.tension*.18)).toFixed(1)}px" aria-label="voice ${i+1}"></div>`).join('');
 $('music-score').setAttribute('aria-label',`${plan.voices} voice(s), artistic harmonic tension ${plan.tension} of 100, not a protein stability score`);
 $('music-note-caption').textContent=`Score: ${plan.intervals.join(', ')} semitone intervals from C4 · ${plan.musicalClassification}. ${state.ch===4?'Demo A–B distance: '+plan.distance+' toy units. ':''}Consonance/dissonance is designed, not measured folding energy.`;
}
function maybeFollowMusic(){if($('music-follow').checked&&$('sound').checked)void playMusic('USER_ARMED_FOLLOW')}
window.__FoldSenseMusicReview={musicPlan,MUSIC_CHAPTERS}; // Test-friendly pure functions, not external model APIs.
'''
s=s.replace('function render(){',engine+'\nfunction render(){',1)
s=s.replace('svg();if(state.ch===4)updateDistance();document.getElementById', 'svg();renderMusic();if(state.ch===4)updateDistance();document.getElementById',1)
s=s.replace('render();cue(\'PAGE\')}',"render();cue('PAGE');maybeFollowMusic()}",1)
s=s.replace('updateDistance();svg();if(entered||exited)', 'updateDistance();svg();renderMusic();maybeFollowMusic();if(entered||exited)',1)
s=s.replace("$('restart-time').addEventListener('click',()=>{state.fi=0;updateDistance();svg();eventRecord('RESET_MOTION')});","$('restart-time').addEventListener('click',()=>{state.fi=0;updateDistance();svg();renderMusic();eventRecord('RESET_MOTION')});",1)
s=s.replace("$('start').addEventListener('click',()=>{state.ch=0;", "$('start').addEventListener('click',()=>{state.ch=0;",1)
s=s.replace("$('change').addEventListener('click',()=>{$('reader')", "$('change').addEventListener('click',()=>{stopMusic();$('reader')",1)
s=s.replace("$('try-vibration').addEventListener('click',()=>cue('TEST'));","$('try-vibration').addEventListener('click',()=>cue('TEST'));$('play-music').addEventListener('click',()=>{if(!$('sound').checked)$('sound').checked=true;void playMusic()});$('stop-music').addEventListener('click',stopMusic);$('music-follow').addEventListener('change',e=>{if(e.target.checked)$('sound').checked=true;$('music-play-status').textContent=e.target.checked?'Sound will follow your future page/frame gestures after opt-in.':'Automatic follow off; manual previews remain available.'});",1)
s=s.replace("model_execution:'NOT_EXECUTED',watch_connection", "model_execution:'NOT_EXECUTED',musical_map:'foldsense.music.review.v2',last_music_plan:musicPlan(state.ch,state.fi),instrument:$('instrument').value,musical_context:'CREATIVE_SONIFICATION_NOT_BIOPHYSICAL_STABILITY',watch_connection",1)
s=s.replace("      const", "      const",1)
# Preserve user autonomy: optional music/narration remains available by explicit choice in every profile.
s=s.replace("if($('sound').checked&&state.profile!=='hearing'&&state.profile!=='combined')", "if($('sound').checked&&!$('music-follow').checked)")
s=s.replace("if(state.profile==='hearing'||state.profile==='combined'){$('cue-status').textContent='This profile does not require sound. Narration is optional: change preference to All or Less vision.';return}", "")
out=root/'FoldSense_Living_MUSICAL_Storybook_REVIEW_v2.html'
out.write_text(s)
print(out, 'bytes',out.stat().st_size)