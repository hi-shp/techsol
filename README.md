# techsol
다운받아서 압축 풀고 그대로 파일 구조 유지하시면 됩니다.  

.env 코드에서  
-> mathpix id, pw 입력  
-> chatgpt api key 입력 (현재 버전에서 필요하진 않음)  

requirements.txt 따라서  
-> 필요한 라이브러리 설치  

mathpix는 셀레니움으로 열어서 요소 찾는 거라 따로 설정 필요없고,   
chatgpt는 미리 창을 띄워놓고(크롬 기준 맨 오른쪽, 마지막에 오도록) alt tab으로 넘어가게 한 거라서  
화면비율에 따라 절대값 좌표 조정 필요합니다. 괄호 치고 무슨 버튼인지 적어 놓았어요.(input, 요청, 복사)  

메인 함수 실행하면  
크롬으로 새 창 열리고 -> 이미지 업로드 하면 -> mathpix로 텍스트 추출 -> 챗지피티 요청 후 응답 복사 -> 새 창 열어서 결과 띄움  
순서대로 진행합니다.  

이후 database.py 통해서 추출된 텍스트, 이미지 경로, GPT 응답을 데이터베이스에 저장.  
data.db에서 확인 가능합니다.  

끝
