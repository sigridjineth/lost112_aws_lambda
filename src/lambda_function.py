from webdriver_wrapper import WebDriverWrapper
from bs4 import BeautifulSoup

lost112_link = 'https://www.lost112.go.kr/find/findList.do'

def lambda_handler(*args, **kwargs):
    global example_text
    driver = WebDriverWrapper()

    # iterate 3 times
    for i in range(3):
        driver.get_url(lost112_link)
        print("link > ", lost112_link)
        # <tbody>
        # 				<!-- 테이블 반복 구간 시작 -->
        #
        # 						  <tr>
        # 							<td scope="row" title="F2022111300000595" class="first "><a href="javascript:fn_find_detail('F2022111300000595', '1')">F2022111300000595</a></td>
        # 							<td scope="row" title="남성지갑" class="board_title1 "><div class="title_text">
        # 							<a href="javascript:fn_find_detail('F2022111300000595', '1')">남성지갑
        # 								</a></div></td>
        # 							<td style="text-overflow:ellipsis; display:inline-block; overflow: hidden; width: 100px; white-space: nowrap; padding-top:12.5px" scope="row" title="서*찬" class=""><a href="javascript:fn_find_detail('F2022111300000595', '1')">서*찬</a></td>
        #
        #
        #
        #
        # 									<td scope="row" title="솔샘지구대" class="">
        # 										<div class="losers_text">
        # 											<a href="javascript:fn_find_detail('F2022111300000595', '1')">솔샘지구대</a>
        # 										</div>
        # 									</td>
        #
        #
        # 							<td scope="row" title="02-944-4123" class="first "><a href="javascript:fn_find_detail('F2022111300000595', '1')">02-944-4123</a></td>
        # 							<td scope="row" class=""><a href="javascript:fn_find_detail('F2022111300000595', '1')">2022-11-13</a></td>
        # 						</tr>
        #
        # 						  <tr>
        # 							<td scope="row" title="F2022111300000593" class="first "><a href="javascript:fn_find_detail('F2022111300000593', '1')">F2022111300000593</a></td>
        # 							<td scope="row" title="반지갑, 신분증, 부산은행카드, 국민은행카드 등" class="board_title1 "><div class="title_text">
        # 							<a href="javascript:fn_find_detail('F2022111300000593', '1')">반지갑, 신분증, 부산은행카드, 국민은행카드 등
        # 								</a></div></td>
        # 							<td style="text-overflow:ellipsis; display:inline-block; overflow: hidden; width: 100px; white-space: nowrap; padding-top:12.5px" scope="row" title="조*협" class=""><a href="javascript:fn_find_detail('F2022111300000593', '1')">조*협</a></td>
        #
        #
        #
        #
        # 									<td scope="row" title="남포지구대" class="">
        # 										<div class="losers_text">
        # 											<a href="javascript:fn_find_detail('F2022111300000593', '1')">남포지구대</a>
        # 										</div>
        # 									</td>
        #
        #
        # 							<td scope="row" title="051-245-0835" class="first "><a href="javascript:fn_find_detail('F2022111300000593', '1')">051-245-0835</a></td>
        # 							<td scope="row" class=""><a href="javascript:fn_find_detail('F2022111300000593', '1')">2022-11-13</a></td>
        # 						</tr>
        #
        # 						  <tr>
        # 							<td scope="row" title="F2022111300000608" class="first "><a href="javascript:fn_find_detail('F2022111300000608', '1')">F2022111300000608</a></td>
        # 							<td scope="row" title="헤지스 여성 카드지갑" class="board_title1 "><div class="title_text">
        # 							<a href="javascript:fn_find_detail('F2022111300000608', '1')">헤지스 여성 카드지갑
        # 								</a></div></td>
        # 							<td style="text-overflow:ellipsis; display:inline-block; overflow: hidden; width: 100px; white-space: nowrap; padding-top:12.5px" scope="row" title="이*헌" class=""><a href="javascript:fn_find_detail('F2022111300000608', '1')">이*헌</a></td>
        #
        #
        #
        #
        # 									<td scope="row" title="노량진지구대" class="">
        # 										<div class="losers_text">
        # 											<a href="javascript:fn_find_detail('F2022111300000608', '1')">노량진지구대</a>
        # 										</div>
        # 									</td>
        #
        #
        # 							<td scope="row" title="02-815-3494" class="first "><a href="javascript:fn_find_detail('F2022111300000608', '1')">02-815-3494</a></td>
        # 							<td scope="row" class=""><a href="javascript:fn_find_detail('F2022111300000608', '1')">2022-11-13</a></td>
        # 						</tr>
        #
        # 						  <tr>
        # 							<td scope="row" title="F2022111300000591" class="first "><a href="javascript:fn_find_detail('F2022111300000591', '1')">F2022111300000591</a></td>
        # 							<td scope="row" title="삼성 갤력시 핸드폰" class="board_title1 "><div class="title_text">
        # 							<a href="javascript:fn_find_detail('F2022111300000591', '1')">삼성 갤력시 핸드폰
        # 								<img src="/images/sub/icon_jpg.gif" alt="사진있음"></a></div></td>
        # 							<td style="text-overflow:ellipsis; display:inline-block; overflow: hidden; width: 100px; white-space: nowrap; padding-top:12.5px" scope="row" title="-" class=""><a href="javascript:fn_find_detail('F2022111300000591', '1')">-</a></td>
        #
        #
        #
        #
        # 									<td scope="row" title="제기파출소" class="">
        # 										<div class="losers_text">
        # 											<a href="javascript:fn_find_detail('F2022111300000591', '1')">제기파출소</a>
        # 										</div>
        # 									</td>
        #
        #
        # 							<td scope="row" title="02-961-4304" class="first "><a href="javascript:fn_find_detail('F2022111300000591', '1')">02-961-4304</a></td>
        # 							<td scope="row" class=""><a href="javascript:fn_find_detail('F2022111300000591', '1')">2022-11-11</a></td>
        # 						</tr>
        #
        # 						  <tr>
        # 							<td scope="row" title="V0000552H11130002" class="first "><a href="javascript:fn_find_detail('V0000552H11130002', '1')">V0000552H11130002</a></td>
        # 							<td scope="row" title="어르신교통카드" class="board_title1 "><div class="title_text">
        # 							<a href="javascript:fn_find_detail('V0000552H11130002', '1')">어르신교통카드
        # 								</a></div></td>
        # 							<td style="text-overflow:ellipsis; display:inline-block; overflow: hidden; width: 100px; white-space: nowrap; padding-top:12.5px" scope="row" title="-" class=""><a href="javascript:fn_find_detail('V0000552H11130002', '1')">-</a></td>
        #
        #
        #
        #
        # 									<td scope="row" title="인천터미널역(인천지하철1호선)" class="">
        # 										<div class="losers_text">
        # 											<a href="javascript:fn_find_detail('V0000552H11130002', '1')">인천터미널역(인천지하철1호선)</a>
        # 										</div>
        # 									</td>
        #
        #
        # 							<td scope="row" title="032-441-3126" class="first "><a href="javascript:fn_find_detail('V0000552H11130002', '1')">032-441-3126</a></td>
        # 							<td scope="row" class=""><a href="javascript:fn_find_detail('V0000552H11130002', '1')">2022-11-13</a></td>
        # 						</tr>
        #
        # 						  <tr>
        # 							<td scope="row" title="F2022111300000606" class="first "><a href="javascript:fn_find_detail('F2022111300000606', '1')">F2022111300000606</a></td>
        # 							<td scope="row" title="머니클립" class="board_title1 "><div class="title_text">
        # 							<a href="javascript:fn_find_detail('F2022111300000606', '1')">머니클립
        # 								</a></div></td>
        # 							<td style="text-overflow:ellipsis; display:inline-block; overflow: hidden; width: 100px; white-space: nowrap; padding-top:12.5px" scope="row" title="최*" class=""><a href="javascript:fn_find_detail('F2022111300000606', '1')">최*</a></td>
        #
        #
        #
        #
        # 									<td scope="row" title="사당지구대" class="">
        # 										<div class="losers_text">
        # 											<a href="javascript:fn_find_detail('F2022111300000606', '1')">사당지구대</a>
        # 										</div>
        # 									</td>
        #
        #
        # 							<td scope="row" title="02-521-0112" class="first "><a href="javascript:fn_find_detail('F2022111300000606', '1')">02-521-0112</a></td>
        # 							<td scope="row" class=""><a href="javascript:fn_find_detail('F2022111300000606', '1')">2022-11-13</a></td>
        # 						</tr>
        #
        # 						  <tr>
        # 							<td scope="row" title="V0001520H11130002" class="first "><a href="javascript:fn_find_detail('V0001520H11130002', '1')">V0001520H11130002</a></td>
        # 							<td scope="row" title="37-가방" class="board_title1 "><div class="title_text">
        # 							<a href="javascript:fn_find_detail('V0001520H11130002', '1')">37-가방
        # 								</a></div></td>
        # 							<td style="text-overflow:ellipsis; display:inline-block; overflow: hidden; width: 100px; white-space: nowrap; padding-top:12.5px" scope="row" title="-" class=""><a href="javascript:fn_find_detail('V0001520H11130002', '1')">-</a></td>
        #
        #
        #
        #
        # 									<td scope="row" title="광주공항" class="">
        # 										<div class="losers_text">
        # 											<a href="javascript:fn_find_detail('V0001520H11130002', '1')">광주공항</a>
        # 										</div>
        # 									</td>
        #
        #
        # 							<td scope="row" title="062-940 -0313" class="first "><a href="javascript:fn_find_detail('V0001520H11130002', '1')">062-940 -0313</a></td>
        # 							<td scope="row" class=""><a href="javascript:fn_find_detail('V0001520H11130002', '1')">2022-11-13</a></td>
        # 						</tr>
        #
        # 						  <tr>
        # 							<td scope="row" title="F2022111300000604" class="first "><a href="javascript:fn_find_detail('F2022111300000604', '1')">F2022111300000604</a></td>
        # 							<td scope="row" title="삼성스마트폰" class="board_title1 "><div class="title_text">
        # 							<a href="javascript:fn_find_detail('F2022111300000604', '1')">삼성스마트폰
        # 								<img src="/images/sub/icon_jpg.gif" alt="사진있음"></a></div></td>
        # 							<td style="text-overflow:ellipsis; display:inline-block; overflow: hidden; width: 100px; white-space: nowrap; padding-top:12.5px" scope="row" title="-" class=""><a href="javascript:fn_find_detail('F2022111300000604', '1')">-</a></td>
        #
        #
        #
        #
        # 									<td scope="row" title="구암지구대" class="">
        # 										<div class="losers_text">
        # 											<a href="javascript:fn_find_detail('F2022111300000604', '1')">구암지구대</a>
        # 										</div>
        # 									</td>
        #
        #
        # 							<td scope="row" title="02-870-0850" class="first "><a href="javascript:fn_find_detail('F2022111300000604', '1')">02-870-0850</a></td>
        # 							<td scope="row" class=""><a href="javascript:fn_find_detail('F2022111300000604', '1')">2022-11-13</a></td>
        # 						</tr>
        #
        # 						  <tr>
        # 							<td scope="row" title="F2022111300000602" class="first "><a href="javascript:fn_find_detail('F2022111300000602', '1')">F2022111300000602</a></td>
        # 							<td scope="row" title="보테가베네타 남성용 지갑" class="board_title1 "><div class="title_text">
        # 							<a href="javascript:fn_find_detail('F2022111300000602', '1')">보테가베네타 남성용 지갑
        # 								</a></div></td>
        # 							<td style="text-overflow:ellipsis; display:inline-block; overflow: hidden; width: 100px; white-space: nowrap; padding-top:12.5px" scope="row" title="이*훈" class=""><a href="javascript:fn_find_detail('F2022111300000602', '1')">이*훈</a></td>
        #
        #
        #
        #
        # 									<td scope="row" title="송도국제도시지구대" class="">
        # 										<div class="losers_text">
        # 											<a href="javascript:fn_find_detail('F2022111300000602', '1')">송도국제도시지구대</a>
        # 										</div>
        # 									</td>
        #
        #
        # 							<td scope="row" title="032-453-0830" class="first "><a href="javascript:fn_find_detail('F2022111300000602', '1')">032-453-0830</a></td>
        # 							<td scope="row" class=""><a href="javascript:fn_find_detail('F2022111300000602', '1')">2022-11-13</a></td>
        # 						</tr>
        #
        # 						  <tr>
        # 							<td scope="row" title="V0001517H11130004" class="first  last"><a href="javascript:fn_find_detail('V0001517H11130004', '1')">V0001517H11130004</a></td>
        # 							<td scope="row" title="아동점퍼" class="board_title1  last"><div class="title_text">
        # 							<a href="javascript:fn_find_detail('V0001517H11130004', '1')">아동점퍼
        # 								<img src="/images/sub/icon_jpg.gif" alt="사진있음"></a></div></td>
        # 							<td style="text-overflow:ellipsis; display:inline-block; overflow: hidden; width: 100px; white-space: nowrap; padding-top:12.5px" scope="row" title="-" class=" last"><a href="javascript:fn_find_detail('V0001517H11130004', '1')">-</a></td>
        #
        #
        #
        #
        # 									<td scope="row" title="김해국제공항" class=" last">
        # 										<div class="losers_text">
        # 											<a href="javascript:fn_find_detail('V0001517H11130004', '1')">김해국제공항</a>
        # 										</div>
        # 									</td>
        #
        #
        # 							<td scope="row" title="051-974-3776" class="first  last"><a href="javascript:fn_find_detail('V0001517H11130004', '1')">051-974-3776</a></td>
        # 							<td scope="row" class=" last"><a href="javascript:fn_find_detail('V0001517H11130004', '1')">2022-11-13</a></td>
        # 						</tr>
        #
        # 				<!-- //테이블 반복 구간 끝 -->
        # 			</tbody>

        # //*[@id="contents"]/div[3]/table/tbody
        # get all tr in the tbody, then iterate the tr then find whether it has title of "지갑"
        # if it has, then get the td of the tr and get the text of the td

        example_text = driver.get_inner_html('//*[@id="contents"]/div[3]/table/tbody')
        print("example text > ", example_text)
        # get all tr in the tbody, then iterate the tr then find whether it has title of "지갑"
        # if it has, then get the td of the tr and get the text of the td
        soup = BeautifulSoup(example_text, 'html.parser')
        trs = soup.find_all('tr')
        # check trs have "지갑", "남성지갑", "남성지갑", "박*형", "대전역", then if exists, print the text "check!"
        for tr in trs:
            if tr.find('a', text='지갑') or tr.find('a', text='남성지갑') or tr.find('a', text='여성지갑') or tr.find('a', text='박*형') or tr.find('a', text='대전역'):
                print("check!")
                tds = tr.find_all('td')
                for td in tds:
                    print(td.text)
            else:
                print("not found")

    driver.close()

    return example_text
