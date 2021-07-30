# This is a sample example code. You can use this to test and validate the API
from src.smsfactor.smsfactor import SMSFactorAPI

if __name__ == '__main__':
    smsfactor = SMSFactorAPI(token="my_special_token")
    print(smsfactor.credits)


# See help at https://dev.smsfactor.com/
