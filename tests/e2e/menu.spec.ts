import {test,expect} from '@playwright/test';
for (const viewport of [{width:390,height:480},{width:740,height:360}]) {
 for(const input of ['wheel','touch'] as const) {
 test(`${viewport.width}×${viewport.height} 메뉴 ${input}: 아래 도구·위 대시보드 실제 입력`,async({page,context})=>{
  await page.setViewportSize(viewport);await page.goto('');
  await page.getByRole('button',{name:'메뉴 열기'}).click();
  await page.waitForTimeout(300);
  const sidebar=page.locator('.sidebar');
  const cdp=await context.newCDPSession(page);
  const move=async(down:boolean)=>{
   if(input==='wheel'){await page.mouse.move(130,viewport.height/2);await page.mouse.wheel(0,down?850:-850);}
   else{
    const start=down?viewport.height-65:90,end=down?90:viewport.height-65;
    await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:130,y:start}]});
    for(let step=1;step<=12;step++){
     await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:130,y:start+(end-start)*step/12}]});
     await page.waitForTimeout(18);
    }
    await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});
   }
   await page.waitForTimeout(350);
  };
  for(let i=0;i<4;i++)await move(true);
  expect(await sidebar.evaluate(el=>el.scrollTop)).toBeGreaterThan(0);
  await expect(page.getByRole('button',{name:'학습 기록 백업',exact:true})).toBeInViewport();
  const downloading=page.waitForEvent('download');
  await page.getByRole('button',{name:'학습 기록 백업',exact:true}).click();
  expect((await downloading).suggestedFilename()).toBe('chinese-cook-study-backup.json');
  const reset=page.getByRole('button',{name:'데이터 초기화',exact:true});
  await expect(reset).toBeInViewport();await reset.click();
  await expect(page.getByRole('dialog')).toBeVisible();
  await page.getByRole('button',{name:'돌아가기',exact:true}).click();
  for(let i=0;i<4;i++)await move(false);
  expect(await sidebar.evaluate(el=>el.scrollTop)).toBeLessThan(2);
  const home=page.getByRole('button',{name:'학습 대시보드',exact:true});
  await expect(home).toBeInViewport();await home.click();
  await expect(page.getByRole('heading',{name:'중식조리기능사 필기 CBT',exact:true})).toBeVisible();
  await expect(sidebar).not.toHaveClass(/open/);
  await expect(page.locator('.criteria-note')).toHaveCount(0);
  await page.screenshot({path:`test-results/menu-${viewport.width}-${input}-${test.info().project.name}.png`,fullPage:true});
 });
 }
}
