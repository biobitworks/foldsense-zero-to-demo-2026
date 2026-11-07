from pathlib import Path
import json,hashlib
from playwright.sync_api import sync_playwright
p=Path(__file__).with_name('FoldSense_Living_MUSICAL_Storybook_REVIEW_v2.html')
report={'schema':'foldsense.music.prototype.browser.test.v1','artifact_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'environment':'local Chromium Playwright; NOT phone/human audio','tests':[],'failures':[]}
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
 for access in ['all','vision','hearing','combined']:
  for path in ['sequence','shape','motion']:
   page=b.new_page(viewport={'width':384,'height':688},device_scale_factor=1)
   errors=[]
   page.on('pageerror',lambda exc:errors.append(str(exc)))
   page.set_content(p.read_text(),wait_until='load')
   page.locator('#access-options button').nth(['all','vision','hearing','combined'].index(access)).click()
   page.locator('#path-options button').nth(['sequence','shape','motion'].index(path)).click()
   page.locator('#start').click()
   assert page.locator('#reader-title').inner_text()=='Meet one building block'
   pure=page.evaluate('''() => {let a=window.__FoldSenseMusicReview;return [0,1,2,3,4,5].map(n=>a.musicPlan(n,0))}''')
   assert [x['voices'] for x in pure]==[1,1,2,3,4,5],pure
   assert pure[0]['frequencies']==[261.626]
   assert len(pure[1]['frequencies'])==8 and len(set(pure[1]['frequencies']))>=4
   for i in range(6):
    assert int(page.locator('#music-score').locator('.music-voice').count())==pure[i]['voices']
    assert page.locator('#music-title').inner_text().startswith(['0D','1D','2D','3D','4D','M'][i])
    if i<5:page.locator('#next').click()
   # 4D test needs to occur earlier: navigate back to 4D
   page.locator('#back').click()
   assert page.locator('#music-title').inner_text().startswith('4D')
   start_plan=page.evaluate('window.__FoldSenseMusicReview.musicPlan(4,0)')
   for _ in range(5): page.locator('#step').click()
   switched=page.evaluate('window.__FoldSenseMusicReview.musicPlan(4,5)')
   assert switched['distance']==4.63
   assert switched['switched'] is True
   assert switched['tension']>start_plan['tension']
   assert switched['chord'] != start_plan['chord']
   assert page.locator('#music-tension-value').inner_text() == str(switched['tension'])+' / 100'
   page.locator('#play-music').click()
   page.wait_for_timeout(150)
   status=page.locator('#music-play-status').inner_text()
   assert 'not_tested' in status.lower() or 'does not require audio' in status.lower(),(access,path,status)
   assert 'synthesis requested' in status.lower(),status
   page.locator('#stop-music').click()
   assert 'Sound stopped' in page.locator('#music-play-status').inner_text()
   page.locator('#restart-time').click()
   assert page.locator('#distance').inner_text() in ('8.019','8.020')
   layout=page.evaluate('({scrollWidth:document.documentElement.scrollWidth,innerWidth,innerHeight,next:(()=>{let r=document.querySelector("#next").getBoundingClientRect();return {top:r.top,bottom:r.bottom}})()})')
   assert layout['scrollWidth']<=layout['innerWidth'],layout
   assert layout['next']['top']>=0 and layout['next']['bottom']<=688,layout
   assert errors==[],errors
   report['tests'].append({'access':access,'path':path,'status':'PASS','levels':[x['voices'] for x in pure],'start_tension':start_plan['tension'],'switch_tension':switched['tension'],'headless_audio_request_status':status,'physical_audio':'NOT_TESTED','layout':layout})
   if access=='vision' and path=='shape':
    page.screenshot(path=str(p.with_name('musical_storybook_4D_mobile.png')),full_page=True)
   page.close()
 # one desktop screenshot of 0D score
 page=b.new_page(viewport={'width':1190,'height':850})
 page.set_content(p.read_text(),wait_until='load')
 page.locator('#start').click()
 page.screenshot(path=str(p.with_name('musical_storybook_0D_desktop.png')),full_page=True)
 page.close()
 b.close()
report['summary']={'passed':len(report['tests']),'failed':len(report['failures']),'physical_s26_audio':'NOT_TESTED','actual_watch':'NOT_CONNECTED','lovable_production':'NOT_DEPLOYED','modelling':'PURE_SYNTHETIC_MUSICAL_METAPHOR'}
out=p.with_name('MUSICAL_STORYBOOK_LOCAL_TEST_RECEIPT.json')
out.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
print(json.dumps({'artifact':str(p),'html_sha256':report['artifact_sha256'],'test_receipt':str(out),'receipt_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'summary':report['summary']},indent=2))