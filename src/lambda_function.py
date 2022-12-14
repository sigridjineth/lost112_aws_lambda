from bs4 import BeautifulSoup
import os
import shutil
import uuid

from selenium import webdriver

lost112_link = 'https://www.lost112.go.kr/find/findList.do'

class WebDriverWrapper:
    def __init__(self, download_location=None):
        chrome_options = webdriver.ChromeOptions()
        self._tmp_folder = '/tmp/{}'.format(uuid.uuid4())
        self.download_location = download_location

        if not os.path.exists(self._tmp_folder):
            os.makedirs(self._tmp_folder)

        if not os.path.exists(self._tmp_folder + '/user-data'):
            os.makedirs(self._tmp_folder + '/user-data')

        if not os.path.exists(self._tmp_folder + '/data-path'):
            os.makedirs(self._tmp_folder + '/data-path')

        if not os.path.exists(self._tmp_folder + '/cache-dir'):
            os.makedirs(self._tmp_folder + '/cache-dir')

        if self.download_location:
            prefs = {'download.default_directory': download_location,
                     'download.prompt_for_download': False,
                     'download.directory_upgrade': True,
                     'safebrowsing.enabled': False,
                     'safebrowsing.disable_download_protection': True,
                     'profile.default_content_setting_values.automatic_downloads': 1}

            chrome_options.add_experimental_option('prefs', prefs)

        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1280x1696')
        chrome_options.add_argument('--user-data-dir={}'.format(self._tmp_folder + '/user-data'))
        chrome_options.add_argument('--hide-scrollbars')
        chrome_options.add_argument('--enable-logging')
        chrome_options.add_argument('--log-level=0')
        chrome_options.add_argument('--v=99')
        chrome_options.add_argument('--single-process')
        chrome_options.add_argument('--data-path={}'.format(self._tmp_folder + '/data-path'))
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--homedir={}'.format(self._tmp_folder))
        chrome_options.add_argument('--disk-cache-dir={}'.format(self._tmp_folder + '/cache-dir'))
        chrome_options.add_argument(
            'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')

        chrome_options.binary_location = os.getcwd() + "/bin/headless-chromium"

        self._driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='./bin/chromedriver')

        if self.download_location:
            self.enable_download_in_headless_chrome()

    def get_url(self, url):
        self._driver.get(url)

    def set_input_value(self, xpath, value):
        elem_send = self._driver.find_element_by_xpath(xpath)
        elem_send.send_keys(value)

    def click(self, xpath):
        elem_click = self._driver.find_element_by_xpath(xpath)
        elem_click.click()

    def get_inner_html(self, xpath):
        elem_value = self._driver.find_element_by_xpath(xpath)
        return elem_value.get_attribute('innerHTML')

    def find(self, xpath):
        return self._driver.find_element_by_xpath(xpath)

    def close(self):
        # Close webdriver connection
        self._driver.quit()

        # Remove specific tmp dir of this "run"
        shutil.rmtree(self._tmp_folder)

        # Remove possible core dumps
        folder = '/tmp'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if 'core.headless-chromi' in file_path and os.path.exists(file_path) and os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)

    def enable_download_in_headless_chrome(self):
        """
        This function was pulled from
        https://github.com/shawnbutton/PythonHeadlessChrome/blob/master/driver_builder.py#L44

        There is currently a "feature" in chrome where
        headless does not allow file download: https://bugs.chromium.org/p/chromium/issues/detail?id=696481

        Specifically this comment ( https://bugs.chromium.org/p/chromium/issues/detail?id=696481#c157 )
        saved the day by highlighting that download wasn't working because it was opening up in another tab.

        This method is a hacky work-around until the official chromedriver support for this.
        Requires chrome version 62.0.3196.0 or above.
        """
        self._driver.execute_script(
            "var x = document.getElementsByTagName('a'); var i; for (i = 0; i < x.length; i++) { x[i].target = '_self'; }")
        # add missing support for chrome "send_command"  to selenium webdriver
        self._driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

        params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': self.download_location}}
        command_result = self._driver.execute("send_command", params)
        print("response from browser:")
        for key in command_result:
            print("result:" + key + ":" + str(command_result[key]))


def lambda_handler(*args, **kwargs):
    global trs_text
    driver = WebDriverWrapper()

    for i in range(3):
        driver.get_url(lost112_link)
        print("link > ", lost112_link)
        # <tbody>
        # 				<!-- ????????? ?????? ?????? ?????? -->
        #
        # 						  <tr>
        # 							<td scope="row" title="F2022111300000595" class="first "><a href="javascript:fn_find_detail('F2022111300000595', '1')">F2022111300000595</a></td>
        # 							<td scope="row" title="????????????" class="board_title1 "><div class="title_text">
        # 							<a href="javascript:fn_find_detail('F2022111300000595', '1')">????????????
        # 								</a></div></td>
        # 							<td style="text-overflow:ellipsis; display:inline-block; overflow: hidden; width: 100px; white-space: nowrap; padding-top:12.5px" scope="row" title="???*???" class=""><a href="javascript:fn_find_detail('F2022111300000595', '1')">???*???</a></td>
        #
        #
        #
        #
        # 									<td scope="row" title="???????????????" class="">
        # 										<div class="losers_text">
        # 											<a href="javascript:fn_find_detail('F2022111300000595', '1')">???????????????</a>
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
        # 							<td scope="row" title="?????????, ?????????, ??????????????????, ?????????????????? ???" class="board_title1 "><div class="title_text">
        # 							<a href="javascript:fn_find_detail('F2022111300000593', '1')">?????????, ?????????, ??????????????????, ?????????????????? ???
        # 								</a></div></td>
        # 							<td style="text-overflow:ellipsis; display:inline-block; overflow: hidden; width: 100px; white-space: nowrap; padding-top:12.5px" scope="row" title="???*???" class=""><a href="javascript:fn_find_detail('F2022111300000593', '1')">???*???</a></td>
        #
        #
        #
        #
        # 									<td scope="row" title="???????????????" class="">
        # 										<div class="losers_text">
        # 											<a href="javascript:fn_find_detail('F2022111300000593', '1')">???????????????</a>
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
        # 							<td scope="row" title="????????? ?????? ????????????" class="board_title1 "><div class="title_text">
        # 							<a href="javascript:fn_find_detail('F2022111300000608', '1')">????????? ?????? ????????????
        # 								</a></div></td>
        # 							<td style="text-overflow:ellipsis; display:inline-block; overflow: hidden; width: 100px; white-space: nowrap; padding-top:12.5px" scope="row" title="???*???" class=""><a href="javascript:fn_find_detail('F2022111300000608', '1')">???*???</a></td>
        #
        #
        #
        #
        # 									<td scope="row" title="??????????????????" class="">
        # 										<div class="losers_text">
        # 											<a href="javascript:fn_find_detail('F2022111300000608', '1')">??????????????????</a>
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
        # 							<td scope="row" title="?????? ????????? ?????????" class="board_title1 "><div class="title_text">
        # 							<a href="javascript:fn_find_detail('F2022111300000591', '1')">?????? ????????? ?????????
        # 								<img src="/images/sub/icon_jpg.gif" alt="????????????"></a></div></td>
        # 							<td style="text-overflow:ellipsis; display:inline-block; overflow: hidden; width: 100px; white-space: nowrap; padding-top:12.5px" scope="row" title="-" class=""><a href="javascript:fn_find_detail('F2022111300000591', '1')">-</a></td>
        #
        #
        #
        #
        # 									<td scope="row" title="???????????????" class="">
        # 										<div class="losers_text">
        # 											<a href="javascript:fn_find_detail('F2022111300000591', '1')">???????????????</a>
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
        # 							<td scope="row" title="?????????????????????" class="board_title1 "><div class="title_text">
        # 							<a href="javascript:fn_find_detail('V0000552H11130002', '1')">?????????????????????
        # 								</a></div></td>
        # 							<td style="text-overflow:ellipsis; display:inline-block; overflow: hidden; width: 100px; white-space: nowrap; padding-top:12.5px" scope="row" title="-" class=""><a href="javascript:fn_find_detail('V0000552H11130002', '1')">-</a></td>
        #
        #
        #
        #
        # 									<td scope="row" title="??????????????????(???????????????1??????)" class="">
        # 										<div class="losers_text">
        # 											<a href="javascript:fn_find_detail('V0000552H11130002', '1')">??????????????????(???????????????1??????)</a>
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
        # 							<td scope="row" title="????????????" class="board_title1 "><div class="title_text">
        # 							<a href="javascript:fn_find_detail('F2022111300000606', '1')">????????????
        # 								</a></div></td>
        # 							<td style="text-overflow:ellipsis; display:inline-block; overflow: hidden; width: 100px; white-space: nowrap; padding-top:12.5px" scope="row" title="???*" class=""><a href="javascript:fn_find_detail('F2022111300000606', '1')">???*</a></td>
        #
        #
        #
        #
        # 									<td scope="row" title="???????????????" class="">
        # 										<div class="losers_text">
        # 											<a href="javascript:fn_find_detail('F2022111300000606', '1')">???????????????</a>
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
        # 							<td scope="row" title="37-??????" class="board_title1 "><div class="title_text">
        # 							<a href="javascript:fn_find_detail('V0001520H11130002', '1')">37-??????
        # 								</a></div></td>
        # 							<td style="text-overflow:ellipsis; display:inline-block; overflow: hidden; width: 100px; white-space: nowrap; padding-top:12.5px" scope="row" title="-" class=""><a href="javascript:fn_find_detail('V0001520H11130002', '1')">-</a></td>
        #
        #
        #
        #
        # 									<td scope="row" title="????????????" class="">
        # 										<div class="losers_text">
        # 											<a href="javascript:fn_find_detail('V0001520H11130002', '1')">????????????</a>
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
        # 							<td scope="row" title="??????????????????" class="board_title1 "><div class="title_text">
        # 							<a href="javascript:fn_find_detail('F2022111300000604', '1')">??????????????????
        # 								<img src="/images/sub/icon_jpg.gif" alt="????????????"></a></div></td>
        # 							<td style="text-overflow:ellipsis; display:inline-block; overflow: hidden; width: 100px; white-space: nowrap; padding-top:12.5px" scope="row" title="-" class=""><a href="javascript:fn_find_detail('F2022111300000604', '1')">-</a></td>
        #
        #
        #
        #
        # 									<td scope="row" title="???????????????" class="">
        # 										<div class="losers_text">
        # 											<a href="javascript:fn_find_detail('F2022111300000604', '1')">???????????????</a>
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
        # 							<td scope="row" title="?????????????????? ????????? ??????" class="board_title1 "><div class="title_text">
        # 							<a href="javascript:fn_find_detail('F2022111300000602', '1')">?????????????????? ????????? ??????
        # 								</a></div></td>
        # 							<td style="text-overflow:ellipsis; display:inline-block; overflow: hidden; width: 100px; white-space: nowrap; padding-top:12.5px" scope="row" title="???*???" class=""><a href="javascript:fn_find_detail('F2022111300000602', '1')">???*???</a></td>
        #
        #
        #
        #
        # 									<td scope="row" title="???????????????????????????" class="">
        # 										<div class="losers_text">
        # 											<a href="javascript:fn_find_detail('F2022111300000602', '1')">???????????????????????????</a>
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
        # 							<td scope="row" title="????????????" class="board_title1  last"><div class="title_text">
        # 							<a href="javascript:fn_find_detail('V0001517H11130004', '1')">????????????
        # 								<img src="/images/sub/icon_jpg.gif" alt="????????????"></a></div></td>
        # 							<td style="text-overflow:ellipsis; display:inline-block; overflow: hidden; width: 100px; white-space: nowrap; padding-top:12.5px" scope="row" title="-" class=" last"><a href="javascript:fn_find_detail('V0001517H11130004', '1')">-</a></td>
        #
        #
        #
        #
        # 									<td scope="row" title="??????????????????" class=" last">
        # 										<div class="losers_text">
        # 											<a href="javascript:fn_find_detail('V0001517H11130004', '1')">??????????????????</a>
        # 										</div>
        # 									</td>
        #
        #
        # 							<td scope="row" title="051-974-3776" class="first  last"><a href="javascript:fn_find_detail('V0001517H11130004', '1')">051-974-3776</a></td>
        # 							<td scope="row" class=" last"><a href="javascript:fn_find_detail('V0001517H11130004', '1')">2022-11-13</a></td>
        # 						</tr>
        #
        # 				<!-- //????????? ?????? ?????? ??? -->
        # 			</tbody>

        # //*[@id="contents"]/div[3]/table/tbody
        # get all tr in the tbody, then iterate the tr then find whether it has title of "??????"
        # if it has, then get the td of the tr and get the text of the td

        trs_text = driver.get_inner_html('//*[@id="contents"]/div[3]/table/tbody')
        print("example text > ", trs_text)

        soup = BeautifulSoup(trs_text, 'html.parser')
        trs = soup.find_all('tr')

        for tr in trs:
            if tr.find('a', text='??????') or tr.find('a', text='????????????') or tr.find('a', text='????????????') or tr.find('a', text='????????????') or tr.find('a', text='???*???') or tr.find('a', text='?????????') or tr.find('a', text='?????????'):
                print("check!")
                tds = tr.find_all('td')
                for td in tds:
                    print(td.text)
            else:
                print("not found")

    print("finished")
    driver.close()

    return trs_text
