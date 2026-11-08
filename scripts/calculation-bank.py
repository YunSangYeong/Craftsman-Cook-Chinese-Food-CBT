"""10개 조리 계산 유형 × 94조건. 정수/유한소수 조건, 고정 ID. 개념형 원고와 분리."""
import json
from decimal import Decimal as D
from pathlib import Path
path=Path('src/data/questions.json')
bank=[q for q in json.loads(path.read_text()) if not q.get('family')]
assert len(bank)==60
fmt=lambda x: format(D(str(x)).normalize(),'f')
for family in range(10):
 for i in range(1,95):
  if family==0:
   a=D(i)/10;result=a*1000;unit='g';topic='질량 단위 변환';q=f'식재료 {fmt(a)} kg은 몇 g인가?';why=f'1 kg = 1,000 g이므로 {fmt(a)} × 1,000 = {fmt(result)} g이다.';values=[float(a)]
  elif family==1:
   a=D(i)/20;result=a*1000;unit='mL';topic='부피 단위 변환';q=f'육수 {fmt(a)} L는 몇 mL인가?';why=f'1 L = 1,000 mL이므로 {fmt(a)} × 1,000 = {fmt(result)} mL이다. 질량으로 바꾸는 계산이 아니다.';values=[float(a)]
  elif family==2:
   a=D(1000+i*20);b=D(80);result=a*b/100;unit='g';topic='가식부 수율';q=f'원재료 {fmt(a)} g의 가식부 수율이 {b}%일 때 가식부 무게는?';why=f'가식부 무게 = 원재료 무게 × 수율 / 100 = {fmt(a)} × {b}/100 = {fmt(result)} g이다. 손질 손실을 제외한 무게다.';values=[float(a),float(b)]
  elif family==3:
   a=D(10+i);b=D(150);result=a*b;unit='g';topic='인원별 필요량';q=f'1인분에 재료 {b} g이 필요하다. {a}인분에 필요한 재료 무게는? (손실 없음)';why=f'전체 필요량 = 1인분 필요량 × 인분 수 = {b} × {a} = {fmt(result)} g이다. 손실과 여유분은 계산하지 않는다.';values=[float(a),float(b)]
  elif family==4:
   a=D(10+i);b=D(240);base=D(4);result=b*a/base;unit='g';topic='배합 확대';q=f'{base}인분 레시피의 재료량이 {b} g이다. 같은 배합비로 {a}인분을 만들 때 이 재료는 몇 g 필요한가?';why=f'배율 = {a}/{base}. 필요량 = {b} × {a}/{base} = {fmt(result)} g이다. 가열 시간은 배수로 단순 확대하지 않는다.';values=[float(a),float(b),float(base)]
  elif family==5:
   a=D(1000+i*100);b=D(2);result=a*b/100;unit='g';topic='소금물 질량 백분율';q=f'소금과 물만으로 질량 기준 {b}% 소금물 {a} g을 만들 때 필요한 소금은?';why=f'질량 백분율 = 소금 질량/용액 전체 질량 × 100. 소금 = {a} × {b}/100 = {fmt(result)} g이다. 물은 전체 질량에서 소금을 뺀 양이다.';values=[float(a),float(b)]
  elif family==6:
   a=D(1000+i*40);b=D(15);result=a*b/100;unit='g';topic='손질 손실량';q=f'재료 {a} g을 손질할 때 원재료 대비 손실률이 {b}%이다. 손실되는 무게는?';why=f'손실량 = 원재료 무게 × 손실률/100 = {a} × {b}/100 = {fmt(result)} g이다. 남는 가식부 무게와 구별한다.';values=[float(a),float(b)]
  elif family==7:
   a=D(1000+i*100);b=D(10);result=a/b;unit='원';topic='인분당 재료비';q=f'총 식재료비 {a}원으로 동일한 {b}인분을 만든다. 1인분 재료비는? (인건비·기타 비용 제외)';why=f'인분당 재료비 = 총 재료비/인분 수 = {a}/{b} = {fmt(result)}원이다. 판매가나 전체 원가와는 다르다.';values=[float(a),float(b)]
  elif family==8:
   a=D(i+5);result=a*4;unit='kcal';topic='탄수화물 에너지';q=f'탄수화물 1 g당 에너지를 4 kcal로 계산한다. 탄수화물 {a} g의 에너지는? (다른 영양소 제외)';why=f'에너지 = 탄수화물 무게 × 주어진 계수 = {a} × 4 = {fmt(result)} kcal이다. 전체 음식의 열량을 뜻하지 않는다.';values=[float(a)]
  else:
   a=D(i+2);result=a*9;unit='kcal';topic='지방 에너지';q=f'지방 1 g당 에너지를 9 kcal로 계산한다. 지방 {a} g의 에너지는? (다른 영양소 제외)';why=f'에너지 = 지방 무게 × 주어진 계수 = {a} × 9 = {fmt(result)} kcal이다. 다른 영양소가 있으면 그 에너지도 별도로 더해야 한다.';values=[float(a)]
  options=[result,result+D(1),result+D(5),result+D(10)];shift=i%4;options=options[shift:]+options[:shift]
  bank.append(dict(id=f'CC-N-{family+1:02}-{i:03}',subject='중식 재료관리, 음식조리 및 위생관리',topic=topic,question=q,choices=[f'{fmt(v)} {unit}' for v in options],answer=options.index(result)+1,explanation=why,difficulty='하',year=None,session=None,type='original',sourceUrl='https://github.com/YunSangYeong/Craftsman-Cook-Chinese-Food-CBT',verificationStatus='reviewed',reviewNote='AI 일반 조리 계산 지식으로 직접 작성. Python Decimal 생성 및 별도 TypeScript 역산 검증. 조건·단위·해설 내부 대조. 외부 전문가 검수·공식 출제기준 대조 미완료. URL은 작성 위치이며 외부 정답 증빙 아님.',version='main',rights='자체 제작 문항, CC BY 4.0; 저작자 표시: 중식조리기능사 CBT 프로젝트',family=f'CC-F-{family+1:02}',calculation=dict(kind=str(family+1),values=values,result=float(result),unit=unit)))
assert len(bank)==1000
path.write_text(json.dumps(bank,ensure_ascii=False,indent=2)+'\n')
