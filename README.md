# Lost112 Find My Wallet
* Python (selenium) Lambda Chromium Automation
* This bot allows to automate actions to Lost 112 page on AWS Lambda.

## Start
* build to amd64 library
```
docker buildx build --platform linux/amd64 -f ./Dockerfile -t wallet .
```
* connect to the ECR
```
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 712218945685.dkr.ecr.us-west-2.amazonaws.com
```
* build to target for x86 & x64 environments
```
docker buildx build --platform linux/amd64 -f ./Dockerfile -t wallet .
```
* tag to the docker image
```
docker tag wallet:latest 712218945685.dkr.ecr.ap-northeast-2.amazonaws.com/wallet:latest
```
* push to the ECR
```
docker push 712218945685.dkr.ecr.ap-northeast-2.amazonaws.com/wallet:latest
```

## But... how?

All the process is explained [here](https://medium.com/21buttons-tech/crawling-thousands-of-products-using-aws-lambda-80332e259de1). Technologies used are:
* Python 3.6
* Selenium
* [Chrome driver](https://sites.google.com/a/chromium.org/chromedriver/)
* [Small chromium binary](https://github.com/adieuadieu/serverless-chrome/releases)

## Requirements

Install docker and dependencies:

* `make fetch-dependencies`
* [Installing Docker](https://docs.docker.com/engine/installation/#get-started)
* [Installing Docker compose](https://docs.docker.com/compose/install/#install-compose)
* [bin for selenium](https://github.com/soumilshah1995/Selenium-on-AWS-Lambda-Python3.7/blob/main/chrome_headless_lambda_layer.sh)
* [selenium youtube](https://www.youtube.com/watch?v=jWqbYiHudt8)
* [setting selenium API for AWS Lambda](https://dev.to/awscommunity-asean/creating-an-api-that-runs-selenium-via-aws-lambda-3ck3)

## Working locally

To make local development easy, you can use the included docker-compose. 
Have a look at the example in `lambda_function.py`: it looks up “21 buttons” on Google and prints the first result. 

Run it with: `make docker-run`

#### Downloading files

If your goal is to use selenium to download files instead of just scraping content from web pages, then
you will need to specify a `download_dir` when initializing the WebDriverWrapper. Your download location 
should be a writable Lambda directory such as `/tmp`. For example, the first code in 
`lambda_handler` would become 

```python
driver = WebDriverWrapper(download_location='/tmp')
```

This will cause file downloads to automatically download into the `download_location` without 
requiring a confirmation dialog. You might need to sleep the handler until the file is downloaded
since this occurs asynchronously.

In order to download a file from a link that opens in a new tab (i.e. `target='_blank'`) you will need to 
call `enable_download_in_headless_chrome` in your scraping script after navigating to the desired page, but before
clicking to download. This will replace all `target='_blank'` with `target='_self'`. For example:

```python
# Navigate to download page
driver._driver.find_element_by_xpath('//a[@href="/downloads/"]').click()
# Enable headless chrome file download
driver.enable_download_in_headless_chrome()
# Click the download link
driver._driver.find_element_by_class_name("btn").click()
```

## Building and uploading the distributable package

Everything is summarized into a simple Makefile so use:

* `make build-lambda-package`
* Upload the `build.zip` resulting file to your AWS Lambda function
* Set Lambda environment variables (same values as in docker-compose.yml)
    * `PYTHONPATH=/var/task/src:/var/task/lib`
    * `PATH=/var/task/bin`
* Adjust lambda function parameters to match your necessities, for the given example:
    * Timeout: +10 seconds
    * Memory: + 250MB 
* CMD override on AWS Lambda (while nothing on the entrypoint)
```
lambda_function.lambda_handler
```

## References
* [PyChromeless](https://github.com/jairovadillo/pychromeless)
* [Docker lambda](https://github.com/lambci/docker-lambda)
* [Lambdium](https://github.com/smithclay/lambdium)
* [Serverless Chrome repo](https://github.com/adieuadieu/serverless-chrome) & [medium post](https://medium.com/@marco.luethy/running-headless-chrome-on-aws-lambda-fa82ad33a9eb)
* [Chromeless](https://github.com/graphcool/chromeless)
