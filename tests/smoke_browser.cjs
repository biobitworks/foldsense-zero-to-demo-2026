const puppeteer=require(process.env.PUPPETEER_MODULE || 'puppeteer');
const path=require('path'),fs=require('fs'),crypto=require('crypto');(async()=>{
const root=path.resolve(__dirname,'..'),testfile=path.join(root,'storybook.html');
const browser=await puppeteer.launch({headless:true,executablePath:process.env.CHROME_BIN || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',args:['--no-sandbox']});
const runs=[];let passed=0,failed=0;
for(const preset of ['all','vision','hearing','combined'])for(const route of ['sequence','shape','motion']){
const page=await browser.newPage();await page.setViewport({width:384,height:688});
try{
await page.goto('file://'+testfile,{waitUntil:'load'});
await page.evaluate(({preset,route})=>{let p=['all','vision','hearing','combined'].indexOf(preset),r=['sequence','shape','motion'].indexOf(route);
document.querySelectorAll('#access-options button')[p].click();document.querySelectorAll('#path-options button')[r].click()},{preset,route});
await page.click('#start');let voices=[],levels=[];
for(let i=0;i<6;i++){const obj=await page.evaluate(()=>({level:document.getElementById('music-title').textContent, voices:document.querySelectorAll('#music-score .music-voice').length,scroll:document.documentElement.scrollWidth,inner:innerWidth}));levels.push(obj.level.slice(0,2));voices.push(obj.voices);if(obj.scroll>obj.inner)throw Error('OVERFLOW');if(i<5)await page.click('#next')}
if(voices.join(',')!=='1,1,2,3,4,5')throw Error('VOICE_SEQUENCE:'+voices);
await page.click('#back');
for(let i=0;i<5;i++)await page.click('#step');
const after=await page.evaluate(()=>({dist:document.getElementById('distance').textContent,tension:document.getElementById('music-tension-value').textContent,switched:window.__FoldSenseMusicReview.musicPlan(4,5).switched}));
if(after.dist!=='4.630'||after.tension!=='89 / 100'||!after.switched)throw Error('CROSSING:'+JSON.stringify(after));
passed++;runs.push({preset,route,status:'PASS',voices,after});
}catch(err){failed++;runs.push({preset,route,status:'FAIL',failure:err.message});}finally{await page.close()}}
await browser.close();
const report={schema:'foldsense.public_submission.browser_smoke.v1',html_sha256:crypto.createHash('sha256').update(fs.readFileSync(testfile)).digest('hex'),actual_device:'HEADLESS_CHROMIUM_MACOS_NOT_S26',screen:'384x688 CSS px',cases:runs,summary:{passed,failed,physical_sound:'NOT_TESTED',watch:'NOT_CONNECTED'},signed:'NOT_SIGNED',mmr:'NOT_COMMITTED'};
fs.writeFileSync(path.join(root,'evidence/PUBLIC_SUBMISSION_BROWSER_SMOKE.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({passed,failed,html_sha256:report.html_sha256,failedCases:runs.filter(x=>x.status==='FAIL')}));
if(failed)process.exit(1);
})().catch(x=>{console.error(x);process.exit(2)});