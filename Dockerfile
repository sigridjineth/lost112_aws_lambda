FROM lambci/lambda:python3.6
MAINTAINER tech@21buttons.com

USER root

ENV APP_DIR /var/task

WORKDIR $APP_DIR

COPY requirements.txt .
# bin of chromedriver and headless-chromium
COPY bin ./bin
COPY lib ./lib
COPY beautifulsoup4-4.11.1.dist-info ./beautifulsoup4-4.11.1.dist-info
COPY bs4 ./bs4
COPY chromedriver_binary ./chromedriver_binary
COPY chromedriver_binary-2.37.0.dist-info ./chromedriver_binary-2.37.0.dist-info
COPY selenium ./selenium
COPY selenium-2.53.0.dist-info ./selenium-2.53.0.dist-info
COPY soupsieve ./soupsieve
COPY bin ./bin
COPY soupsieve-2.3.2.post1.dist-info ./soupsieve-2.3.2.post1.dist-info
#COPY run.py ./run.py
#COPY webdriver_wrapper.py ./webdriver_wrapper.py

COPY ./src/lambda_function.py ./lambda_function.py
#COPY ./src/webdriver_wrapper.py ./webdriver_wrapper_2.py

RUN mkdir -p $APP_DIR/lib
RUN pip3 install -r requirements.txt -t /var/task/lib
CMD ["lambda_function.lambda_handler"]
