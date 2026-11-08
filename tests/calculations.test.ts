import { expect, it } from 'vitest';
import { BASE_BANK, fingerprint } from '../src/model';
import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
const numeric=BASE_BANK.filter(q=>q.calculation);
it('원고 재생성: 개념 60 + 10유형×94조건 = 1000, 동일 출력',()=>{
 const before=readFileSync('src/data/questions.json','utf8');
 execFileSync('python',['scripts/author-bank.py']);
 execFileSync('python',['scripts/calculation-bank.py']);
 expect(readFileSync('src/data/questions.json','utf8')).toBe(before);
 expect(BASE_BANK).toHaveLength(1000);expect(numeric).toHaveLength(940);
 expect(new Set(BASE_BANK.map(fingerprint)).size).toBe(1000);
 const groups=new Map<string,number>();numeric.forEach(q=>groups.set(q.family!,1+(groups.get(q.family!)||0)));
 expect(groups.size).toBe(10);expect([...groups.values()].every(n=>n===94)).toBe(true);
});
for(const q of numeric) it(`${q.id}: 조건·단위·정답의 독립 역산`,()=>{
 const c=q.calculation!;const [a,b,base]=c.values;
 const correct=Number(q.choices[q.answer-1].split(' ')[0]);
 // 생성 식을 복사하지 않고 답안으로부터 원래 조건을 복원한다.
 let recovered:number;
 switch(c.kind){
 case '1':case '2': recovered=correct/1000;break;
 case '3':case '6':case '7':recovered=correct*100/b;break;
 case '4':recovered=correct/b;break;
 case '5':recovered=correct*base/b;break;
 case '8':recovered=correct*b;break;
 case '9':recovered=correct/4;break;
 case '10':recovered=correct/9;break;
 default:throw Error('알 수 없는 계산 유형');
 }
 expect(recovered).toBeCloseTo(a,8);
 expect(correct).toBeCloseTo(c.result,8);
 expect(new Set(q.choices.map(x=>Number(x.split(' ')[0]))).size).toBe(4);
 expect(q.choices.every(x=>x.endsWith(` ${c.unit}`))).toBe(true);
 expect(q.explanation).toContain(String(correct));
 expect(q.year).toBeNull();expect(q.session).toBeNull();
});
